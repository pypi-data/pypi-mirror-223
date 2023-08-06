# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Config random forest grid-search."""


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

from . import scorings

rf_param_grid = [
    {
        "n_estimators": [100, 200, 300],
        "max_depth": [4, 6, 8, 10],
        "criterion": ["gini", "entropy", "log_loss"],
        "bootstrap": [True],
        "class_weight": ["balanced", None],
    },
    {
        "n_estimators": [100, 200, 300],
        "max_depth": [4, 6, 8, 10],
        "criterion": ["gini", "entropy", "log_loss"],
        "bootstrap": [False],
        "class_weight": [None],
    },
]

grid_search = GridSearchCV(
    estimator=RandomForestClassifier(),
    param_grid=rf_param_grid,
    scoring=scorings,
    refit="Balanced accuracy",
    n_jobs=8,
    verbose=3,
)
