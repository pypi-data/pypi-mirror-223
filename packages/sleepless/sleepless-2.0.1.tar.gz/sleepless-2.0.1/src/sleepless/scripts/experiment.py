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
    1. Run a experiment with a random forest model and with ST_subset (from EDF database):

       .. code::

           sleepless analyze stedf-filtered rf-gs-mne -o "/path/to/output_folder"

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
@click.option(
    "--detailed",
    help="Detailed analysis",
    is_flag=True,
    default=False,
    cls=ResourceOption,
)
@verbosity_option(logger=logger, cls=ResourceOption, expose_value=False)
@click.pass_context
def experiment(
    ctx, output_folder, dataset, model, model_parameters, detailed, **_
):
    import time

    from .analyze import analyze
    from .predict import predict
    from .train import train
    from .utils import save_sh_command

    save_sh_command(os.path.join(output_folder, "command.sh"))

    tic = time.perf_counter()

    if isinstance(dataset, str):
        import joblib

        dataset = joblib.load(dataset)

    if not isinstance(dataset, dict):
        logger.error("Dataset should be path to a dataset or a dataset object")

    ctx.invoke(
        train,
        output_folder=output_folder,
        dataset=dataset,
        model=model,
        model_parameters=model_parameters,
    )

    if isinstance(model, nn.Module):
        trained_model = os.path.join(
            output_folder, "train/model_lowest_valid_loss.pth"
        )
        if not os.path.exists(trained_model):
            trained_model = os.path.join(
                output_folder, "train/model_final_epoch.pth"
            )

    else:
        trained_model = os.path.join(output_folder, "train/fit_model")

    ctx.invoke(
        predict,
        output_folder=output_folder,
        model=model,
        dataset=dataset,
        weight=trained_model,
        model_parameters=model_parameters,
    )

    ctx.invoke(
        analyze,
        output_folder=output_folder,
        dataset=dataset,
        prediction_folder=output_folder + "/prediction",
        detailed=detailed,
    )

    toc = time.perf_counter()

    logger.info(f"Experiment ended and took {toc - tic:0.1f} seconds")
