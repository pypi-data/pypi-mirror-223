# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Training script."""

from __future__ import annotations

import logging
import typing

from collections.abc import Mapping
from datetime import datetime

import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import PredefinedSplit

from ..data.sample import DelayedSample
from ..utils.utils_fig_table_df import make_rst_tabulate, save_tables

logger = logging.getLogger(__name__)


def train_scikit(
    model: typing.Any,
    training_set: list[DelayedSample],
    validation_set: list[list[DelayedSample]],
    output_folder: str,
    model_parameters: Mapping,
) -> None:
    """Train script for the scikit-learn pipeline.

    :param model: The scikit learn model to be fit
    :param training_set: the training_set which need to already be
        transformed.
    :param validation_set: a list of validation_set which need to
        already be transformed.
    :param output_folder: A path where the training model will be saved
    :param model_parameters: The parameters to train the model
    """

    if "early_stop" in model_parameters:
        early_stop = model_parameters["early_stop"]

    else:
        early_stop = False

    get_np_data_train = np.array(
        [
            np.array(
                (sample.features, sample.label[np.newaxis, :]), dtype=object
            )
            for sample in training_set
        ],
    )

    X_train, y_train = np.concatenate(get_np_data_train[:, 0]), np.concatenate(
        get_np_data_train[:, 1], axis=1
    )

    if ("grid-search" in model_parameters) or early_stop:
        get_np_data_valid_list = [
            np.array(
                [
                    np.array(
                        (sample.features, sample.label[np.newaxis, :]),
                        dtype=object,
                    )
                    for sample in valid_transf
                ]
            )
            for valid_transf in validation_set
        ]

        list_valid = [
            (
                np.concatenate(get_np_data_valid[:, 0]),
                np.concatenate(get_np_data_valid[:, 1], axis=1),
            )
            for get_np_data_valid in get_np_data_valid_list
        ]

        eval_set = [(X_train, y_train)] + list_valid

    if "grid-search" in model_parameters:
        fit_model = train_scikit_grid_search(
            model,
            eval_set,
            output_folder,
            **model_parameters["grid-search"],
        )

    elif early_stop:
        logger.info("early stop option activated")

        fit_model = model.fit(
            X_train,
            y_train.ravel(),
            eval_set=eval_set,
        )

    else:
        fit_model = model.fit(X_train, y_train.ravel())

    joblib.dump(fit_model, output_folder + "/fit_model")

    return


def train_scikit_grid_search(
    grid_search: typing.Any,
    eval_set: list[tuple[np.ndarray, np.ndarray]],
    output_folder: str,
    seed: int = 42,
    early_stop: bool = False,
):
    """Train function to train a grid-search with or without early-stop.

    :param grid_search: The grid search model

    :param eval_set: A list of set of shape [(X_train,y_train),(X_val0,y_val0),(X_val1,y_val1),...]

    :param output_folder: A path where the parameters of the grid-search model will be saved

    :param seed: To fix random_seed parameter

    :param early_stop: activate or not the early stop

    :return: The best estimator found by the grid-search
    """

    grid_search.estimator.random_state = seed

    X_y_train_valid = np.array(eval_set, dtype=object)

    test_fold = np.concatenate(
        [
            np.full(len(arr[1][0]), index)
            for index, arr in enumerate(eval_set, -1)
        ]
    )

    ps = PredefinedSplit(test_fold=test_fold)
    grid_search.cv = ps

    X_train_valid, y_train_valid = (
        np.concatenate(X_y_train_valid[:, 0]),
        np.concatenate(X_y_train_valid[:, 1], axis=1).ravel(),
    )

    logger.info("Start training")

    if not early_stop:
        fit_gs = grid_search.fit(X_train_valid, y_train_valid)

    else:
        fit_gs = grid_search.fit(
            X_train_valid,
            y_train_valid,
            eval_set=eval_set,
        )

    df = pd.DataFrame.from_dict(fit_gs.cv_results_, orient="index")

    df.to_csv(
        output_folder
        + "/grid_search_results"
        + "_"
        + datetime.now().strftime("%Y%m%d-%H%M%S")
        + ".csv"
    )

    save_tables(
        out_path=output_folder,
        tables=[
            make_rst_tabulate(output_folder.split("/")[-1] + "/fit_gs", df)
        ],
        name="Grid_search_result_table",
    )

    logger.info(fit_gs.best_params_)

    return fit_gs.best_estimator_
