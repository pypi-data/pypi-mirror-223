# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Montreal Archive of Sleep Studies (MASS)

This cohort comprises polysomnograms of 200 complete nights recorded
(SS1-SS5: 97 males aged 42.9 ± 19.8 years and 103 females aged 38.3 ± 18.9 years; total sample 40.6 ± 19.4 years, age range: 18-76 years).

All recordings feature a sampling frequency of 256 Hz and an electroencephalography (EEG) montage of
4-20 channels plus standard electro-oculography (EOG), electromyography (EMG), electrocardiogra- phy (ECG) and respiratory signals.

SS1 contains 53 recording of 53 different patients

SS2 contains 29 recording of 29 different patients

SS3 contains 62 recording of 62 different patients

SS4 contains 40 recording of 40 different patients

SS5 contains 26 recording of 26 different patients

* Reference: [MASS-2014]_
* Protocol ``ss1_subset``:

  * Train split: 33 (from SS1 subset)
  * Validation split: 10 (from SS1 subset)
  * Test split: 10 (from SS1 subset)

* Protocol ``ss2_subset``:

  * Train split: 11 (from SS2 subset)
  * Validation split: 4 (from SS2 subset)
  * Test split: 4 (from SS2 subset)

* Protocol ``ss3_subset``:

  * Train split: 38 (from SS3 subset)
  * Validation split: 12 (from SS3 subset)
  * Test split: 12 (from SS3 subset)

* Protocol ``ss4_subset``:

  * Train split: 24 (from SS4 subset)
  * Validation split: 8 (from SS4 subset)
  * Test split: 8 (from SS4 subset)

* Protocol ``ss5_subset``:

  * Train split: 16 (from SS5 subset)
  * Validation split: 5 (from SS5 subset)
  * Test split: 5 (from SS5 subset)
"""
from __future__ import annotations

import importlib.resources
import logging
import os
import pathlib

from collections.abc import Mapping

import pandas as pd

from ...utils.rc import load_rc
from ..dataset import JSONDataset
from ..loader import Loader, load_annotation_raw, load_edf_raw

logger = logging.getLogger(__name__)

_root_path = load_rc().get("datadir.MASS", os.path.realpath(os.curdir))

_root_path_preprocess = load_rc().get("cachedatadir.MASS_preprocess")


class LoaderMass(Loader):
    def __init__(self, transform_parameters, csv_subset, protocol_name) -> None:
        super().__init__(transform_parameters, csv_subset, protocol_name)
        self.preproc_path = _root_path_preprocess

    def _get_metadata_from_csv(self, csv_subset) -> dict:
        """Generate an id for the patient with filepath by removing night
        number.

        MASS data

        :param filepath: file path
        :return: patient id
        """
        csv_meta = os.path.join(
            _root_path,
            "MASS_Restricted-access-descriptors-locked_C1-all-subsets_to-share.xlsx",
        )

        mapping_subset = {
            "ss1": "01-01",
            "ss2": "01-02",
            "ss3": "01-03",
            "ss4": "01-04",
            "ss5": "01-05",
        }

        column_mapper = {"Age": "age", "Sexe": "gender"}

        if pathlib.Path(csv_meta).is_file():
            df = pd.read_excel(csv_meta, header=1)

            df_subset = df[
                df.iloc[:, 0].str.startswith(
                    str(mapping_subset[csv_subset]), na=False
                )
            ]

            df_drop_empty_col = df_subset.dropna(axis=1, how="all")

            df_set_index = df_drop_empty_col.set_index(df.columns[0])

            df_rename_col = df_set_index.rename(columns=column_mapper)

            df_to_dic = df_rename_col.to_dict(orient="index")

        else:
            logger.info(
                f"The file {csv_meta} could not be access, metadata are not attached"
            )

            df_to_dic = {}

        return df_to_dic

    def _raw_data_loader(self, sample):
        infer_types = True

        preload = False

        misc = None

        # exclude ECG, load separatelly if needed, sampling frequency is different for the ECG channel
        # and it creates problems while resampling
        exclude = ["ECGI", "ECGII", "ECGIII"]

        raw_from_file = load_edf_raw(
            os.path.join(_root_path, sample["data"]),
            infer_types,
            preload,
            misc,
            exclude,
        )

        label_from_file = load_annotation_raw(
            os.path.join(_root_path, sample["label"])
        )

        return (raw_from_file, label_from_file)

    def _map_key_metadata(self, key):
        return key.split("/")[1].split(" ")[0]


_EVENT_DICT: dict[str, int] = {
    "Sleep stage W": 0,
    "Sleep stage 1": 1,
    "Sleep stage 2": 2,
    "Sleep stage 3": 3,
    "Sleep stage 4": 3,
    "Sleep stage R": 4,
    "Movement time": 0,
}


_UNFILTERED_MIXED_FP_AND_C_TO_FPZ_CZ_AND_PZ_OZ_100HZ = {
    "raw-to-epochs-params": {
        "event_id": _EVENT_DICT,
        "chunk_duration": 30.0,
        "crop_wake_time": 0.0,
    },
    "combined-chan": {
        "group": {
            "Fpz-LER": ["Fp1-LER", "Fp2-LER"],
            "submental": ["Chin1", "Chin2", "Chin3"],
        },
        "method": "mean",
    },
    "bipol-ref": {
        "Fpz-Cz": ["Fpz-LER", "Cz-LER"],
        "Pz-Oz": ["Pz-LER", "Oz-LER"],
        "horizontal": ["Left Horiz", "Right Horiz"],
    },
    "resampling": {"sfreq": 100.0},
}

_FILTERED_MIXED_FP_AND_C_TO_FPZ_CZ_AND_PZ_OZ_100HZ = {
    "raw-to-epochs-params": {
        "event_id": _EVENT_DICT,
        "chunk_duration": 30.0,
        "crop_wake_time": 0.0,
    },
    "band-filter": {"freq-range": [0.3, 30], "filter-len": 400},
    "combined-chan": {
        "group": {
            "Fpz-LER": ["Fp1-LER", "Fp2-LER"],
            "submental": ["Chin1", "Chin2", "Chin3"],
        },
        "method": "mean",
    },
    "bipol-ref": {
        "Fpz-Cz": ["Fpz-LER", "Cz-LER"],
        "Pz-Oz": ["Pz-LER", "Oz-LER"],
        "horizontal": ["Left Horiz", "Right Horiz"],
    },
    "resampling": {"sfreq": 100.0},
}

_protocols: dict[
    str,
    tuple[
        str | pathlib.Path | importlib.abc.Traversable,
        Mapping,
    ],
] = {
    "ss3-unfiltered-fpz-cz-100Hz": (
        importlib.resources.files(__name__).joinpath("ss3_subset.json"),
        _UNFILTERED_MIXED_FP_AND_C_TO_FPZ_CZ_AND_PZ_OZ_100HZ,
    ),
    "ss3-filtered-fpz-cz-100Hz": (
        importlib.resources.files(__name__).joinpath("ss3_subset.json"),
        _FILTERED_MIXED_FP_AND_C_TO_FPZ_CZ_AND_PZ_OZ_100HZ,
    ),
}

dataset = JSONDataset(
    protocols=_protocols,
    fieldnames=("data", "label"),
    loader=LoaderMass,
)
"""MASS dataset object."""
