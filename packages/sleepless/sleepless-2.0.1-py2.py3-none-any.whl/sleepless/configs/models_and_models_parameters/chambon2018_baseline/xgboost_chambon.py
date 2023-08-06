# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Config xgboost grid-search.

* Reference: [Chambon-2018]_
"""

from ....data.transforms import FeatureExtractorChambon
from ...grid_search.xgboost import grid_search

model = grid_search

model_parameters = {
    "transform": [FeatureExtractorChambon(["Fpz-Cz", "Pz-Oz"])],
    "grid-search": {"seed": 42, "early_stop": True},
}
