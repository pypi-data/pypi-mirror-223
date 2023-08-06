# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Data loading code."""

from __future__ import annotations

import functools
import logging
import os

logger = logging.getLogger(__name__)

from abc import ABC, abstractmethod
from collections.abc import Callable

from mne import (
    Annotations,
    Epochs,
    pick_channels,
    read_annotations,
    read_epochs,
    set_bipolar_reference,
)
from mne.channels import combine_channels
from mne.io import read_raw_edf
from mne.io.edf.edf import RawEDF
from scipy import signal

from .sample import DelayedSample
from .transforms import RawToEpochs


class Loader(ABC):
    def __init__(
        self, transform_parameters, csv_subset, protocol_name: str
    ) -> None:
        if "band-filter" in transform_parameters:
            self.filter_param = transform_parameters["band-filter"]
        else:
            self.filter_param = None

        if "combined-chan" in transform_parameters:
            self.transform_combine = transform_parameters["combined-chan"]
        else:
            self.transform_combine = None

        if "bipol-ref" in transform_parameters:
            self.transform_bipolref = transform_parameters["bipol-ref"]
        else:
            self.transform_bipolref = None

        if "raw-to-epochs-params" in transform_parameters:
            self.transform_epochs = transform_parameters["raw-to-epochs-params"]
        else:
            self.transform_epochs = None

        if "resampling" in transform_parameters:
            self.resampling_params = transform_parameters["resampling"]
        else:
            self.resampling_params = None

        self.metadata = self._get_metadata_from_csv(csv_subset)

        self.protocol_name = protocol_name

        self.preproc_path = None

    @abstractmethod
    def _get_metadata_from_csv(self, csv_subset) -> dict:
        pass

    def _raw_filtering(self, raw: RawEDF) -> RawEDF:
        frq = int(raw.info["sfreq"])

        freq_range = self.filter_param["freq-range"]
        len_filter = self.filter_param["filter-len"]

        raw.load_data()

        scipy_filter = signal.firwin(
            len_filter, freq_range, fs=frq, pass_zero=False
        )
        raw._data = signal.filtfilt(scipy_filter, 1, raw._data, axis=1)

        logger.info("raw filtered")

        return raw

    def _raw_combine_channels(self, raw: RawEDF) -> RawEDF:
        mix = self.transform_combine["group"]
        method = self.transform_combine["method"]

        groups = {
            k: pick_channels(raw.info["ch_names"], include=v)
            for k, v in mix.items()
        }

        raw_combine = combine_channels(raw, groups=groups, method=method)

        raw_combine.set_meas_date(raw.info["meas_date"])

        raw.load_data().add_channels([raw_combine])

        logger.info("raws combined")

        return raw

    def _raw_compute_bip_ref(self, raw: RawEDF) -> RawEDF:
        name_list = []
        anode_list = []
        cathode_list = []

        for k, v in self.transform_bipolref.items():
            name_list.append(k)
            anode_list.append(v[0])
            cathode_list.append(v[1])

        raw_bipo_ref = set_bipolar_reference(
            raw, cathode_list, anode_list, ch_name=name_list
        )

        logger.info("bipolar ref computed")

        return raw_bipo_ref

    def _raw_to_epochs(self, raw: RawEDF, label: Annotations) -> Epochs:
        raw_to_epochs_transformer = RawToEpochs(**self.transform_epochs)

        epochs_obj = raw_to_epochs_transformer.transform(raw, label)
        label_from_obj = epochs_obj.events[:, 2]

        logger.info("epochs and labels computed")

        return (epochs_obj, label_from_obj)

    def _epochs_resample(self, epochs_obj: Epochs) -> Epochs:
        sample_freq = epochs_obj.info["sfreq"]

        desired_freq = self.resampling_params["sfreq"]

        logger.info(
            f"resampled as sampling frequency was {sample_freq} and {desired_freq} is needed"
        )

        resampled_epochs = epochs_obj.load_data().resample(
            **self.resampling_params
        )

        return resampled_epochs

    def _raw_data_transf_pipeline(self, sample):
        key = os.path.splitext(sample["data"])[0]

        if self.preproc_path is not None:
            path_file = os.path.join(
                self.preproc_path, self.protocol_name, key + "_epo.fif"
            )

            out_check = self._checkpoint_raw_data_loader(path_file)

            if out_check is not None:
                logger.info(f"Loaded already preprocess data {key}")
                return dict(data=out_check[0], label=out_check[1])

        raw, label = self._raw_data_loader(sample)

        logger.info(f"start preprocessing {key}")

        if self.filter_param is not None:
            raw = self._raw_filtering(raw)

        if self.transform_combine is not None:
            raw = self._raw_combine_channels(raw)

        if self.transform_bipolref is not None:
            raw = self._raw_compute_bip_ref(raw)

        if self.transform_epochs is not None:
            raw, label = self._raw_to_epochs(raw, label)

            if self.resampling_params is not None:
                raw = self._epochs_resample(raw)

        logger.info("preprocessing ended")

        if self.preproc_path is not None:
            raw.save(path_file, overwrite=True)
            logger.info(f"saved at {path_file}")

        return dict(data=raw, label=label)

    @abstractmethod
    def _raw_data_loader(self, sample):
        pass

    @abstractmethod
    def _map_key_metadata(self, key):
        pass

    def _checkpoint_raw_data_loader(self, path_file):
        path_dir = os.path.dirname(path_file)

        if os.path.isfile(path_file):
            epochs_from_file = read_epochs(path_file, preload=False)

            logger.info(f"loading {path_file} ")

            label_from_file = epochs_from_file.events[:, 2]

            return (epochs_from_file, label_from_file)

        else:
            os.makedirs(path_dir, exist_ok=True)

            return None

    def _loader(self, context, sample):
        # "context" is ignored in this case - database is homogeneous
        # we returned delayed samples to avoid loading all nights
        key = os.path.splitext(sample["data"])[0]
        key_dic = self._map_key_metadata(key)

        if len(self.metadata) > 0:
            metadata_sample = self.metadata[key_dic]
        else:
            metadata_sample = {}

        return make_delayed(
            sample,
            self._raw_data_transf_pipeline,
            key=key,
            metadata=metadata_sample,
        )


def load_edf_raw(
    path: str,
    infer_types: bool,
    preload: bool,
    misc: list[str] | None = None,
    exclude: list[str] | None = [],
) -> RawEDF:
    """Loads PSG signals sample from an EDF file.

    :param path: The full path to the EDF file to be loaded
    :param infer_types: If True mne will try to to infer the type of
        channel (e.g. eeg) from their name
    :param preload: If True data will be loaded in memory
    :param misc: Name of misc channels
    :param exclude: A list of channel to not load
    :return: A mne raw object
    """

    raw_edf = read_raw_edf(
        path,
        infer_types=infer_types,
        misc=misc,
        preload=preload,
        exclude=exclude,
        verbose=False,
    )

    return raw_edf


def load_annotation_raw(path: str) -> Annotations:
    """Loads annotation sample from an EDF or TXT file.

    :param path: The full path to the EDF or TXT file to be loaded
    :return: A mne object for annotating segments of raw data
    """
    annotations_raw = read_annotations(path)

    return annotations_raw


def make_delayed(
    sample: dict[str, str],
    loader: Callable,
    key: str | None = None,
    metadata: dict = {},
) -> DelayedSample:
    """Returns a delayed-loading Sample object.

    :param sample: A dictionary that maps field names to sample data values (e.g. paths)

    :param loader: A function that inputs ``sample`` dictionaries and returns the loaded
            data.

    :param key: A unique key identifier for this sample.  If not provided, assumes
                ``sample`` is a dictionary with a ``data`` entry and uses its path as
                key.

    :return: In which ``key`` is as provided and ``data`` can be accessed to trigger
            sample loading.
    """

    return DelayedSample(
        functools.partial(loader, sample),
        key=key or os.path.splitext(sample["data"])[0],
        **metadata,
    )
