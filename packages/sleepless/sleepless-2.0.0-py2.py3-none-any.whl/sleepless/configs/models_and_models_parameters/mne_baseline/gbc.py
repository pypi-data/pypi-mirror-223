# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Config gbc grid-search.

For mne-baseline :

* Reference: [mne_baseline]_
"""
from ....data.transforms import EEGPowerBand
from ...grid_search.gbc import grid_search

model = grid_search

model_parameters = {
    "transform": [EEGPowerBand(["Fpz-Cz", "Pz-Oz"])],
    "grid-search": {"seed": 42},
}
