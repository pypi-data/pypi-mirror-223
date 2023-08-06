# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# For Class RawToEpochs, Class EEGPowerBand and Class FeatureExtractorChambon:
# SPDX-FileCopyrightText: Copyright © 2011-2022, authors of MNE-Python
#
# SPDX-FileContributor: Alexandre Gramfort <alexandre.gramfort@inria.fr>
# SPDX-FileContributor: Stanislas Chambon <stan.chambon@gmail.com>
# SPDX-FileContributor: Joan Massich <mailsik@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause
"""Signal transformations for our pipelines."""

from __future__ import annotations

import logging

import mne
import numpy as np
import scipy
import torch

from mne import Annotations, Epochs, events_from_annotations
from mne.io.edf.edf import RawEDF
from torch.utils.data import ConcatDataset

from .sample import DelayedSample
from .utils import ListSampleDataset, chan_list_to_dict

logger = logging.getLogger(__name__)


class RawToEpochs:
    """Transform Raw and Annotation objects to Epochs object, with some
    preprocessing options. Data are not loaded in memory until
    mne.Epochs.get_data() is call.

    This class was inspired from version 1.4 of
    https://mne.tools/stable/auto_tutorials/clinical/60_sleep.html

    :param raw_obj: A mne raw object
    :param annot_obj: A mne object for annotating segments of raw data
    :param event_id: Map stage_name (str=keys) and interger event codes
        (int=values)
    :param chunk_duration: The window time (in seconde) that was used to
        annotated
    :param picks_chan: List of channels to keep (e.g.
        ['eeg','eog','emg']), if None (default)
    :param no_overlapping: If True remove last sample from epoch to
        avoid overlapping, Default (False)
    :param crop_wake_time: Wake time (in minute) to keep at the begining
        and the end, in some case it is usefull to crop a part of the
        wake time if it is too long regarding the other stage or not
        usefull (e.g. walking time)
    :param wake_stage_name: Only needed for crop_wake_time. (e.g. "Sleep
        stage W")
    """

    def __init__(
        self,
        event_id: dict[str, int],
        chunk_duration: float,
        picks_chan: str | list[str] | None = None,
        no_overlapping: bool = True,
        crop_wake_time: float = 0.0,
        wake_stage_name: str | None = None,
    ):
        self.event_id = event_id
        self.chunk_duration = chunk_duration
        self.picks_chan = picks_chan
        self.no_overlapping = no_overlapping
        self.crop_wake_time = crop_wake_time
        self.wake_stage_name = wake_stage_name

    def __call__(self, samples: list[DelayedSample]) -> list[DelayedSample]:
        """Return a list of samples with computed epochs.

        :return: A list of samples with where mne.epochs are computed
        """

        for index, sample in enumerate(samples, 1):
            logger.info(
                f"computing epochs for sample {index} on {len(samples)} samples"
            )

            sample.epochs = self.transform(
                sample.data["data"], sample.data["label"]
            )

        return samples

    def transform(self, raw_obj: RawEDF, annot_obj: Annotations) -> Epochs:
        """Return the mne.Epochs object from raw data and label of a sample.

        :return: A mne Epochs object
        """

        raw_obj.set_annotations(annot_obj, emit_warning=True, verbose=True)
        if self.crop_wake_time > 0:
            if self.wake_stage_name is None:
                logger.error(
                    "wake_stage_name need to be defined for cropping process"
                )

            mask = [x == self.wake_stage_name for x in annot_obj.description]
            sleep_event_inds = np.where(mask)[0]

            tmin = (
                annot_obj[int(sleep_event_inds[0] + 1)]["onset"]
                - self.crop_wake_time * 60
            )
            tmin = max(raw_obj.times[0], tmin)
            tmax = (
                annot_obj[int(sleep_event_inds[-1])]["onset"]
                + self.crop_wake_time * 60
            )
            tmax = min(tmax, raw_obj.times[-1])
            raw_obj.crop(tmin=tmin, tmax=tmax)

        events, map_event_id = events_from_annotations(
            raw_obj,
            event_id=self.event_id,
            chunk_duration=self.chunk_duration,
            verbose=True,
        )

        tmax = self.chunk_duration

        if self.no_overlapping:
            tmax = self.chunk_duration - 1.0 / raw_obj.info["sfreq"]

        epochs_obj = Epochs(
            raw=raw_obj,
            events=events,
            event_id=map_event_id,
            picks=self.picks_chan,
            tmin=0.0,
            tmax=tmax,
            preload=False,
            baseline=None,
            verbose=True,
            on_missing="warn",
        )

        return epochs_obj


class EEGPowerBand:
    """Extract feature from a py:class:`DelayedSample` list.

    This class was copied and modified from https://mne.tools/stable/auto_tutorials/clinical/60_sleep.html v1.4

    Modification: change to class, adding pick_chan attribute, management division by zero

    :param pick_chan: the channel type (e.g. "eeg","eog") or name (e.g. "Fpz-Cz") whom extract the features, if None default compute
        features for all EEG channels.

    :return: py:class:`DelayedSample` list where features have been extracted
    """

    def __init__(self, pick_chan: list[str] = None):
        self.pick_chan = None

        if pick_chan is not None:
            self.pick_chan = chan_list_to_dict(pick_chan)

    def __call__(self, samples: list[DelayedSample]) -> list[DelayedSample]:
        for index, sample in enumerate(samples, 1):
            logger.info(
                f"computing frequency decomposition for sample {index} on {len(samples)} samples"
            )

            sample.features, sample.label = (
                self._transform(sample.data["data"]),
                sample.data["data"].events[:, 2],
            )

        return samples

    def _transform(self, epochs: Epochs) -> np.ndarray:
        """EEG relative power band feature extraction. This function takes an
        ``mne.Epochs`` object and creates EEG features based on relative power
        in specific frequency bands. Also saving the labels as attribute of the
        sample while data are loaded.

        :param epochs: mne.Epochs of a sample
        :return: Transformed data of shape [n_epochs, n_channel*5]
        """

        FREQ_BANDS = {
            "delta": [0.5, 4.5],
            "theta": [4.5, 8.5],
            "alpha": [8.5, 11.5],
            "sigma": [11.5, 15.5],
            "beta": [15.5, 30],
        }

        pick_chan_idx = "eeg"
        if self.pick_chan is not None:
            pick_chan_idx = mne.pick_types(info=epochs.info, **self.pick_chan)

        spectrum = epochs.compute_psd(fmin=0.5, fmax=30.0, picks=pick_chan_idx)
        psds, freqs = spectrum.get_data(return_freqs=True, picks="all")

        psds_norm = np.zeros(psds.shape)
        psds_sum = np.sum(psds, axis=-1, keepdims=True)
        np.divide(psds, psds_sum, where=psds_sum > 0, out=psds_norm)

        X = []
        for fmin, fmax in FREQ_BANDS.values():
            psds_band = psds_norm[:, :, (freqs >= fmin) & (freqs < fmax)].mean(
                axis=-1
            )
            X.append(psds_band.reshape(len(psds), -1))

        return np.concatenate(X, axis=1)


class ToTorchDataset:
    """Build Torch dataset from a py:class:`DelayedSample` list.

    :param normalize: If True, normalized the sample

    :param pick_chan: the channel type (e.g. "eeg","eog") or name (e.g. "Fpz-Cz") whom extract the features, if None default compute
        features for all EEG channels.

    :param n_past_epochs: number of precedent epochs to include in the ListSampleDataset object (by concatenation).

    :return: :py:class:`torch.utils.data.dataset.ConcatDataset` of all samples
    """

    def __init__(
        self,
        normalize: bool = False,
        pick_chan: list[str] = None,
        n_past_epochs: int = 0,
    ):
        self.normalize = normalize

        self.pick_chan = None

        self.n_past_epochs = n_past_epochs

        if pick_chan is not None:
            self.pick_chan = chan_list_to_dict(pick_chan)

    def __call__(
        self, samples: list[DelayedSample]
    ) -> torch.utils.ConcatDataset:
        samples_list = []

        for index, sample in enumerate(samples, 1):
            logger.info(
                f"making torch dataset for sample {index} on {len(samples)} samples"
            )

            samples_list.append(
                ListSampleDataset(
                    sample, self.normalize, self.pick_chan, self.n_past_epochs
                )
            )

        return ConcatDataset(samples_list)


class ResampleEpochs:
    """Resample ``mne.Epochs`` object from a py:class:`DelayedSample` list.

    :param sampling_freq: sampling frequency to which resample

    :return: py:class:`DelayedSample` list with resampled data
    """

    def __init__(self, sampling_freq: int):
        self.sampling_freq = sampling_freq

    def __call__(self, samples: list[DelayedSample]) -> list[DelayedSample]:
        for index, sample in enumerate(samples, 1):
            logger.info(
                f"resampling for sample {index} on {len(samples)} samples"
            )

            freq_sample = sample.data["data"].info["sfreq"]

            if freq_sample != self.sampling_freq:
                logger.info(
                    f"resampled as sampling frequency was {freq_sample} and {self.sampling_freq} is needed"
                )

                sample.data["data"] = self._transform(sample.data["data"])
            else:
                logger.info(
                    f" no need of resample as sampling frequency is already {freq_sample}"
                )

        return samples

    def _transform(self, epochs: Epochs) -> Epochs:
        """To resample the epochs at a given frequency. This function takes an
        ``mne.Epochs`` object.

        :param epochs: ``mne.Epochs`` object

        :return: ``mne.Epochs`` resampled
        """

        resampled_epochs = epochs.load_data().resample(sfreq=self.sampling_freq)

        return resampled_epochs


class FeatureExtractorChambon:
    """Extract feature from a py:class:`DelayedSample` list. 26 manually chosen
    features (total power (5), relative power (5), power ratio (10), spectral
    entropy, mean, variance, skewness, kurtosis, 75% quantile.)

    This class was copied and modified from https://mne.tools/stable/auto_tutorials/clinical/60_sleep.html v1.4

    Modification: change to class, adding pick_chan attribute, management division by zero, adding computation of more features

    Reference: [Chambon-2018]_

    :param pick_chan: the channel type (e.g. "eeg","eog") or name (e.g. "Fpz-Cz") whom extract the features, if None default compute
        features for all EEG channels.

    :return: py:class:`DelayedSample` list where features have been extracted
    """

    def __init__(self, pick_chan: list[str] = None):
        self.pick_chan = None

        if pick_chan is not None:
            self.pick_chan = chan_list_to_dict(pick_chan)

    def __call__(self, samples: list[DelayedSample]) -> list[DelayedSample]:
        for index, sample in enumerate(samples, 1):
            logger.info(
                f"computing frequency decomposition for sample {index} on {len(samples)} samples"
            )

            sample.features, sample.label = (
                self._transform(sample.data["data"]),
                sample.data["data"].events[:, 2],
            )

        return samples

    def _transform(self, epochs: Epochs) -> np.ndarray:
        """EEG relative power band feature extraction. This function takes an
        ``mne.Epochs`` object and creates EEG features based on relative power
        in specific frequency bands. Also saving the labels as attribute of the
        sample while data are loaded.

        :param epochs: mne.Epochs of a sample
        :return: Transformed data of shape [n_epochs, n_channel*26] 20
            spectral features and 6 temporal
        """

        FREQ_BANDS = {
            "delta": [0.5, 4.5],
            "theta": [4.5, 8.5],
            "alpha": [8.5, 11.5],
            "sigma": [11.5, 15.5],
            "beta": [15.5, 30],
        }

        pick_chan_idx = "eeg"
        if self.pick_chan is not None:
            pick_chan_idx = mne.pick_types(info=epochs.info, **self.pick_chan)

        spectrum = epochs.compute_psd(fmin=0.5, fmax=30.0, picks=pick_chan_idx)
        psds, freqs = spectrum.get_data(return_freqs=True, picks="all")

        total_power_list = []
        # compute the total power (spectral power) of each bands in FREQ_BANDS
        for fmin, fmax in FREQ_BANDS.values():
            psds_band = psds[:, :, (freqs >= fmin) & (freqs < fmax)].mean(
                axis=-1
            )
            total_power_list.append(psds_band.reshape(len(psds), -1))
        total_power_vec = np.concatenate(total_power_list, axis=1)

        psds_norm = np.zeros(psds.shape)
        psds_sum = np.sum(psds, axis=-1, keepdims=True)
        np.divide(psds, psds_sum, where=psds_sum > 0, out=psds_norm)

        relative_power_list = []
        # compute the relative power for each bands in FREQ_BANDS (total power of the bands/total power)
        for fmin, fmax in FREQ_BANDS.values():
            psds_band = psds_norm[:, :, (freqs >= fmin) & (freqs < fmax)].mean(
                axis=-1
            )
            relative_power_list.append(psds_band.reshape(len(psds), -1))
        relative_power_vec = np.concatenate(relative_power_list, axis=1)

        ratio_power_list = []
        # ratio of power (e.g. relative power beta bands/relative power theta bands)
        # in all 10 combinations
        for index, psds_band in enumerate(relative_power_list, 1):
            for i in range(index, len(relative_power_list)):
                ratio_power = np.zeros(psds_band.shape)
                ratio_power_list.append(
                    np.divide(
                        psds_band,
                        relative_power_list[i],
                        where=relative_power_list[i] != 0,
                        out=ratio_power,
                    )
                )
        ratio_power_vec = np.concatenate(ratio_power_list, axis=1)

        # compute the spectral entropy
        log_psds_norm = np.zeros(psds_norm.shape)
        np.log(psds_norm, where=psds_norm > 0, out=log_psds_norm)
        spectral_entropy = -(1 / np.log2(psds_norm.shape[2])) * (
            psds_norm * log_psds_norm
        ).sum(axis=-1)

        del psds

        data = epochs.get_data(picks=pick_chan_idx)

        # compute 6 temporal features (mean,variance, skewness,kurtosis and 75% quantile)
        mean_vec = np.mean(data, axis=-1)
        vars_vec = np.std(data, axis=-1)

        skew_vec = scipy.stats.mstats.skew(data, axis=-1).data
        kurtosis_vec = scipy.stats.mstats.kurtosis(data, axis=-1).data

        quantile_75_vec = np.quantile(data, 0.75, axis=-1)

        del data

        feature_vector = (
            total_power_vec,
            relative_power_vec,
            ratio_power_vec,
            spectral_entropy,
            mean_vec,
            vars_vec,
            skew_vec,
            kurtosis_vec,
            quantile_75_vec,
        )

        return np.hstack(feature_vector)
