# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Cross dataset protocols:

In this protocol all the raw data have been filtered with a pass band filter [0.3,30] Hz.

Train split = train split mass_ss3,

Validation split = validation split mass_ss3

Test split = test split mass_ss3, train split edf_sc, validation split edf_sc, test split edf_sc,
             train split edf_st, validation split edf_st, test split edf_st,
"""

from ..EDF.sc_filtered import dataset_as_test as sc_dataset
from ..EDF.st_filtered import dataset_as_test as st_dataset
from ..MASS.ss3_filtered_fpz_cz import dataset as ss3_dataset

dataset = ss3_dataset | sc_dataset | st_dataset
