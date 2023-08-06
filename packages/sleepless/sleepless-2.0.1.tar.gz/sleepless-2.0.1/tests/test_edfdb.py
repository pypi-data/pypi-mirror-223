# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for Sleep-EDF (expanded) dataset."""

import numpy as np
import pytest

from sleepless.data.EDF import dataset


@pytest.mark.parametrize(
    "dataset,subset_name,len_train,len_validation,len_test,check_file_name",
    [
        pytest.param(
            dataset,
            "st-unfiltered",
            28,
            8,
            8,
            "sleep-telemetry",
            id="st_subset_unfil",
        ),
        pytest.param(
            dataset,
            "sc-unfiltered",
            97,
            28,
            28,
            "sleep-cassette",
            id="sc_subset_unfil",
        ),
        pytest.param(
            dataset,
            "st-filtered",
            28,
            8,
            8,
            "sleep-telemetry",
            id="st_subset_fil",
        ),
        pytest.param(
            dataset,
            "sc-filtered",
            97,
            28,
            28,
            "sleep-cassette",
            id="sc_subset_fil",
        ),
    ],
)
def test_protocol_consistency(protocol_consistency):
    return


dic_meta = {
    "id": (str, np.str_),
    "age": (int, np.int_),
    "gender": str,
    "medication": str,
}


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
@pytest.mark.parametrize(
    "dataset,subset_name, year,nb_channel,dic_meta",
    [
        pytest.param(
            dataset,
            "st-unfiltered",
            [1994],
            [5],
            dic_meta,
            id="st_subset_unfil",
        ),
        pytest.param(
            dataset,
            "sc-unfiltered",
            [1989, 1990, 1991],
            [7],
            dic_meta,
            id="sc_subset_unfil",
        ),
        pytest.param(
            dataset,
            "st-filtered",
            [1994],
            [5],
            dic_meta,
            id="st_subset_fil",
        ),
    ],
)
def test_loading(protocol_loading):
    return


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
def test_check():
    assert dataset.check(1) == 0
