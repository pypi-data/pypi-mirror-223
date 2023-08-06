# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Config random forest grid-search.

For chambon-baseline :

* Reference: [Chambon-2018]_
"""


from ....data.transforms import FeatureExtractorChambon
from ...grid_search.randomforest import grid_search

model = grid_search

model_parameters = {
    "transform": [FeatureExtractorChambon(["submental"])],
    "grid-search": {"seed": 42},
}
