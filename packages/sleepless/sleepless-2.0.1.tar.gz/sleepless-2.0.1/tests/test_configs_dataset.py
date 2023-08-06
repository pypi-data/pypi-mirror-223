# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for configs dataset."""

import pytest

from .conftest import _protocol_check


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
def test_protocol_consistency_EDF_sc_unf():
    from sleepless.configs.datasets.EDF.sc_unfiltered import (
        dataset as sc_subset,
    )

    _protocol_check(sc_subset, 97, 28, 28)

    return


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
def test_protocol_consistency_EDF_sc_fil():
    from sleepless.configs.datasets.EDF.sc_filtered import dataset as sc_subset

    _protocol_check(sc_subset, 97, 28, 28)

    return


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
def test_protocol_consistency_EDF_sc_fil_crop():
    from sleepless.configs.datasets.EDF.sc_filtered_crop_wake import (
        dataset as sc_subset,
    )

    _protocol_check(sc_subset, 97, 28, 28)

    return


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
def test_protocol_consistency_EDF_st_unfil():
    from sleepless.configs.datasets.EDF.st_unfiltered import (
        dataset as st_subset,
    )

    _protocol_check(st_subset, 28, 8, 8)

    return


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
def test_protocol_consistency_EDF_st_fil():
    from sleepless.configs.datasets.EDF.st_filtered import dataset as st_subset

    _protocol_check(st_subset, 28, 8, 8)

    return


@pytest.mark.skip_if_rc_var_not_set("datadir.MASS")
def test_protocol_consistency_MASS_ss3_unf():
    from sleepless.configs.datasets.MASS.ss3_unfiltered_fpz_cz import (
        dataset as ss3_subset,
    )

    _protocol_check(ss3_subset, 38, 12, 12)

    return


@pytest.mark.skip_if_rc_var_not_set("datadir.MASS")
def test_protocol_consistency_MASS_ss3_fil():
    from sleepless.configs.datasets.MASS.ss3_filtered_fpz_cz import (
        dataset as ss3_subset,
    )

    _protocol_check(ss3_subset, 38, 12, 12)

    return


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
def test_dataset_consistency_edf_train_sc():
    from sleepless.configs.datasets.EDF.train_sc_filtered import (
        dataset as edf_sc,
    )

    keys = edf_sc.keys()

    assert len(keys) == 6

    assert "train" in keys
    assert len(edf_sc["train"]) == 97

    assert "validation" in keys
    assert len(edf_sc["validation"]) == 28

    assert "test" in keys
    assert len(edf_sc["test"]) == 28

    assert "edf_st_train" in keys
    assert len(edf_sc["edf_st_train"]) == 28

    assert "edf_st_validation" in keys
    assert len(edf_sc["edf_st_validation"]) == 8

    assert "edf_st_test" in keys
    assert len(edf_sc["edf_st_test"]) == 8


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
def test_dataset_consistency_edf_train_st():
    from sleepless.configs.datasets.EDF.train_st_filtered import (
        dataset as edf_st,
    )

    keys = edf_st.keys()

    assert len(keys) == 6

    assert "train" in keys
    assert len(edf_st["train"]) == 28

    assert "validation" in keys
    assert len(edf_st["validation"]) == 8

    assert "test" in keys
    assert len(edf_st["test"]) == 8

    assert "edf_sc_train" in keys
    assert len(edf_st["edf_sc_train"]) == 97

    assert "edf_sc_validation" in keys
    assert len(edf_st["edf_sc_validation"]) == 28

    assert "edf_sc_test" in keys
    assert len(edf_st["edf_sc_test"]) == 28


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
def test_dataset_consistency_edf_train_sc_st():
    from sleepless.configs.datasets.EDF.train_st_sc_filtered import (
        dataset as edf_st_sc,
    )

    keys = edf_st_sc.keys()

    assert len(keys) == 4

    assert "train" in keys
    assert len(edf_st_sc["train"]) == 97 + 28

    assert "validation" in keys
    assert len(edf_st_sc["validation"]) == 8 + 28

    assert "edf_st_test" in keys
    assert len(edf_st_sc["edf_st_test"]) == 8

    assert "edf_sc_test" in keys
    assert len(edf_st_sc["edf_sc_test"]) == 28


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
@pytest.mark.skip_if_rc_var_not_set("datadir.MASS")
def test_dataset_consistency_edf_mass_train_edf_sc():
    from sleepless.configs.datasets.EDF_X_MASS.train_edf_sc import (
        dataset as train_edf_sc,
    )

    keys = train_edf_sc.keys()

    assert len(keys) == 12

    assert "train" in keys
    assert len(train_edf_sc["train"]) == 97

    assert "validation" in keys
    assert len(train_edf_sc["validation"]) == 28

    assert "test" in keys
    assert len(train_edf_sc["test"]) == 28

    assert "mass_ss3_train" in keys
    assert len(train_edf_sc["mass_ss3_train"]) == 38

    assert "mass_ss3_validation" in keys
    assert len(train_edf_sc["mass_ss3_validation"]) == 12

    assert "mass_ss3_test" in keys
    assert len(train_edf_sc["mass_ss3_test"]) == 12

    assert "edf_st_train" in keys
    assert len(train_edf_sc["edf_st_train"]) == 28

    assert "edf_st_validation" in keys
    assert len(train_edf_sc["edf_st_validation"]) == 8

    assert "edf_st_test" in keys
    assert len(train_edf_sc["edf_st_test"]) == 8

    assert "edf_sc_crop_train" in keys
    assert len(train_edf_sc["edf_sc_crop_train"]) == 97

    assert "edf_sc_crop_validation" in keys
    assert len(train_edf_sc["edf_sc_crop_validation"]) == 28

    assert "edf_sc_crop_test" in keys
    assert len(train_edf_sc["edf_sc_crop_test"]) == 28


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
@pytest.mark.skip_if_rc_var_not_set("datadir.MASS")
def test_dataset_consistency_edf_mass_train_edf_st():
    from sleepless.configs.datasets.EDF_X_MASS.train_edf_st import (
        dataset as train_edf_st,
    )

    keys = train_edf_st.keys()

    assert len(keys) == 9

    assert "train" in keys
    assert len(train_edf_st["train"]) == 28

    assert "validation" in keys
    assert len(train_edf_st["validation"]) == 8

    assert "test" in keys
    assert len(train_edf_st["test"]) == 8

    assert "mass_ss3_train" in keys
    assert len(train_edf_st["mass_ss3_train"]) == 38

    assert "mass_ss3_validation" in keys
    assert len(train_edf_st["mass_ss3_validation"]) == 12

    assert "mass_ss3_test" in keys
    assert len(train_edf_st["mass_ss3_test"]) == 12

    assert "edf_sc_train" in keys
    assert len(train_edf_st["edf_sc_train"]) == 97

    assert "edf_sc_validation" in keys
    assert len(train_edf_st["edf_sc_validation"]) == 28

    assert "edf_sc_test" in keys
    assert len(train_edf_st["edf_sc_test"]) == 28


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
@pytest.mark.skip_if_rc_var_not_set("datadir.MASS")
def test_dataset_consistency_edf_mass_train_mass_ss3():
    from sleepless.configs.datasets.EDF_X_MASS.train_mass_ss3 import (
        dataset as train_mass_ss3,
    )

    keys = train_mass_ss3.keys()

    assert len(keys) == 9

    assert "train" in keys
    assert len(train_mass_ss3["train"]) == 38

    assert "validation" in keys
    assert len(train_mass_ss3["validation"]) == 12

    assert "test" in keys
    assert len(train_mass_ss3["test"]) == 12

    assert "edf_sc_train" in keys
    assert len(train_mass_ss3["edf_sc_train"]) == 97

    assert "edf_sc_validation" in keys
    assert len(train_mass_ss3["edf_sc_validation"]) == 28

    assert "edf_sc_test" in keys
    assert len(train_mass_ss3["edf_sc_test"]) == 28

    assert "edf_st_train" in keys
    assert len(train_mass_ss3["edf_st_train"]) == 28

    assert "edf_st_validation" in keys
    assert len(train_mass_ss3["edf_st_validation"]) == 8

    assert "edf_st_test" in keys
    assert len(train_mass_ss3["edf_st_test"]) == 8


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
@pytest.mark.skip_if_rc_var_not_set("datadir.MASS")
def test_dataset_consistency_edf_mass_train_edf_sc_crop():
    from sleepless.configs.datasets.EDF_X_MASS.train_edf_sc_crop_wake import (
        dataset as train_edf_sc_cropped,
    )

    keys = train_edf_sc_cropped.keys()

    assert len(keys) == 9

    assert "train" in keys
    assert len(train_edf_sc_cropped["train"]) == 97

    assert "validation" in keys
    assert len(train_edf_sc_cropped["validation"]) == 28

    assert "test" in keys
    assert len(train_edf_sc_cropped["test"]) == 28

    assert "edf_st_train" in keys
    assert len(train_edf_sc_cropped["edf_st_train"]) == 28

    assert "edf_st_validation" in keys
    assert len(train_edf_sc_cropped["edf_st_validation"]) == 8

    assert "edf_st_test" in keys
    assert len(train_edf_sc_cropped["edf_st_test"]) == 8

    assert "mass_ss3_train" in keys
    assert len(train_edf_sc_cropped["mass_ss3_train"]) == 38

    assert "mass_ss3_validation" in keys
    assert len(train_edf_sc_cropped["mass_ss3_validation"]) == 12

    assert "mass_ss3_test" in keys
    assert len(train_edf_sc_cropped["mass_ss3_test"]) == 12


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
@pytest.mark.skip_if_rc_var_not_set("datadir.MASS")
def test_dataset_consistency_edf_mass_train_edf_st_sc():
    from sleepless.configs.datasets.EDF_X_MASS.train_edf_st_sc import (
        dataset as train_edf_st_sc,
    )

    keys = train_edf_st_sc.keys()

    assert len(keys) == 10

    assert "train" in keys
    assert len(train_edf_st_sc["train"]) == 28 + 97

    assert "validation" in keys
    assert len(train_edf_st_sc["validation"]) == 8 + 28

    assert "edf_st_test" in keys
    assert len(train_edf_st_sc["edf_st_test"]) == 8

    assert "edf_sc_test" in keys
    assert len(train_edf_st_sc["edf_sc_test"]) == 28

    assert "mass_ss3_train" in keys
    assert len(train_edf_st_sc["mass_ss3_train"]) == 38

    assert "mass_ss3_validation" in keys
    assert len(train_edf_st_sc["mass_ss3_validation"]) == 12

    assert "mass_ss3_test" in keys
    assert len(train_edf_st_sc["mass_ss3_test"]) == 12


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
@pytest.mark.skip_if_rc_var_not_set("datadir.MASS")
def test_dataset_consistency_mixed_all_db():
    from sleepless.configs.datasets.mixed_all_db.mixed_all_db import (
        dataset as mixed_all_db,
    )

    keys = mixed_all_db.keys()

    assert len(keys) == 5

    assert "train" in keys
    assert len(mixed_all_db["train"]) == 28 + 97 + 38

    assert "validation" in keys
    assert len(mixed_all_db["validation"]) == 8 + 28 + 12

    assert "edf_st_test" in keys
    assert len(mixed_all_db["edf_st_test"]) == 8

    assert "edf_sc_test" in keys
    assert len(mixed_all_db["edf_sc_test"]) == 28

    assert "mass_ss3_test" in keys
    assert len(mixed_all_db["mass_ss3_test"]) == 12
