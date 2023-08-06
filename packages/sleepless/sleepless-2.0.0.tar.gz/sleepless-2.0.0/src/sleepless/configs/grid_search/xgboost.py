# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Config xgboost grid-search."""

from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier

from . import scorings

rf_param_grid = {
    "eta": [10e-4, 10e-3, 10e-2],
    "min_child_weight": [2, 4, 6, 8, 10],
    "max_depth": [2, 4, 6, 8, 10],
    "alpha": [0, 0.5, 1],
    "subsample": [0.5, 0.75, 1],
    "colsample_bylevel": [0.5, 0.75, 1],
}

grid_search = GridSearchCV(
    estimator=XGBClassifier(
        n_estimators=1000,
        early_stopping_rounds=10,
        tree_method="gpu_hist",
    ),
    param_grid=rf_param_grid,
    scoring=scorings,
    refit="Balanced accuracy",
    n_jobs=-1,
    verbose=3,
)
