# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for the transform."""

import pytest

from sleepless.data.loader import load_annotation_raw, load_edf_raw
from sleepless.data.transforms import (
    EEGPowerBand,
    FeatureExtractorChambon,
    RawToEpochs,
)


def test_epochs_(datadir):
    raw = load_edf_raw(str(datadir / "SC4001E0-PSG.edf"), True, False, None)

    annot = load_annotation_raw(str(datadir / "SC4001EC-Hypnogram.edf"))

    event_dic = {
        "Sleep stage W": 0,
        "Sleep stage 1": 1,
        "Sleep stage 2": 2,
        "Sleep stage 3": 3,
        "Sleep stage 4": 3,
        "Sleep stage R": 4,
        "Movement time": 0,
    }

    kw_args_dic = {
        "event_id": event_dic,
        "chunk_duration": 30.0,
        "picks_chan": ["Fpz-Cz", "Pz-Oz"],
        "crop_wake_time": 0.0,
        "wake_stage_name": "Sleep stage W",
    }

    raw_epochs_transform = RawToEpochs(**kw_args_dic)

    epochs = raw_epochs_transform.transform(raw, annot)

    nb_channel = len(epochs.info["ch_names"])

    nb_points_time = kw_args_dic["chunk_duration"] * raw.info["sfreq"]

    nb_events = int(raw.n_times / nb_points_time)

    assert nb_events == epochs.events.shape[0]

    assert epochs.get_data().shape == (
        int(raw.n_times / nb_points_time),
        nb_channel,
        nb_points_time,
    )

    assert epochs.get_data(picks="Fpz-Cz").shape == (
        int(raw.n_times / nb_points_time),
        1,
        nb_points_time,
    )


def test_eeg_power_band(datadir):
    raw = load_edf_raw(str(datadir / "SC4001E0-PSG.edf"), True, False, None)

    annot = load_annotation_raw(str(datadir / "SC4001EC-Hypnogram.edf"))

    event_dic = {
        "Sleep stage W": 0,
        "Sleep stage 1": 1,
        "Sleep stage 2": 2,
        "Sleep stage 3": 3,
        "Sleep stage 4": 3,
        "Sleep stage R": 4,
        "Movement time": 0,
    }

    kw_args_dic = {
        "event_id": event_dic,
        "chunk_duration": 30.0,
        "picks_chan": ["Fpz-Cz", "Pz-Oz"],
        "crop_wake_time": 0.0,
        "wake_stage_name": "Sleep stage W",
    }

    raw_epochs_transform = RawToEpochs(**kw_args_dic)

    epochs = raw_epochs_transform.transform(raw, annot)

    nb_channel = len(epochs.info["ch_names"])

    nb_points_time = kw_args_dic["chunk_duration"] * raw.info["sfreq"]

    nb_events = int(raw.n_times / nb_points_time)

    transform = EEGPowerBand(["eeg"])

    features = transform._transform(epochs)

    assert features.shape == (nb_events, nb_channel * 5)


def test_feature_extractor_chambon(datadir):
    raw = load_edf_raw(str(datadir / "SC4001E0-PSG.edf"), True, False, None)

    annot = load_annotation_raw(str(datadir / "SC4001EC-Hypnogram.edf"))

    event_dic = {
        "Sleep stage W": 0,
        "Sleep stage 1": 1,
        "Sleep stage 2": 2,
        "Sleep stage 3": 3,
        "Sleep stage 4": 3,
        "Sleep stage R": 4,
        "Movement time": 0,
    }

    kw_args_dic = {
        "event_id": event_dic,
        "chunk_duration": 30.0,
        "picks_chan": ["Fpz-Cz", "Pz-Oz"],
        "crop_wake_time": 0.0,
        "wake_stage_name": "Sleep stage W",
    }

    raw_epochs_transform = RawToEpochs(**kw_args_dic)

    epochs = raw_epochs_transform.transform(raw, annot)

    nb_channel = len(epochs.info["ch_names"])

    nb_points_time = kw_args_dic["chunk_duration"] * raw.info["sfreq"]

    nb_events = int(raw.n_times / nb_points_time)

    transform = FeatureExtractorChambon(["eeg"])

    features = transform._transform(epochs)

    assert features.shape == (nb_events, nb_channel * 26)


@pytest.mark.parametrize(
    "transform_object,nb_channels, nb_features",
    [
        pytest.param(
            FeatureExtractorChambon(),
            2,
            26,
            id="chambon_no_pick",
        ),
        pytest.param(
            FeatureExtractorChambon(["eog", "emg", "Fpz-Cz"]),
            3,
            26,
            id="chambon_pick_eog_emg_fpz",
        ),
        pytest.param(
            FeatureExtractorChambon(["eeg"]),
            2,
            26,
            id="chambon_pick_eeg",
        ),
        pytest.param(
            FeatureExtractorChambon(["eog"]),
            1,
            26,
            id="chambon_pick_eog",
        ),
        pytest.param(
            EEGPowerBand(),
            2,
            5,
            id="mne_no_pick",
        ),
        pytest.param(
            EEGPowerBand(["eog", "emg", "Fpz-Cz"]),
            3,
            5,
            id="mne_pick_eog_emg_fpz",
        ),
        pytest.param(
            EEGPowerBand(["eeg"]),
            2,
            5,
            id="mne_pick_eeg",
        ),
        pytest.param(
            EEGPowerBand(["eog"]),
            1,
            5,
            id="mne_pick_eog",
        ),
    ],
)
def test_transform(transform_shape_check):
    return
