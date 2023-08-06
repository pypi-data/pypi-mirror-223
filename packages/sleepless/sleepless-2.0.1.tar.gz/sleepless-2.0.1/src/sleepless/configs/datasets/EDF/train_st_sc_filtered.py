# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Cross subset protocols:

In this protocol all the raw data have been filtered with a pass band filter [0.3,30] Hz.

Train split = train split st + train split sc,

Validation split = validation split st, validation split sc,

Test split = test split st, test split sc
"""

from .sc_filtered import dataset as sc_dataset
from .st_filtered import dataset as st_dataset

dataset = {
    "train": st_dataset["train"] + sc_dataset["train"],
    "validation": st_dataset["validation"] + sc_dataset["validation"],
    "edf_st_test": st_dataset["test"],
    "edf_sc_test": sc_dataset["test"],
}
