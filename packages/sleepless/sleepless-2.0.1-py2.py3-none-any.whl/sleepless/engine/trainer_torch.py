# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Training script."""

from __future__ import annotations

import contextlib
import csv
import datetime
import io
import logging
import multiprocessing
import os
import shutil
import sys
import time
import typing

from collections.abc import Mapping

import numpy
import torch
import torch.nn as nn

from torch.nn import CrossEntropyLoss
from torch.utils.data import DataLoader
from tqdm import tqdm

from ..data.utils import get_samples_weights
from ..utils.checkpointer import Checkpointer
from ..utils.resources import ResourceMonitor, cpu_constants, gpu_constants
from ..utils.summary import summary
from .utils import set_seeds, setup_pytorch_device

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def torch_evaluation(model: nn.Module):
    """Context manager to turn ON/OFF model evaluation. This context manager
    will turn evaluation mode ON on entry and turn it OFF when exiting the
    ``with`` statement block.

    :param model: pytorch network

    Yields
    ------

    model: pytorch network
    """
    model.eval()
    yield model
    model.train()


def check_gpu(device: torch.device):
    """Check the device type and the availability of GPU.

    :param device: device to use
    """
    if device.type == "cuda":
        # asserts we do have a GPU
        assert bool(
            gpu_constants()
        ), f"Device set to '{device}', but nvidia-smi is not installed"


def save_model_summary(output_folder, model) -> tuple[str, int]:
    """Save a little summary of the model in a txt file.

    :param output_folder: output path
    :param model: pytorch network
    :return: r: The model summary in a text format, n: The number of
        parameters of the model.
    """
    summary_path = os.path.join(output_folder, "model_summary.txt")
    logger.info(f"Saving model summary at {summary_path}...")
    with open(summary_path, "w") as f:
        r, n = summary(model)
        logger.info(f"Model has {n} parameters...")
        f.write(r)
    return r, n


def static_information_to_csv(
    static_logfile_name: str, device: torch.device, n: int
):
    """Save the static information in a csv file.

    :param static_logfile_name: The static file name which is a join
        between the output folder and "constant.csv"
    :param device: device to use
    :param n: The number of parameters of the model
    """
    if os.path.exists(static_logfile_name):
        backup = static_logfile_name + "~"
        if os.path.exists(backup):
            os.unlink(backup)
        shutil.move(static_logfile_name, backup)
    with open(static_logfile_name, "w", newline="") as f:
        logdata = cpu_constants()
        if device.type == "cuda":
            logdata += gpu_constants()
        logdata += (("model_size", n),)
        logwriter = csv.DictWriter(f, fieldnames=[k[0] for k in logdata])
        logwriter.writeheader()
        logwriter.writerow(dict(k for k in logdata))


def check_exist_logfile(logfile_name: str, arguments: dict):
    """Check existance of logfile (trainlog.csv), If the logfile exist the and
    the epochs number are still 0, The logfile will be replaced.

    :param logfile_name: The logfile_name which is a join between the
        output_folder and trainlog.csv
    :param arguments: start and end epochs
    """
    if arguments["epoch"] == 0 and os.path.exists(logfile_name):
        backup = logfile_name + "~"
        if os.path.exists(backup):
            os.unlink(backup)
        shutil.move(logfile_name, backup)


def create_logfile_fields(
    valid_loader: DataLoader,
    extra_valid_loaders: list[DataLoader],
    device: torch.device,
) -> tuple:
    """Creation of the logfile fields that will appear in the logfile.

    :param valid_loader: To be used to validate the model and enable automatic checkpointing.
        If set to ``None``, then do not validate it.

    :param extra_valid_loaders: To be used to validate the model, however **does not affect** automatic
        checkpointing. If set to ``None``, or empty, then does not log anything
        else.  Otherwise, an extra column with the loss of every dataset in
        this list is kept on the final training log.

    :param device: device to use

    :return: The fields that will appear in trainlog.csv
    """
    logfile_fields: tuple = (
        "epoch",
        "total_time",
        "eta",
        "loss",
        "learning_rate",
    )
    if valid_loader is not None:
        logfile_fields += ("validation_loss",)
    if extra_valid_loaders:
        logfile_fields += ("extra_validation_losses",)
    logfile_fields += tuple(
        ResourceMonitor.monitored_keys(device.type == "cuda")
    )
    return logfile_fields


def train_epoch(
    loader: DataLoader,
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    criterion: nn._Loss,
    batch_chunk_count: int,
) -> float:
    r"""Trains the model for a single epoch (through all batches)

    :param loader: :py:class:`torch.utils.data.DataLoader`
        To be used to train the model

    :param model: pytorch network

    :param optimizer: pytorch optimizer

    :param device: device to use

    :param criterion: pytorch loss function

    :param batch_chunk_count: If this number is different than 1, then each batch will be divided in
        this number of chunks.  Gradients will be accumulated to perform each
        mini-batch.   This is particularly interesting when one has limited RAM
        on the GPU, but would like to keep training with larger batches.  One
        exchanges for longer processing times in this case.  To better understand
        gradient accumulation, read
        https://stackoverflow.com/questions/62067400/understanding-accumulated-gradients-in-pytorch.

    :return: A floating-point value corresponding the weighted average of this
        epoch's loss
    """
    losses_in_epoch = []
    samples_in_epoch = []
    losses_in_batch = []
    samples_in_batch = []

    # progress bar only on interactive jobs
    for idx, samples in enumerate(
        tqdm(loader, desc="train", leave=False, disable=None)
    ):
        win_epochs = samples[1].to(
            device=device,
            non_blocking=torch.cuda.is_available(),
            dtype=torch.float32,
        )
        labels = samples[2].to(
            device=device,
            non_blocking=torch.cuda.is_available(),
            dtype=torch.int64,
        )

        # Forward pass on the network
        outputs = model(win_epochs)

        if isinstance(outputs, tuple):
            outputs = outputs[0]

        loss = criterion(outputs, labels)

        losses_in_batch.append(loss.item())
        samples_in_batch.append(len(win_epochs))

        # Normalize loss to account for batch accumulation
        loss = loss / batch_chunk_count

        # Accumulate gradients - does not update weights just yet...
        loss.backward()

        # Weight update on the network
        if ((idx + 1) % batch_chunk_count == 0) or (idx + 1 == len(loader)):
            # Advances optimizer to the "next" state and applies weight update
            # over the whole model
            optimizer.step()

            # Zeroes gradients for the next batch
            optimizer.zero_grad()

            # Normalize loss for current batch
            batch_loss = numpy.average(
                losses_in_batch, weights=samples_in_batch
            )
            losses_in_epoch.append(batch_loss.item())
            samples_in_epoch.append(len(win_epochs))

            losses_in_batch.clear()
            samples_in_batch.clear()
            logger.debug(f"batch loss: {batch_loss.item()}")
            logger.debug(f"samples_in_epoch: {len(win_epochs)}")

    return numpy.average(losses_in_epoch, weights=samples_in_epoch)


def validate_epoch(
    loader: DataLoader,
    model: nn.Module,
    device: torch.device,
    criterion: nn._Loss,
    pbar_desc: str,
) -> float:
    """Processes input samples and returns loss (scalar)

    :param loader: To be used to validate the model
    :param model: pytorch network
    :param optimizer: pytorch optimizer
    :param device: device to use
    :param criterion: loss function
    :param pbar_desc: A string for the progress bar descriptor
    :return: A floating-point value corresponding the weighted average
        of this epoch's loss
    """
    batch_losses = []
    samples_in_batch = []

    with torch.no_grad(), torch_evaluation(model):
        for samples in tqdm(loader, desc=pbar_desc, leave=False, disable=None):
            win_epochs = samples[1].to(
                device=device,
                non_blocking=torch.cuda.is_available(),
                dtype=torch.float32,
            )
            labels = samples[2].to(
                device=device,
                non_blocking=torch.cuda.is_available(),
                dtype=torch.int64,
            )

            # data forwarding on the existing network
            outputs = model(win_epochs)
            if isinstance(outputs, tuple):
                outputs = outputs[0]

            loss = criterion(outputs, labels)

            batch_losses.append(loss.item())
            samples_in_batch.append(len(win_epochs))

    return numpy.average(batch_losses, weights=samples_in_batch)


def checkpointer_process(
    checkpointer: Checkpointer,
    checkpoint_period: int,
    valid_loss: float,
    lowest_validation_loss: float,
    arguments: dict,
    epoch: int,
    max_epoch: int,
) -> float:
    """Process the checkpointer, save the final model and keep track of the
    best model.

    :param checkpointer: checkpointer implementation

    :param checkpoint_period: save a checkpoint every ``n`` epochs.  If set to ``0`` (zero), then do
        not save intermediary checkpoints

    :param valid_loss: Current epoch validation loss

    :param lowest_validation_loss: Keeps track of the best (lowest) validation loss

    :param arguments: start and end epochs

    :param epoch: current epoch

    :param max_epoch: end_epoch

    :return: The lowest validation loss currently observed
    """
    if checkpoint_period and (epoch % checkpoint_period == 0):
        checkpointer.save("model_periodic_save", **arguments)

    if valid_loss is not None and valid_loss < lowest_validation_loss:
        lowest_validation_loss = valid_loss
        logger.info(
            f"Found new low on validation set:" f" {lowest_validation_loss:.6f}"
        )
        checkpointer.save("model_lowest_valid_loss", **arguments)

    if epoch >= max_epoch:
        checkpointer.save("model_final_epoch", **arguments)

    return lowest_validation_loss


def write_log_info(
    epoch: int,
    current_time: float,
    eta_seconds: float,
    loss: float,
    valid_loss: float | None,
    extra_valid_losses: list[float] | None,
    optimizer: torch.optim.Optimizer,
    logwriter: csv.DictWriter,
    logfile: io.TextIOWrapper,
    resource_data: tuple,
):
    """Write log info in trainlog.csv.

    :param epoch: Current epoch
    :param current_time: Current training time
    :param eta_seconds: estimated time-of-arrival taking into
        consideration previous epoch performance
    :param loss: Current epoch's training loss
    :param valid_loss: Current epoch's validation loss
    :param extra_valid_losses: Validation losses from other validation
        datasets being currently tracked
    :param optimizer: pytorch optimizer
    :param logwriter: Dictionary writer that give the ability to write
        on the trainlog.csv
    :param logfile: text file containing the logd
    :param resource_data: Monitored resources at the machine (CPU and
        GPU)
    """

    logdata: tuple = (
        ("epoch", f"{epoch}"),
        (
            "total_time",
            f"{datetime.timedelta(seconds=int(current_time))}",
        ),
        ("eta", f"{datetime.timedelta(seconds=int(eta_seconds))}"),
        ("loss", f"{loss:.6f}"),
        ("learning_rate", f"{optimizer.param_groups[0]['lr']:.6f}"),
    )

    if valid_loss is not None:
        logdata += (("validation_loss", f"{valid_loss:.6f}"),)

    if extra_valid_losses:
        entry = numpy.array_str(
            numpy.array(extra_valid_losses),
            max_line_width=sys.maxsize,
            precision=6,
        )
        logdata += (("extra_validation_losses", entry),)

    logdata += resource_data

    logwriter.writerow(dict(k for k in logdata))
    logfile.flush()
    tqdm.write("|".join([f"{k}: {v}" for (k, v) in logdata[:4]]))


def run(
    model: nn.Module,
    data_loader: DataLoader,
    valid_loader: DataLoader | None,
    extra_valid_loaders: list[DataLoader] | None,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim._LRScheduler,
    criterion: nn._Loss,
    checkpointer: Checkpointer,
    checkpoint_period: int,
    device: torch.device,
    arguments: dict,
    output_folder: str,
    monitoring_interval: int | float,
    batch_chunk_count: int,
    criterion_valid: nn._Loss | None,
    patience: int | None,
):
    """Fits a CNN model using supervised learning and save it to disk. This
    method supports periodic checkpointing and the output of a CSV-formatted
    log with the evolution of some figures during training.

    :param model: pytorch network

    :param data_loader: To be used to train the model

    :param valid_loaders: To be used to validate the model and enable automatic checkpointing.
        If ``None``, then do not validate it.

    :param extra_valid_loaders: To be used to validate the model, however **does not affect** automatic
        checkpointing. If empty, then does not log anything else.  Otherwise,
        an extra column with the loss of every dataset in this list is kept on
        the final training log.

    :param optimizer: pytorch optimizer

    :param scheduler: pytorch scheduler

    :param criterion: loss function

    :param checkpointer: checkpointer implementation

    :param checkpoint_period: save a checkpoint every ``n`` epochs.  If set to ``0`` (zero), then do
        not save intermediary checkpoints

    :param device: device to use

    :param arguments: start and end epochs

    :param output_folder: output path

    :param monitoring_interval: interval, in seconds (or fractions), through which we should monitor
        resources during training.

    :param batch_chunk_count: If this number is different than 1, then each batch will be divided in
        this number of chunks.  Gradients will be accumulated to perform each
        mini-batch.   This is particularly interesting when one has limited RAM
        on the GPU, but would like to keep training with larger batches.  One
        exchanges for longer processing times in this case.

    :param criterion_valid: specific loss function for the validation set
    """

    start_epoch = arguments["epoch"]
    max_epoch = arguments["max_epoch"]

    waiting = 0

    check_gpu(device)

    # Save model summary
    r, n = save_model_summary(output_folder, model)

    # write static information to a CSV file
    static_logfile_name = os.path.join(output_folder, "constants.csv")

    static_information_to_csv(static_logfile_name, device, n)

    # Log continous information to (another) file
    logfile_name = os.path.join(output_folder, "trainlog.csv")

    check_exist_logfile(logfile_name, arguments)

    logfile_fields = create_logfile_fields(
        valid_loader, extra_valid_loaders, device
    )

    # the lowest validation loss obtained so far - this value is updated only
    # if a validation set is available
    lowest_validation_loss = sys.float_info.max

    # set a specific validation criterion if the user has set one
    if criterion_valid is None:
        criterion_valid = criterion

    with open(logfile_name, "a+", newline="") as logfile:
        logwriter = csv.DictWriter(logfile, fieldnames=logfile_fields)

        if arguments["epoch"] == 0:
            logwriter.writeheader()

        model.train()  # set training mode

        model.to(device)  # set/cast parameters to device
        for state in optimizer.state.values():
            for k, v in state.items():
                if isinstance(v, torch.Tensor):
                    state[k] = v.to(device)

        # Total training timer
        start_training_time = time.time()

        for epoch in tqdm(
            range(start_epoch, max_epoch),
            desc="epoch",
            leave=False,
            disable=None,
        ):
            with ResourceMonitor(
                interval=monitoring_interval,
                has_gpu=(device.type == "cuda"),
                main_pid=os.getpid(),
                logging_level=logging.ERROR,
            ) as resource_monitor:
                epoch = epoch + 1
                arguments["epoch"] = epoch

                # Epoch time
                start_epoch_time = time.time()

                train_loss = train_epoch(
                    data_loader,
                    model,
                    optimizer,
                    device,
                    criterion,
                    batch_chunk_count,
                )

                valid_loss = (
                    validate_epoch(
                        valid_loader, model, device, criterion_valid, "valid"
                    )
                    if valid_loader is not None
                    else None
                )

                if scheduler is not None:
                    scheduler.step()

                extra_valid_losses = []
                for pos, extra_valid_loader in enumerate(extra_valid_loaders):
                    loss = validate_epoch(
                        extra_valid_loader,
                        model,
                        device,
                        criterion_valid,
                        f"xval@{pos+1}",
                    )
                    extra_valid_losses.append(loss)

            lowest_validation_loss = checkpointer_process(
                checkpointer,
                checkpoint_period,
                valid_loss,
                lowest_validation_loss,
                arguments,
                epoch,
                max_epoch,
            )

            # computes ETA (estimated time-of-arrival; end of training) taking
            # into consideration previous epoch performance
            epoch_time = time.time() - start_epoch_time
            eta_seconds = epoch_time * (max_epoch - epoch)
            current_time = time.time() - start_training_time

            write_log_info(
                epoch,
                current_time,
                eta_seconds,
                train_loss,
                valid_loss,
                extra_valid_losses,
                optimizer,
                logwriter,
                logfile,
                resource_monitor.data,
            )

            if valid_loss > lowest_validation_loss:
                waiting += 1
            else:
                waiting = 0

            if patience is not None:
                if waiting >= patience:
                    logger.info(f"Stop training at epoch {epoch}")
                    logger.info(f"Best val loss : {lowest_validation_loss:.4f}")
                    break

        total_training_time = time.time() - start_training_time
        logger.info(
            f"Total training time: {datetime.timedelta(seconds=total_training_time)} ({(total_training_time/max_epoch):.4f}s in average per epoch)"
        )


def train_torch(
    model: nn.Module,
    training_set: torch.utils.data.ConcatDataset,
    validation_set: list[torch.utils.data.ConcatDataset],
    output_folder: str,
    model_parameters: Mapping,
):
    """Fits a CNN model using supervised learning and save it to disk. This
    method supports periodic checkpointing and the output of a CSV-formatted
    log with the evolution of some figures during training.

    :param model: pytorch network

    :param data_loader: To be used to train the model

    :param valid_loaders: To be used to validate the model and enable automatic checkpointing.
        If ``None``, then do not validate it.

    :param output_folder: path to save the model and parameters

    :param model_parameters: a dictionary where the following keys need to be defined,
        ``optimizer``: :py:class:`torch.optim.Optimizer`
        ``epochs``: int
        ``batch_size``: int
        ``valid_batch_size``: int
        ``batch_chunk_count``: int
        ``drop_incomplete_batch``: bool
        ``criterion``: pytorch loss function
        ``scheduler``: :py:mod:`torch.optim`
        ``checkpoint_period``: int
        ``device``: str
        ``seed``: int
        ``parallel``: int
        ``monitoring_interval``: int | float

        and optionally:

        ``criterion_valid``: pytorch loss function
        ``patience``: pytorch loss function
    """

    optimizer = model_parameters["optimizer"]
    epochs = model_parameters["epochs"]
    batch_size = model_parameters["batch_size"]
    valid_batch_size = model_parameters["valid_batch_size"]
    batch_chunk_count = model_parameters["batch_chunk_count"]
    drop_incomplete_batch = model_parameters["drop_incomplete_batch"]
    criterion = model_parameters["criterion"]
    scheduler = model_parameters["scheduler"]
    checkpoint_period = model_parameters["checkpoint_period"]
    device = model_parameters["device"]
    seed = model_parameters["seed"]
    parallel = model_parameters["parallel"]
    monitoring_interval = model_parameters["monitoring_interval"]

    criterion_valid = criterion

    if "criterion_valid" in model_parameters.keys():
        criterion_valid = model_parameters["criterion_valid"]

    patience = None

    if "patience" in model_parameters.keys():
        patience = model_parameters["patience"]

    device = setup_pytorch_device(device)

    set_seeds(seed, all_gpus=False)

    multiproc_kwargs: dict[str, typing.Any] = dict()
    if parallel < 0:
        multiproc_kwargs["num_workers"] = 0
    else:
        multiproc_kwargs["num_workers"] = (
            parallel or multiprocessing.cpu_count()
        )

    if multiproc_kwargs["num_workers"] > 0 and sys.platform == "darwin":
        multiproc_kwargs[
            "multiprocessing_context"
        ] = multiprocessing.get_context("spawn")

    batch_chunk_size = batch_size
    if batch_size % batch_chunk_count != 0:
        # batch_size must be divisible by batch_chunk_count.
        raise RuntimeError(
            f"--batch-size ({batch_size}) must be divisible by "
            f"--batch-chunk-size ({batch_chunk_count})."
        )
    else:
        batch_chunk_size = batch_size // batch_chunk_count

    valid_batch_chunk_size = valid_batch_size
    if valid_batch_size % batch_chunk_count != 0:
        # batch_size must be divisible by batch_chunk_count.
        raise RuntimeError(
            f"--batch-size ({valid_batch_size}) must be divisible by "
            f"--batch-chunk-size ({batch_chunk_count})."
        )
    else:
        valid_batch_chunk_size = valid_batch_size // batch_chunk_count

    train_samples_weights = get_samples_weights(training_set)
    train_samples_weights = train_samples_weights.to(
        device=device, non_blocking=torch.cuda.is_available()
    )

    data_loader = DataLoader(
        dataset=training_set,
        shuffle=True,
        batch_size=batch_chunk_size,
        drop_last=drop_incomplete_batch,
        pin_memory=torch.cuda.is_available(),
        **multiproc_kwargs,
    )

    valid_loader = None
    if validation_set is not None:
        valid_loader = DataLoader(
            dataset=validation_set[0],
            batch_size=valid_batch_chunk_size,
            shuffle=False,
            drop_last=False,
            pin_memory=torch.cuda.is_available(),
            **multiproc_kwargs,
        )

    extra_valid_loaders = [
        DataLoader(
            dataset=k,
            shuffle=False,
            batch_size=valid_batch_chunk_size,
            drop_last=False,
            pin_memory=torch.cuda.is_available(),
            **multiproc_kwargs,
        )
        for k in validation_set[1:]
    ]

    if isinstance(criterion, torch.nn.CrossEntropyLoss):
        criterion = CrossEntropyLoss(weight=train_samples_weights)
    else:
        logger.warning("Weighted criterion not supported")

    checkpointer = Checkpointer(model, optimizer, scheduler, path=output_folder)

    arguments = {}
    arguments["epoch"] = 0
    extra_checkpoint_data = checkpointer.load()
    arguments.update(extra_checkpoint_data)
    arguments["max_epoch"] = epochs

    logger.info("Training for {} epochs".format(arguments["max_epoch"]))
    logger.info("Continuing from epoch {}".format(arguments["epoch"]))

    run(
        model=model,
        data_loader=data_loader,
        valid_loader=valid_loader,
        extra_valid_loaders=extra_valid_loaders,
        optimizer=optimizer,
        scheduler=scheduler,
        criterion=criterion,
        checkpointer=checkpointer,
        checkpoint_period=checkpoint_period,
        device=device,
        arguments=arguments,
        output_folder=output_folder,
        monitoring_interval=monitoring_interval,
        batch_chunk_count=batch_chunk_count,
        criterion_valid=criterion_valid,
        patience=patience,
    )
