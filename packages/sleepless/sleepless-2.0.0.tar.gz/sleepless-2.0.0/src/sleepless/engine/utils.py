# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Setup functions for engine."""

import logging
import os
import random
import tempfile
import urllib.request

import h5py
import numpy as np
import torch

from tqdm import tqdm

from ..data.sample import DelayedSample

logger = logging.getLogger(__name__)


def setup_pytorch_device(name: str) -> torch.device:
    """Sets-up the pytorch device to use.

    :param name: The device name (``cpu``, ``cuda:0``, ``cuda:1``, and so on).  If you
        set a specific cuda device such as ``cuda:1``, then we'll make sure it
        is currently set.


    :return: The pytorch device to use, pre-configured (and checked)
    """

    if name.startswith("cuda:"):
        # In case one has multiple devices, we must first set the one
        # we would like to use so pytorch can find it.
        logger.info(f"User set device to '{name}' - trying to force device...")
        os.environ["CUDA_VISIBLE_DEVICES"] = name.split(":", 1)[1]
        if not torch.cuda.is_available():
            raise RuntimeError(
                f"CUDA is not currently available, but "
                f"you set device to '{name}'"
            )
        # Let pytorch auto-select from environment variable
        return torch.device("cuda")

    elif name.startswith("cuda"):  # use default device
        logger.info(f"User set device to '{name}' - using default CUDA device")
        assert os.environ.get("CUDA_VISIBLE_DEVICES") is not None

    # cuda or cpu
    return torch.device(name)


def set_seeds(value: int, all_gpus: bool):
    """Sets up all relevant random seeds (numpy, python, cuda)

    If running with multiple GPUs **at the same time**, set ``all_gpus`` to
    ``True`` to force all GPU seeds to be initialized.

    Reference: `PyTorch page for reproducibility
    <https://pytorch.org/docs/stable/notes/randomness.html>`_.

    :param value: The random seed value to use


    :param all_gpus: If set, then reset the seed on all GPUs available at once.  This is
        normally **not** what you want if running on a single GPU
    """

    random.seed(value)
    np.random.seed(value)
    torch.manual_seed(value)
    torch.cuda.manual_seed(value)  # noop if cuda not available

    # set seeds for all gpus
    if all_gpus:
        torch.cuda.manual_seed_all(value)  # noop if cuda not available


def download_to_tempfile(
    url: str, progress: bool = False
) -> tempfile._TemporaryFileWrapper:
    """Downloads a file to a temporary named file and returns it.

    :param url: The URL pointing to the file to download
    :param progress: If a progress bar should be displayed for
        downloading the URL.
    :return: A named temporary file that contains the downloaded URL
    """

    file_size = 0
    response = urllib.request.urlopen(url)
    meta = response.info()
    if hasattr(meta, "getheaders"):
        content_length = meta.getheaders("Content-Length")
    else:
        content_length = meta.get_all("Content-Length")

    if content_length is not None and len(content_length) > 0:
        file_size = int(content_length[0])

    progress &= bool(file_size)

    f = tempfile.NamedTemporaryFile()

    with tqdm(total=file_size, disable=not progress) as pbar:
        while True:
            buffer = response.read(8192)
            if len(buffer) == 0:
                break
            f.write(buffer)
            pbar.update(len(buffer))

    f.flush()
    f.seek(0)
    return f


def save_hdf5(
    stem,
    prob: np.ndarray,
    label: np.ndarray,
    epochs_index: np.ndarray,
    output_folder: str,
    features: np.ndarray = None,
):
    """Saves predictions, label and night_epochs_index in a hdf5 format. Be
    careful that if the file already exist data will be append to this existing
    file.

    :param stem: the name of the file without extension on the original
        dataset
    :param prob: 2d nd.array of shape (nb_epochs,nb_classes)
    :param label: 1d nd.array of shape (nb_epochs,)
    :param epochs_index: 1d nd.array of shape (nb_epochs,)
    :param output_folder: path where to store predictions
    :param features: 2d of shape (nb_epochs,nb_features)
    """

    fullpath = os.path.join(output_folder, f"{stem}.hdf5")
    tqdm.write(f"Saving {fullpath}...")

    os.makedirs(os.path.dirname(fullpath), exist_ok=True)

    data = np.hstack((epochs_index[:, None], label[:, None], prob))
    max_shape = (None, data.shape[1])

    if features is not None:
        features = np.hstack((epochs_index[:, None], label[:, None], features))
        max_shape_feat = (None, features.shape[1])

    if os.path.isfile(fullpath):
        with h5py.File(fullpath, "a") as f:
            f["prob"].resize((f["prob"].shape[0] + len(data)), axis=0)
            f["prob"][-len(data) :] = data
            if features is not None:
                f["features"].resize(
                    (f["features"].shape[0] + len(features)), axis=0
                )
                f["features"][-len(features) :] = features

    else:
        with h5py.File(fullpath, "w") as f:
            f.create_dataset(
                "prob",
                data=data,
                dtype=np.float32,
                compression="gzip",
                compression_opts=9,
                maxshape=max_shape,
            )
            if features is not None:
                f.create_dataset(
                    "features",
                    data=features,
                    dtype=np.float32,
                    compression="gzip",
                    compression_opts=9,
                    maxshape=max_shape_feat,
                )


def load_from_hdf5(
    dataset: dict[str, list[DelayedSample]],
    predicted_folder: str,
    dataset_key: str,
) -> dict[str, list[DelayedSample]]:
    """Load either predictions or features and label from a hdf5 file and
    attached it to the dataset samples.

    :param dataset: the original dataset
    :param predicted_folder: path where predictions have been stored
    :param dataset_key: the key of the dataset to load can be "prob" or
        "features"
    :return: the original dataset where predictions have been attached
        to each samples
    """
    for k, v in dataset.items():
        for sample in v:
            fullpath = os.path.join(
                predicted_folder, str(k), f"{sample.key}.hdf5"
            )

            with h5py.File(fullpath, "r") as f:
                data = f[dataset_key][:]

            data_ordered = data[data[:, 0].argsort()]

            sample.label = data_ordered[:, 1]

            if dataset_key == "prob":
                sample.output_prob = data_ordered[:, 2:]

            elif dataset_key == "features":
                sample.features = data_ordered[:, 2:]

    return dataset
