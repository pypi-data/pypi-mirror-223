# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Sleep-EDF (expanded) dataset for sleep analysis.

The database includes 197 all night PSGs recording in 2 subsets (SC and ST):

ST contains 44 PSG (9-hours-night) of 22 Caucasian (between  18-79 years old),
healthy (without medication) but with difficulty to fall asleep.

SC contains 153 PSG (20 hours) of 78 Caucasian (between  25-101 years old),
healthy (without medication)

* Reference: [SLEEP_EDF-2018]_

* Protocol ``st_subset``:

  * Train split: 28 (from ST subset)
  * Validation split: 8 (from ST subset)
  * Test split: 8 (from ST subset)

* Protocol ``sc_subset``:

  * Train split: 97 (from Sc subset)
  * Validation split: 28 (from SC subset)
  * Test split: 28 (from SC subset)
"""
from __future__ import annotations

import importlib.resources
import logging
import os
import pathlib

from collections.abc import Mapping

import numpy as np
import pandas as pd

from ...utils.rc import load_rc
from ..dataset import JSONDataset
from ..loader import Loader, load_annotation_raw, load_edf_raw

logger = logging.getLogger(__name__)

_root_path = load_rc().get("datadir.EDF", os.path.realpath(os.curdir))

_root_path_preprocess = load_rc().get("cachedatadir.EDF")


class LoaderEdf(Loader):
    def __init__(self, transform_parameters, csv_subset, protocol_name) -> None:
        super().__init__(transform_parameters, csv_subset, protocol_name)
        self.preproc_path = _root_path_preprocess

    def _get_metadata_from_csv(self, csv_subset: str) -> dict:
        """Generate an id for the patient with filepath by removing night
        number.

        Work for ST and SC subset but only for EDF database.

        :param filepath: file path
        :return: patient id
        """
        csv_sc = os.path.join(_root_path, "SC-subjects.xls")

        csv_st = os.path.join(_root_path, "ST-subjects.xls")

        _id = None
        age = None
        gender = None
        medication = None

        if csv_subset == "sc":
            if pathlib.Path(csv_sc).is_file():
                df = pd.read_excel(csv_sc)

                _id = df.iloc[:, 0].values.astype(str)

                night_number = df.iloc[:, 1].values

                age = df.iloc[:, 2].values

                gender = df.iloc[:, 3].values
                gender = ["F" if i == 1 else "M" for i in gender]

                medication = ["None"] * len(gender)

                key = [
                    "".join(["SC4", str(i).zfill(2), str(night_number[index])])
                    for index, i in enumerate(_id)
                ]

            else:
                logger.warning(
                    f"The file {csv_sc} could not be access, metadata are not attached"
                )

        elif csv_subset == "st":
            if pathlib.Path(csv_st).is_file():
                df = pd.read_excel(csv_st)

                _id = df.iloc[:, 0][1:].values.astype(str)
                _id = np.concatenate((_id, _id))

                age = df.iloc[:, 1][1:].values
                age = np.concatenate((age, age))

                gender = df.iloc[:, 2][1:].values
                gender = ["F" if i == 1 else "M" for i in gender]
                gender += gender

                placebo_night_number = df.iloc[:, 3][1:].values
                medicate_night_number = df.iloc[:, 5][1:].values

                medication = ["Temazepam"] * len(placebo_night_number) + [
                    "Placebo"
                ] * len(medicate_night_number)

                night_number = np.concatenate(
                    (placebo_night_number, medicate_night_number)
                )

                key = [
                    "".join(["ST7", str(i).zfill(2), str(night_number[index])])
                    for index, i in enumerate(_id)
                ]

            else:
                logger.info(
                    f"The file {csv_st} could not be access, metadata are not attached"
                )

        else:
            logger.error("Unknown id")

        attribute = ["id", "age", "gender", "medication"]

        if _id is None:
            output_dic = {}

        else:
            output_dic = {
                key[index]: dict(zip(attribute, values))
                for index, values in enumerate(
                    zip(_id, age, gender, medication)
                )
            }

        return output_dic

    def _raw_data_loader(self, sample):
        infer_types = True

        preload = False

        misc = ["Temp rectal", "Event marker", "Marker"]

        raw_from_file = load_edf_raw(
            os.path.join(_root_path, sample["data"]), infer_types, preload, misc
        )

        label_from_file = load_annotation_raw(
            os.path.join(_root_path, sample["label"])
        )

        return (raw_from_file, label_from_file)

    def _map_key_metadata(self, key):
        return key.split("/")[1][0:6]


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
    },
}

_FILTERED = {
    "raw-to-epochs-params": {
        "event_id": _EVENT_DICT,
        "chunk_duration": 30.0,
        "crop_wake_time": 0.0,
    },
    "band-filter": {"freq-range": [0.3, 30], "filter-len": 300},
}

_FILTERED_WAKE_30_MIN = {
    "raw-to-epochs-params": {
        "event_id": _EVENT_DICT,
        "chunk_duration": 30.0,
        "crop_wake_time": 30.0,
        "wake_stage_name": "Sleep stage W",
    },
    "band-filter": {"freq-range": [0.3, 30], "filter-len": 300},
}

_protocols: dict[
    str,
    tuple[
        str | pathlib.Path | importlib.abc.Traversable,
        Mapping,
    ],
] = {
    "st-unfiltered": (
        importlib.resources.files(__name__).joinpath("st_subset.json"),
        _UNFILTERED,
    ),
    "sc-unfiltered": (
        importlib.resources.files(__name__).joinpath("sc_subset.json"),
        _UNFILTERED,
    ),
    "st-filtered": (
        importlib.resources.files(__name__).joinpath("st_subset.json"),
        _FILTERED,
    ),
    "sc-filtered": (
        importlib.resources.files(__name__).joinpath("sc_subset.json"),
        _FILTERED,
    ),
    "sc-filtered-crop-wake": (
        importlib.resources.files(__name__).joinpath("sc_subset.json"),
        _FILTERED_WAKE_30_MIN,
    ),
}

dataset = JSONDataset(
    protocols=_protocols,
    fieldnames=("data", "label"),
    loader=LoaderEdf,
)
"""Sleep-EDF dataset object."""
