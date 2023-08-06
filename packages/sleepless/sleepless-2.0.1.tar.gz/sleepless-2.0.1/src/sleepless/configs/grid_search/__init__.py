# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from sklearn.metrics import (
    cohen_kappa_score,
    hamming_loss,
    make_scorer,
    matthews_corrcoef,
)

scorings = {
    "Accuracy score": "accuracy",
    "Balanced accuracy": "balanced_accuracy",
    "Quadratic Weighted Kappa": make_scorer(
        cohen_kappa_score, weights="quadratic"
    ),
    "Linear Weighted Kappa": make_scorer(cohen_kappa_score, weights="linear"),
    "Mcc": make_scorer(matthews_corrcoef),
    "Hamming Loss": make_scorer(hamming_loss),
}
