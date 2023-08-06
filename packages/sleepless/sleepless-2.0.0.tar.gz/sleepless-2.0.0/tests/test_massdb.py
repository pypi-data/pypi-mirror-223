# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for MASS dataset."""


import pytest

from sleepless.data.MASS import dataset


@pytest.mark.parametrize(
    "dataset,subset_name,len_train,len_validation,len_test,check_file_name",
    [
        pytest.param(
            dataset,
            "ss3-unfiltered-fpz-cz-100Hz",
            38,
            12,
            12,
            "Biosignals_SS3",
            id="ss3_subset_unfil_fpz_cz",
        ),
        pytest.param(
            dataset,
            "ss3-filtered-fpz-cz-100Hz",
            38,
            12,
            12,
            "Biosignals_SS3",
            id="ss3_subset_fil_fpz_cz",
        ),
    ],
)
def test_protocol_consistency(protocol_consistency):
    return


dic_meta_ss3 = {
    "age": float,
    "BMI": float,
    "gender": str,
    "Notch filter": str,
    "Reference": str,
    "Type": str,
    "Scorers ID": float,
    "Scoring Rules": str,
    "Page duration": float,
}


@pytest.mark.skip_if_rc_var_not_set("datadir.MASS")
@pytest.mark.parametrize(
    "dataset,subset_name, year,nb_channel,dic_meta",
    [
        pytest.param(
            dataset,
            "ss3-unfiltered-fpz-cz-100Hz",
            [2000],
            [25],
            dic_meta_ss3,
            id="ss3_subset_unfil",
        ),
    ],
)
def test_loading(protocol_loading):
    return
