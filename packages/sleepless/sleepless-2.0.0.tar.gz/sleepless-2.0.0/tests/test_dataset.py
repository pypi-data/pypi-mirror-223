# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Test code for datasets."""

import numpy as np
import pytest

from sleepless.data.dataset import CSVDataset, JSONDataset
from sleepless.data.loader import Loader
from sleepless.data.sample import Sample


def _raw_data_loader(context, d):
    return Sample(
        data=[
            float(d["sepal_length"]),
            float(d["sepal_width"]),
            float(d["petal_length"]),
            float(d["petal_width"]),
            d["species"][5:],
        ],
        key=(context["subset"] + str(context["order"])),
    )


class LoaderTest(Loader):
    def __init__(self, transform_parameters, csv_subset, protocol_name) -> None:
        super().__init__(transform_parameters, csv_subset, protocol_name)

    def _raw_data_loader(context, d):
        return Sample(
            data=[
                float(d["sepal_length"]),
                float(d["sepal_width"]),
                float(d["petal_length"]),
                float(d["petal_width"]),
                d["species"][5:],
            ],
            key=(context["subset"] + str(context["order"])),
        )

    def _get_metadata_from_csv(self, csv_subset: str) -> dict:
        """Generate an id for the patient with filepath by removing night
        number.

        Work for ST and SC subset but only for EDF database.

        :param filepath: file path
        :return: patient id
        """

        return {"_id": csv_subset, "age": 45, "gender": "M"}

    def _map_key_metadata(self, key):
        return key.split("/")[1][0:6]

    def _loader(self, context, sample):
        # "context" is ignored in this case - database is homogeneous
        # we returned delayed samples to avoid loading all nights
        return _raw_data_loader(context, sample)


def test_csv_loading(datadir):
    # tests if we can build a simple CSV loader for the Iris Flower dataset
    subsets = {
        "train": str(datadir / "iris-train.csv"),
        "test": str(datadir / "iris-train.csv"),
    }

    fieldnames = (
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species",
    )

    dataset = CSVDataset(subsets, fieldnames, _raw_data_loader)
    dataset.check()

    data = dataset.subsets()

    assert len(data["train"]) == 75
    for k in data["train"]:
        for f in range(4):
            assert isinstance(k.data[f], float)
        assert isinstance(k.data[4], str)
        assert isinstance(k.key, str)

    assert len(data["test"]) == 75
    for k in data["test"]:
        for f in range(4):
            assert isinstance(k.data[f], float)
        assert isinstance(k.data[4], str)
        assert k.data[4] in ("setosa", "versicolor", "virginica")
        assert isinstance(k.key, str)


def test_json_loading(datadir):
    # tests if we can build a simple JSON loader for the Iris Flower dataset
    protocols = {"default": (str(datadir / "iris.json"), {})}

    fieldnames = (
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species",
    )

    dataset = JSONDataset(protocols, fieldnames, LoaderTest)
    dataset.check()

    data = dataset.subsets("default")

    assert len(data["train"]) == 75
    for k in data["train"]:
        for f in range(4):
            assert isinstance(k.data[f], float)
        assert isinstance(k.data[4], str)
        assert isinstance(k.key, str)

    assert len(data["test"]) == 75
    for k in data["test"]:
        for f in range(4):
            assert isinstance(k.data[f], float)
        assert isinstance(k.data[4], str)
        assert isinstance(k.key, str)


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF_preprocess")
def test_preprocessing_edf(dataset_from_json):
    from sleepless.data.EDF import LoaderEdf, _protocols

    fieldnames = ("data", "label")

    dataset_preproc = JSONDataset(_protocols, fieldnames, LoaderEdf)

    dataset = dataset_from_json
    dataset.check()

    data = dataset.subsets("unfiltered")["train"][0]

    # get SC4001E0-PSG from loaderEDF it is in test set at index 6
    data_prepro = dataset_preproc.subsets("sc-unfiltered")["test"][6]

    assert np.isclose(data.data["label"], data_prepro.data["label"]).all()
    assert np.isclose(
        data.data["data"].events, data_prepro.data["data"].events
    ).all()

    data = dataset.subsets("filtered")["train"][0]

    data_prepro = dataset_preproc.subsets("sc-filtered")["test"][6]

    assert np.isclose(data.data["label"], data_prepro.data["label"]).all()
    assert np.isclose(
        data.data["data"].events, data_prepro.data["data"].events
    ).all()

    data = dataset.subsets("crop_wake")["train"][0]

    data_prepro = dataset_preproc.subsets("sc-filtered-crop-wake")["test"][6]

    assert np.isclose(data.data["label"], data_prepro.data["label"]).all()
    assert np.isclose(
        data.data["data"].events, data_prepro.data["data"].events
    ).all()


def test_json_loading_edf(dataset_from_json):
    dataset = dataset_from_json
    dataset.check()

    data = dataset.subsets("unfiltered")

    assert len(data["train"]) == 2
    assert len(data["validation"]) == 1
    assert len(data["test"]) == 1
    assert data["test"][0].age == 33

    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    # data["test"][0].data["data"].compute_psd(picks="eeg", fmin=0.5, fmax=50.0).plot(show=False,axes=ax)
    # fig.savefig("A PATH")

    FREQ_BANDS = {"before_cut": [0, 30], "after_cut": [30, 50]}

    spectrum = (
        data["test"][0]
        .data["data"]
        .compute_psd(picks="eeg", fmin=0.5, fmax=50.0)
    )
    psds, freqs = spectrum.get_data(return_freqs=True)

    psds = np.nan_to_num(psds / np.sum(psds, axis=-1, keepdims=True))

    X = []
    for fmin, fmax in FREQ_BANDS.values():
        psds_band = psds[:, :, (freqs >= fmin) & (freqs < fmax)].mean(axis=-1)
        X.append(psds_band.mean(axis=1))

    X_unfilt = np.array(X).T

    data = dataset.subsets("filtered")

    assert len(data["train"]) == 2
    assert len(data["validation"]) == 1
    assert len(data["test"]) == 1
    assert data["test"][0].age == 33

    # fig2, ax2 = plt.subplots(1, 1, figsize=(8, 6))
    # data["test"][0].data["data"].compute_psd(picks="eeg", fmin=0.5, fmax=50.0).plot(show=False,axes=ax2)
    # fig2.savefig("A PATH")

    spectrum = (
        data["test"][0]
        .data["data"]
        .compute_psd(picks="eeg", fmin=0.5, fmax=50.0)
    )
    psds, freqs = spectrum.get_data(return_freqs=True)

    psds = np.nan_to_num(psds / np.sum(psds, axis=-1, keepdims=True))

    X = []
    for fmin, fmax in FREQ_BANDS.values():
        psds_band = psds[:, :, (freqs >= fmin) & (freqs < fmax)].mean(axis=-1)
        X.append(psds_band.mean(axis=1))

    X_filt = np.array(X).T

    assert X_filt.shape == X_unfilt.shape

    assert np.isclose(
        X_filt[:, 0].sum() / X_unfilt[:, 0].sum(), np.array([1]), 10e-2
    )

    assert not np.isclose(
        X_filt[:, 1].sum() / X_unfilt[:, 1].sum(), np.array([1]), 10e-2
    )

    data = dataset.subsets("crop_wake")

    assert len(data["train"]) == 2
    assert len(data["validation"]) == 1
    assert len(data["test"]) == 1
    assert data["test"][0].age == 33
    assert len(data["train"][0].data["data"].events) == 841
