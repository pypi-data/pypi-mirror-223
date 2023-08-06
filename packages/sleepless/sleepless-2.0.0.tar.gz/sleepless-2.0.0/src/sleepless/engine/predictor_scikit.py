# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Predcition script."""

from __future__ import annotations

import logging
import os

from collections.abc import Mapping

import numpy as np

from ..data.sample import DelayedSample
from ..data.utils import ComposeTransform
from .utils import save_hdf5

logger = logging.getLogger(__name__)


def predict_scikit(
    dataset: dict[str, list[DelayedSample]],
    model: object,
    output_folder: str,
    model_parameters: Mapping,
):
    """Compute the class probabilities prediction (or prediction if predict
    probabilities is not possible) for a set of data, given a fitted model. The
    prediction are computed for all samples of all keys.

    :param dataset: A dictionary containing a list of DelayedSample.

    :param model: A scikit learn model already fitted.

    :param output_folder: A path where prediction will be saved

    :param model_parameters: a dictionary where the following key need to be defined,
        ``transform``: list (if data are not transformed yet)
    """

    if "transform" in model_parameters:
        compose_transform = ComposeTransform(model_parameters["transform"])

    for k, v in dataset.items():
        if not (hasattr(v[0], "features")):
            v = compose_transform(v)

        for sample in v:
            if hasattr(model, "predict_proba"):
                output_prob = model.predict_proba(sample.features)

            elif hasattr(model, "predict"):
                output_prob = model.predict(sample.features)[:, None]

            else:
                logger.error("Model can not predict")

            output_folder_pred = os.path.join(output_folder, k)

            save_hdf5(
                sample.key,
                output_prob,
                sample.label,
                np.arange(0, len(sample.label)),
                output_folder_pred,
                sample.features,
            )

    return
