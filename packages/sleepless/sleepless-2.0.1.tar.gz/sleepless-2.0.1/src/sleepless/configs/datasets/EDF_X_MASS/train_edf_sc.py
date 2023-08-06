# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Cross dataset protocols:

In this protocol all the raw data have been filtered with a pass band filter [0.3,30] Hz.

Train split = train split edf_sc,

Validation split = validation split edf_sc

Test split = test split edf_sc, train split mass_ss3, validation split mass_ss3, test split mass_SS3,
             train split edf_st, validation split edf_st, test split edf_st,
             train split edf_sc_cropped, validation split edf_sc_cropped, test split edf_sc_cropped
"""

from ..EDF.sc_filtered import dataset as sc_dataset
from ..EDF.sc_filtered_crop_wake import dataset_as_test as sc_dataset_crop
from ..EDF.st_filtered import dataset_as_test as st_dataset
from ..MASS.ss3_filtered_fpz_cz import dataset_as_test as ss3_dataset

dataset = sc_dataset | st_dataset | ss3_dataset | sc_dataset_crop
