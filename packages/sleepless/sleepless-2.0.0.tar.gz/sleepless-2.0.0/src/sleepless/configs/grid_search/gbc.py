# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Config sk-learn gradient-boosting grid-search."""

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV

from . import scorings

rf_param_grid = {
    "learning_rate": [10e-4, 10e-3, 10e-2],
    "min_impurity_decrease": [2, 4, 6, 8, 10],
    "max_depth": [2, 4, 6, 8, 10],
    "subsample": [0.5, 0.75, 1],
}

grid_search = GridSearchCV(
    estimator=GradientBoostingClassifier(
        n_estimators=1000,
        n_iter_no_change=10,
    ),
    param_grid=rf_param_grid,
    scoring=scorings,
    refit="Balanced accuracy",
    n_jobs=-1,
    verbose=3,
)
