# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Sleep-EDF (expanded) dataset for sleep analysis.

Small dataset for testing purpose
"""

from .st_filtered import dataset as st_dataset

dataset = {
    "train": st_dataset["train"][0:4],
    "validation": st_dataset["validation"][0:2],
    "test": st_dataset["test"][0:2],
}
