# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Common utilities."""

from __future__ import annotations

import mne
import numpy as np
import torch

from sklearn.utils.class_weight import compute_class_weight
from torch.utils.data import ConcatDataset, Dataset

from .sample import DelayedSample, Sample


def plot_PSG_and_annotation(raw_obj, annot_obj):
    """Plot raw signal with annotation using MNE plot function."""
    raw_obj.set_annotations(annot_obj, emit_warning=False)

    return raw_obj.plot(
        start=1200,
        duration=30,
        scalings=dict(eeg=2e-4, eog=1e-4, emg=10 - 7),
    )


class ComposeTransform:
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, sample_data):
        for t in self.transforms:
            new_sample_data = t(sample_data)
        return new_sample_data


def saving_preprocess(dataset):
    for k, v in dataset.items():
        for sample in v:
            sample.data
    return


class ListSampleDataset(Dataset):
    """PyTorch dataset wrapper around Sample list. This Class takes a
    py:class:`DelayedSample`or :py:class:`Sample` object and generate a object
    as :py:class:`torch.utils.data.dataset.Dataset` where every sample of the
    dataset is defined as a list. It supports indexing such that dataset[i] can
    be used to get the i-th sample.

    :param sample: sample to be wrap into the dataset object
    :param normalize: if set to True, we remove the mean of data, and
        divided them by the standard deviation (it is done epoch
        (window) wise)
    :param pick_chan: the channel type (e.g. "eeg","eog") or name (e.g.
        "Fpz-Cz") whom extract the features, if None default compute
        features for all EEG channels.
    :param n_past_epochs: it indicates how many past epochs to
        concatenate to the current sample epoch. E.g. if n_past_epochs =
        1, then one past epoch is concatenated to the current.
    """

    def __init__(
        self,
        sample: DelayedSample | Sample,
        normalize: bool,
        pick_chan: dict[str, bool | list[str]] | None,
        n_past_epochs: int = 0,
    ):
        self.key = sample.key

        self.labels = sample.data["label"]

        epochs = sample.data["data"]

        pick_chan_idx = "eeg"
        if pick_chan is not None:
            pick_chan_idx = mne.pick_types(info=epochs.info, **pick_chan)

        data = epochs.get_data(picks=pick_chan_idx)

        self.data = data

        self.n_past_epochs = n_past_epochs

        # if normalize is true remove the mean of the data and divide
        # by the standard deviation, the result is set to zero if the standard deviation
        # is equal to zero
        if normalize:
            data_tensor = torch.from_numpy(data)
            mean_data = torch.mean(data_tensor, dim=-1, keepdim=True)
            std_data = torch.std(data_tensor, dim=-1, keepdim=True)

            data_norm = torch.where(
                std_data != 0,
                (data_tensor - mean_data) / std_data,
                torch.zeros(data_tensor.shape),
            )
            self.data = data_norm

    def __len__(self) -> int:
        """
        :return: The size of the dataset
        """
        return len(self.labels)

    def __getitem__(self, idx: int) -> list:
        """
        :param idx: int

        :return: sample data with following structure [name path of the file,data,label,night_epoch_index]
        """
        # Create a tensor of indexes, where the negative indexes indicate that padding is required
        indexes = torch.arange(
            idx - self.n_past_epochs, idx + 1, dtype=torch.long
        )

        # Create a tensor with zeros, with dimensions based on self.data
        dt = torch.zeros((len(indexes), self.data.shape[1], self.data.shape[2]))

        # Iterate over the indexes
        for i in range(len(indexes)):
            # Check if the index is greater than or equal to 0
            if indexes[i] >= 0:
                # Set the i-th element of dt to a tensor created from self.data at the corresponding index
                dt[i] = torch.Tensor(self.data[indexes[i]])

        # Check if dt has more than one element
        if dt.shape[0] > 1:
            # Reshape dt to have dimensions dt.shape[1] and dt.shape[0]*dt.shape[2]
            dt = dt.reshape(dt.shape[1], dt.shape[0] * dt.shape[2])
            # Return a list containing self.key, dt, self.labels[idx], and idx
            return [self.key, dt, self.labels[idx], idx]

        # If dt has only one element, remove the extra dimension
        return [self.key, dt.squeeze(), self.labels[idx], idx]


def get_samples_weights(dataset: ConcatDataset | Dataset):
    """Compute the weights of all the samples of the dataset to balance the
    cross-entropy criterion. This function takes as input a
    :py:class:`torch.utils.data.dataset.Dataset` and computes the weights to
    balance each class in the dataset and the datasets themselves if we have a
    ConcatDataset.

    :param dataset: torch.utils.data.dataset.Dataset
        An instance of torch.utils.data.dataset.Dataset
        ConcatDataset are supported

    :return: :py:class:`torch.Tensor`
        the weights for all the samples in the dataset given as input
    """

    train_y = np.concatenate([ds.labels for ds in dataset.datasets])

    class_weights = compute_class_weight(
        "balanced", classes=np.unique(train_y), y=train_y
    )

    return torch.tensor(class_weights, dtype=torch.float32)


def chan_list_to_dict(chan_list: list[str]) -> dict[str, bool | list[str]]:
    """Handle list which are a mix of channel type and channel names. To be use
    then with the :py:func:`mne.pick_types`

    :param chan_list: list of channel which can be channel
        type or channel names

    :return: dictionary where recognized channel types are assigned as key and their value set to true
        and other channels are expected to be channel names and are placed in a list, the key of this list is "include".
        See :py:func:`mne.pick_types` for more information
    """

    list_of_types = [
        "eeg",
        "seeg",
        "ecog",
        "dbs",
        "eog",
        "ecg",
        "emg",
        "bio",
        "resp",
        "temp",
        "misc",
        "sao2",
    ]

    dic: dict[str, bool | list[str]] = {}

    include_list: list[str] = []

    for chan in chan_list:
        low_case_chan_name = chan.lower()

        if low_case_chan_name in list_of_types:
            dic[low_case_chan_name] = True

        else:
            include_list.append(chan)

    dic["include"] = include_list

    return dic
