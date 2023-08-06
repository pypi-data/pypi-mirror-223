# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Predcition script."""

import datetime
import logging
import multiprocessing
import os
import sys
import time
import typing

from collections.abc import Mapping

import numpy as np
import torch
import torch.nn as nn

from torch.utils.data import DataLoader
from tqdm import tqdm

from ..data.utils import ComposeTransform
from ..utils.checkpointer import Checkpointer
from .utils import download_to_tempfile, save_hdf5, setup_pytorch_device

logger = logging.getLogger(__name__)


def run(
    model: nn.Module,
    data_loader: torch.utils.data.DataLoader,
    name: str,
    device: torch.device,
    output_folder: str,
):
    """Runs inference on input data, outputs HDF5 files with predictions.

    :param model: neural network model fitted

    :param data_loader: dataset

    :param name: the local name of this dataset (e.g. ``train``, or ``test``), to be
        used when saving measures files.

    :param device: device to use

    :param output_folder: folder where to store output prediction (HDF5 files)
    """

    logger.info(f"Output folder: {output_folder}")

    logger.info(f"Device: {device}")

    model.eval()  # set evaluation mode
    model.to(device)  # set/cast parameters to device

    # Setup timers
    start_total_time = time.time()
    times = []
    len_samples = []

    output_folder = os.path.join(output_folder, name)

    for samples in tqdm(data_loader, desc="batches", leave=False, disable=None):
        names = np.array(samples[0])
        labels = samples[2]
        win_epochs = samples[1].to(
            device=device,
            non_blocking=torch.cuda.is_available(),
            dtype=torch.float32,
        )

        win_epochs_index = samples[3]

        with torch.no_grad():
            start_time = time.perf_counter()
            predictions = model(win_epochs)

            features = None
            if isinstance(predictions, tuple):
                predictions, features = predictions

            batch_time = time.perf_counter() - start_time
            times.append(batch_time)
            len_samples.append(len(win_epochs))
            unique_names = np.unique(np.array(names))

            for name in unique_names:
                mask_index_name = names == name

                prediction_to_save = (
                    predictions[mask_index_name, :].cpu().squeeze(1).numpy()
                )
                label_to_save = labels[mask_index_name].numpy()
                win_epochs_to_save = win_epochs_index[mask_index_name].numpy()

                features_to_save = None
                if features is not None:
                    features_to_save = (
                        features[mask_index_name, :].cpu().squeeze(1).numpy()
                    )

                save_hdf5(
                    name,
                    prediction_to_save,
                    label_to_save,
                    win_epochs_to_save,
                    output_folder,
                    features_to_save,
                )

    # report operational summary
    total_time = datetime.timedelta(seconds=int(time.time() - start_total_time))
    logger.info(f"Total time: {total_time}")

    average_batch_time = np.mean(times)
    logger.info(f"Average batch time: {average_batch_time:g}s")

    average_image_time = np.sum(np.array(times) * len_samples) / float(
        sum(len_samples)
    )
    logger.info(f"Average image time: {average_image_time:g}s")


def predict_torch(
    dataset: dict,
    model: nn.Module,
    weight: str,
    output_folder: str,
    model_parameters: Mapping,
):
    """Prepare data and model to runs inference on data.

    :param dataset: A dictionary containing a :py:class:`torch.utils.data.ConcatDataset` per key

    :param model: neural network model not fitted

    :param weight: weigth path to fit the neural network

    :param output_folder: folder where prediciton will be saved

    :param model_parameters: a dictionary where the following keys need to be defined,
        ``batch_size``: int
        ``parallel``: int
        ``device``: str
        ``transform``: list (if data are not trasnformed yet)
    """
    batch_size = model_parameters["batch_size"]
    device = model_parameters["device"]
    parallel = model_parameters["parallel"]

    device = setup_pytorch_device(device)

    if weight.startswith("http"):
        logger.info(f"Temporarily downloading '{weight}'...")
        f = download_to_tempfile(weight, progress=True)
        weight_fullpath = os.path.abspath(f.name)
    else:
        weight_fullpath = os.path.abspath(weight)

    checkpointer = Checkpointer(model)
    checkpointer.load(weight_fullpath)

    if "transform" in model_parameters:
        compose_transform = ComposeTransform(model_parameters["transform"])

    for k, v in dataset.items():
        if not isinstance(v, torch.utils.data.ConcatDataset):
            v = compose_transform(v)

        if k.startswith("_"):
            logger.info(f"Skipping dataset '{k}' (not to be evaluated)")
            continue

        logger.info(f"Running inference on '{k}' set...")

        # PyTorch dataloader
        multiproc_kwargs: dict[str, typing.Any] = dict()
        if parallel < 0:
            multiproc_kwargs["num_workers"] = 0
        else:
            multiproc_kwargs["num_workers"] = (
                parallel or multiprocessing.cpu_count()
            )

        if multiproc_kwargs["num_workers"] > 0 and sys.platform.startswith(
            "darwin"
        ):
            multiproc_kwargs[
                "multiprocessing_context"
            ] = multiprocessing.get_context("spawn")

        data_loader = DataLoader(
            dataset=v,
            batch_size=batch_size,
            shuffle=False,
            pin_memory=torch.cuda.is_available(),
            **multiproc_kwargs,
        )
        run(model, data_loader, k, device, output_folder)
