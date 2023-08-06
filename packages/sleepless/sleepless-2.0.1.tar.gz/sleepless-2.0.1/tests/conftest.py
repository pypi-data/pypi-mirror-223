# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import copy
import os
import pathlib

import numpy as np
import pytest

from sleepless.data.sample import Sample
from sleepless.data.transforms import EEGPowerBand, RawToEpochs


@pytest.fixture
def datadir(request) -> pathlib.Path:
    """Returns the directory in which the test is sitting."""
    return pathlib.Path(request.module.__file__).parents[0] / "data"


def pytest_configure(config):
    """This function is run once for pytest setup."""
    config.addinivalue_line(
        "markers",
        "skip_if_rc_var_not_set(name): this mark skips the test if a certain "
        "~/.config/sleepless.toml variable is not set",
    )

    config.addinivalue_line("markers", "slow: this mark indicates slow tests")


def pytest_runtest_setup(item):
    """This function is run for every test candidate in this directory.

    The test is run if this function returns ``None``.  To skip a test,
    call ``pytest.skip()``, specifying a reason.
    """
    from sleepless.utils.rc import load_rc

    rc = load_rc()

    # iterates over all markers for the item being examined, get the first
    # argument and accumulate these names
    rc_names = [
        mark.args[0]
        for mark in item.iter_markers(name="skip_if_rc_var_not_set")
    ]

    # checks all names mentioned are set in ~/.config/sleepless.toml, otherwise,
    # skip the test
    if rc_names:
        missing = [k for k in rc_names if rc.get(k) is None]
        if any(missing):
            pytest.skip(
                f"Test skipped because {', '.join(missing)} is **not** "
                f"set in ~/.config/sleepless.toml"
            )


def rc_variable_set(name):
    from sleepless.utils.rc import load_rc

    rc = load_rc()
    pytest.mark.skipif(
        name not in rc,
        reason=f"RC variable '{name}' is not set",
    )


@pytest.fixture(scope="session")
def sample() -> Sample:
    from sleepless.data.loader import load_annotation_raw, load_edf_raw

    datadir = pathlib.Path(__file__).parents[0] / "data"

    data_ = load_edf_raw(str(datadir / "SC4001E0-PSG.edf"), True, False)

    label_ = load_annotation_raw(str(datadir / "SC4001EC-Hypnogram.edf"))

    return Sample(
        data=dict(data=data_, label=label_),
        gender=1,
        age=10,
        key=os.path.splitext("SC4001E0-PSG.edf")[0],
    )


@pytest.fixture(scope="session")
def dataset_test(sample):
    sample_train = Sample(
        data=dict(data=sample.data["data"], label=sample.data["label"]),
        parent=sample,
    )
    sample_test = sample
    return {"train": [sample_train], "test": [sample_test]}


@pytest.fixture(scope="session")
def transform_dataset_1sample(dataset_test):
    from sleepless.data.utils import ComposeTransform

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

    class EpochsToData:
        def __call__(self, samples):
            for index, sample in enumerate(samples, 1):
                sample.data["data"] = sample.epochs

            return samples

    transformer1 = RawToEpochs(**kw_args_dic)

    transformer2 = EpochsToData()

    transformer3 = EEGPowerBand(["eeg"])

    compose_transform = ComposeTransform(
        [transformer1, transformer2, transformer3]
    )

    dataset_test["train"] = compose_transform(dataset_test["train"])

    dataset_test["test"] = compose_transform(dataset_test["test"])

    return dataset_test


@pytest.fixture(scope="session")
def transform_dataset_5samples(transform_dataset_1sample):
    list_train = []

    list_test = []

    sample_transformed = transform_dataset_1sample["train"][0]

    for index, assing_age in enumerate([10, 20, 70, 90, 100]):
        list_train.append(copy.copy(sample_transformed))

        list_train[index].key = list_train[index].key + str(assing_age)

        list_train[index].age = assing_age

        list_train[index].gender = 1

        list_test.append(copy.copy(sample_transformed))

        list_test[index].key = list_test[index].key + str(assing_age)

        list_test[index].age = assing_age

        list_test[index].gender = 2

    return {"train": list_train, "test": list_test}


@pytest.fixture(scope="session")
def dataset_from_json():
    datadir = pathlib.Path(__file__).parents[0] / "data"

    from sleepless.data.dataset import JSONDataset
    from sleepless.data.loader import Loader, load_annotation_raw, load_edf_raw

    class LoaderTestEdf(Loader):
        def __init__(
            self, transform_parameters, csv_subset, protocol_name
        ) -> None:
            super().__init__(transform_parameters, csv_subset, protocol_name)
            self._root_path = pathlib.Path(__file__).parents[0] / "data"

        def _get_metadata_from_csv(self, csv_subset: str) -> dict:
            return {"SC4001": {"id": csv_subset, "age": 33, "gender": "M"}}

        def _raw_data_loader(self, sample):
            infer_types = True

            preload = False

            misc = ["Temp rectal", "Event marker"]

            raw_from_file = load_edf_raw(
                os.path.join(self._root_path, sample["data"]),
                infer_types,
                preload,
                misc,
            )

            label_from_file = load_annotation_raw(
                os.path.join(self._root_path, sample["label"])
            )

            return (raw_from_file, label_from_file)

        def _map_key_metadata(self, key):
            return key.split("/")[0][0:6]

    _EVENT_DICT: dict[str, int] = {
        "Sleep stage W": 0,
        "Sleep stage 1": 1,
        "Sleep stage 2": 2,
        "Sleep stage 3": 3,
        "Sleep stage 4": 3,
        "Sleep stage R": 4,
        "Movement time": 0,
    }
    _UNFILTERED = {
        "raw-to-epochs-params": {
            "event_id": _EVENT_DICT,
            "chunk_duration": 30.0,
            "crop_wake_time": 0.0,
        }
    }
    _FILTERED = {
        "raw-to-epochs-params": {
            "event_id": _EVENT_DICT,
            "chunk_duration": 30.0,
            "crop_wake_time": 0.0,
        },
        "band-filter": {"freq-range": [0.3, 30], "filter-len": 300},
    }

    _CROP_WAKE = {
        "raw-to-epochs-params": {
            "event_id": _EVENT_DICT,
            "chunk_duration": 30.0,
            "crop_wake_time": 30.0,
            "wake_stage_name": "Sleep stage W",
        },
    }

    protocols = {
        "filtered": (str(datadir / "sleep.json"), _FILTERED),
        "unfiltered": (
            str(datadir / "sleep.json"),
            _UNFILTERED,
        ),
        "crop_wake": (str(datadir / "sleep.json"), _CROP_WAKE),
    }

    fieldnames = ("data", "label")

    dataset = JSONDataset(protocols, fieldnames, LoaderTestEdf)

    return dataset


@pytest.fixture(scope="session")
def dataset_for_torch(dataset_from_json):
    from sleepless.data.transforms import ToTorchDataset
    from sleepless.data.utils import ComposeTransform

    dataset = dataset_from_json.subsets("unfiltered")

    class changeKeyName:
        def __call__(self, samples):
            for index, sample in enumerate(samples, 1):
                sample.key = sample.key + str(index)

            return samples

    compose_transform = ComposeTransform(
        [
            changeKeyName(),
            ToTorchDataset(normalize=True, pick_chan=["Fpz-Cz", "Pz-Oz"]),
        ]
    )

    dataset_transformed = {k: compose_transform(v) for k, v in dataset.items()}

    return dataset, dataset_transformed


@pytest.fixture
def protocol_checking(
    subset,
    len_train,
    len_validation,
    len_test,
):
    assert _protocol_check(subset, len_train, len_validation, len_test)

    return


def _protocol_check(
    subset,
    len_train,
    len_validation,
    len_test,
):
    assert len(subset) == 3

    assert "train" in subset
    assert len(subset["train"]) == len_train

    assert "validation" in subset
    assert len(subset["validation"]) == len_validation

    assert "test" in subset
    assert len(subset["test"]) == len_test

    return True


@pytest.fixture
def protocol_consistency(
    dataset,
    subset_name,
    len_train,
    len_validation,
    len_test,
    check_file_name,
):
    subset = dataset.subsets(str(subset_name))

    assert _protocol_check(subset, len_train, len_validation, len_test)

    list_key = []

    for key in subset.keys():
        for s in subset[key]:
            assert s.key.startswith(check_file_name)

            list_key.append(s.key)

            test_unique = np.unique(list_key)

    assert len(test_unique) == len_train + len_validation + len_test

    return


@pytest.fixture
def protocol_loading(dataset, subset_name, year, nb_channel, dic_meta):
    def _check_sample(s):
        data = s.data
        assert isinstance(data, dict)
        assert len(data) == 2

        assert "data" in data
        assert len(data["data"].info["ch_names"]) in nb_channel
        assert data["data"].info["meas_date"].year in year

        assert "label" in data

        for k, v in dic_meta.items():
            assert isinstance(getattr(s, k), v)

        # to visualize signals with annotation, uncomment the folowing code
        # from ..data.utils import plot_PSG_and_annotation
        # display = plot_PSG_and_annotation(data["data"], data["label"])
        # import matplotlib.pyplot; matplotlib.pyplot.show()
        # import ipdb; ipdb.set_trace()
        # to save the figure in pdf uncomment the following code
        # display.savefig("test/fig.pdf")

        return

    subset = dataset.subsets(str(subset_name))

    limit = 1  # use this to limit testing to first images only

    for s in subset["train"][:limit]:
        _check_sample(s)


@pytest.fixture
def transform_shape_check(
    dataset_from_json, transform_object, nb_channels, nb_features
):
    def _check_sample(s_transform):
        features = s_transform.features
        label = s_transform.label
        assert len(label) == len(features)
        assert features.shape[1] == nb_channels * nb_features

    from sleepless.data.utils import ComposeTransform

    dataset = dataset_from_json.subsets("unfiltered")

    compose_transform = ComposeTransform(
        [
            transform_object,
        ]
    )

    dataset_transformed = {"train": compose_transform(dataset["train"])}

    limit = 1

    for s in dataset_transformed["train"][:limit]:
        _check_sample(s)

    return
