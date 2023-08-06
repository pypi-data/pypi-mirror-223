# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Cross subset protocols:

In this protocol all the raw data have been filtered with a pass band filter [0.3,30] Hz.

Train split = train split st,

Validation split = validation split st,

Test split = test split st, train split sc, validation split sc, test split sc,
"""

from .sc_filtered import dataset_as_test as sc_dataset
from .st_filtered import dataset as st_dataset

dataset = st_dataset | sc_dataset
