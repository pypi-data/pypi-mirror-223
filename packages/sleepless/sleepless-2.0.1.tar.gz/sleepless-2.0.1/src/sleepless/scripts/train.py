# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

import click
import torch
import torch.nn as nn

from clapper.click import ConfigCommand, ResourceOption, verbosity_option
from clapper.logging import setup

logger = setup(__name__.split(".")[0], format="%(levelname)s: %(message)s")


@click.command(
    entry_point_group="sleepless.config",
    cls=ConfigCommand,
    epilog="""Examples:

\b
    1. Trains a random forest model with ST_subset (from EDF database):

       .. code:: sh

          sleepless train rf-gs-mne stedf-filtered -o "/path/to/output_folder"

""",
)
@click.option(
    "--output-folder",
    "-o",
    help="Path where to store the generated model (created if does not exist)",
    required=True,
    type=click.Path(),
    default="results",
    cls=ResourceOption,
)
@click.option(
    "--dataset",
    "-d",
    help="A dictionary mapping string keys to "
    "a list of sleepless.data.sample.DelayedSample instances implementing datasets "
    "to be used for training and validating the model, possibly including all "
    "pre-processing pipelines required. At least "
    "one key named ``train`` must be available.",
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
    "--model-parameters",
    "-mp",
    help="Parameters of model training",
    required=True,
    cls=ResourceOption,
)
@verbosity_option(logger=logger, cls=ResourceOption, expose_value=False)
def train(output_folder, dataset, model, model_parameters, **_):
    import json
    import time

    import joblib

    from ..data.utils import ComposeTransform
    from ..engine.trainer_scikit import train_scikit
    from ..engine.trainer_torch import train_torch
    from .utils import default

    output_folder = os.path.join(output_folder, "train")

    os.makedirs(output_folder, exist_ok=True)

    with open(
        os.path.join(output_folder, "model_parameters.json"), "w"
    ) as outfile:
        json.dump(model_parameters, outfile, default=default, indent=4)

    tic = time.perf_counter()

    if isinstance(dataset, str):
        dataset = joblib.load(dataset)

    if not isinstance(dataset, dict):
        logger.error("Dataset should be path to a dataset or a dataset object")

    logger.info("Start training")

    training_set_transform = dataset["train"]

    valid_set = [dataset["validation"]]

    extra_valid_set_list = [
        v
        for k, v in dataset.items()
        if (k.startswith("validation") and not k == "validation")
    ]

    validation_set_list_transform = valid_set + extra_valid_set_list

    if not hasattr(training_set_transform[0], "features") and not isinstance(
        training_set_transform, torch.utils.data.ConcatDataset
    ):
        logger.info("start data transformation")

        compose_transform = ComposeTransform(model_parameters["transform"])

        training_set_transform = compose_transform(training_set_transform)

        validation_set_list_transform = [
            compose_transform(valid) for valid in validation_set_list_transform
        ]

    if isinstance(model, nn.Module):
        train_torch(
            model,
            training_set_transform,
            validation_set_list_transform,
            output_folder,
            model_parameters,
        )

    else:
        train_scikit(
            model,
            training_set_transform,
            validation_set_list_transform,
            output_folder,
            model_parameters,
        )

    toc = time.perf_counter()

    logger.info(
        f"End of training and model saved, it took {toc - tic:0.1f} seconds"
    )
