# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

import click
import joblib

from clapper.click import ConfigCommand, ResourceOption, verbosity_option
from clapper.logging import setup

logger = setup(__name__.split(".")[0], format="%(levelname)s: %(message)s")


@click.command(
    entry_point_group="sleepless.config",
    cls=ConfigCommand,
    epilog="""Examples:

\b
    1. Analyze of ST_subset (from EDF database) where prediction are already computed:

       .. code:: sh

          sleepless analyze stedf-filtered -p "/path/to/predictions" -o "/path/to/output_folder"

""",
)
@click.option(
    "--output-folder",
    "-o",
    help="Path where to store the analysis (created if does not exist)",
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
    "to be used for testing the model, possibly including all "
    "pre-processing pipelines required. All keys keys defined in the dictionary will be used."
    "The prediction of the samples needs to be run before",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--prediction-folder",
    "-p",
    help="folder where prediction have been saved",
    required=True,
    cls=ResourceOption,
    type=click.Path(),
)
@click.option(
    "--detailed",
    help="Detailed analysis",
    is_flag=True,
    default=False,
    cls=ResourceOption,
)
@verbosity_option(logger=logger, cls=ResourceOption, expose_value=False)
def analyze(output_folder, dataset, prediction_folder, detailed, **_):
    output_folder_analysis = os.path.join(output_folder, "analysis")

    os.makedirs(output_folder_analysis, exist_ok=True)

    import time

    from ..engine.analyze import metric_stats, misclassified_analyze
    from ..engine.utils import load_from_hdf5
    from ..utils.utils_fig_table_df import save_fig, save_tables

    tic = time.perf_counter()

    logger.info("Start analysis")

    if isinstance(dataset, str):
        dataset = joblib.load(dataset)

    if not isinstance(dataset, dict):
        logger.error("Dataset should be path to a dataset or a dataset object")

    dataset = load_from_hdf5(dataset, prediction_folder, "prob")

    fig_metrics, tables_metrics, list_dic = metric_stats(dataset)

    for k, v in list_dic:
        v.to_csv(
            os.path.join(
                output_folder_analysis, str(k).replace(" ", "_") + ".csv"
            )
        )

    save_fig(output_folder_analysis, fig_metrics, "Plot_metrics_analyze")

    path = save_tables(
        output_folder_analysis,
        tables_metrics,
        "metrics_tables",
    )

    f = open(path)

    logger.info("================== Metrics Analysis ========================")

    logger.info(f.read())

    f.close()

    if detailed:
        fig_misepochs, _ = misclassified_analyze(dataset)

        save_fig(
            output_folder_analysis,
            fig_misepochs,
            "Plot_misclassified_analysis_Epochs",
        )

        logger.info(
            "================== Misclassification Epochs Analysis ========================"
        )

    toc = time.perf_counter()

    logger.info(f"Analysis ended and saved, it took {toc - tic:0.1f} seconds")
