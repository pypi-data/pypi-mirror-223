# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Cross subset protocols:

In this protocol all the raw data have been filtered with a pass band filter [0.3,30] Hz.

Train split = train split sc,

Validation split = validation split sc,

Test split = test split sc, train split st, validation split st, test split st,
"""

from .sc_filtered import dataset as sc_dataset
from .st_filtered import dataset_as_test as st_dataset

dataset = sc_dataset | st_dataset
