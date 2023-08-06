# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Cross dataset protocols:

In this protocol all the raw data have been filtered with a pass band filter [0.3,30] Hz.

Train split = train split edf_sc, train split edf_st, train split mass_ss3

Validation split = validation split edf_sc, validation split edf_st, validation split mass_ss3

Test split = test split edf_sc, test split edf_st, test split mass_SS3
"""

from ..EDF.sc_filtered import dataset as sc_dataset
from ..EDF.st_filtered import dataset as st_dataset
from ..MASS.ss3_filtered_fpz_cz import dataset as ss3_dataset

dataset = {
    "train": sc_dataset["train"] + st_dataset["train"] + ss3_dataset["train"],
    "validation": sc_dataset["validation"]
    + st_dataset["validation"]
    + ss3_dataset["validation"],
    "edf_sc_test": sc_dataset["test"],
    "mass_ss3_test": ss3_dataset["test"],
    "edf_st_test": st_dataset["test"],
}
