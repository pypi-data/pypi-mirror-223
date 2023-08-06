# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

import click
import torch.nn as nn

from clapper.click import ConfigCommand, ResourceOption, verbosity_option
from clapper.logging import setup

logger = setup(__name__.split(".")[0], format="%(levelname)s: %(message)s")


@click.command(
    entry_point_group="sleepless.config",
    cls=ConfigCommand,
    epilog="""Examples:

\b
    1. Compute prediction of ST_subset (from EDF database) based on a pre-trained model:

       .. code:: sh

          sleepless predict stedf-filtered -w /path/to/trained_model -o "/path/to/output_folder"

""",
)
@click.option(
    "--output-folder",
    "-o",
    help="Path where to store the predictions (created if does not exist)",
    required=True,
    default="results",
    cls=ResourceOption,
    type=click.Path(),
)
@click.option(
    "--dataset",
    "-d",
    help="A dictionary mapping string keys to "
    "a list of sleepless.data.sample.DelayedSample instances implementing datasets "
    "to be used for testsing the model, possibly including all "
    "pre-processing pipelines required. All keys keys defined in the dictionary will be used.",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--model",
    "-m",
    help="An instance model to be trained",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--weight",
    "-w",
    help="Path or URL to trained model file (pickle if scikit model)",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--model-parameters",
    "-mp",
    help="Parameters of model training",
    required=True,
    cls=ResourceOption,
)
@verbosity_option(logger=logger, cls=ResourceOption, expose_value=False)
def predict(output_folder, dataset, model, weight, model_parameters, **_):
    import time

    import joblib

    from ..engine.predictor_scikit import predict_scikit
    from ..engine.predictor_torch import predict_torch

    output_folder = os.path.join(output_folder, "prediction")

    os.makedirs(output_folder, exist_ok=True)

    tic = time.perf_counter()

    if isinstance(dataset, str):
        dataset = joblib.load(dataset)

    if not isinstance(dataset, dict):
        logger.error("Dataset should be path to a dataset or a dataset object")

    logger.info("Start prediction")

    if isinstance(model, nn.Module):
        predict_torch(dataset, model, weight, output_folder, model_parameters)

    else:
        fitted_model = joblib.load(weight)

        if not isinstance(fitted_model, type(model)):
            logger.warning(
                f"model is type {type(model)} and fitted model is type "
                f"{type(fitted_model)}"
            )

        predict_scikit(dataset, fitted_model, output_folder, model_parameters)

    toc = time.perf_counter()

    logger.info(f"Prediction ended and saved, it took {toc - tic:0.1f} seconds")
