# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import click

from clapper.click import ConfigCommand, ResourceOption, verbosity_option
from clapper.logging import setup

logger = setup(__name__.split(".")[0], format="%(levelname)s: %(message)s")


@click.command(
    entry_point_group="sleepless.config",
    cls=ConfigCommand,
    epilog="""Examples:

\b
    1. Transform and save ST_subset (from EDF database):

       .. code:: sh

          sleepless visualize stedf-filtered -t raw -s train -n 0 -p "/path/to/predictions"

""",
)
@click.option(
    "--dataset",
    "-d",
    help="A dictionary mapping string keys to "
    "a list of sleepless.data.sample.DelayedSample instances implementing datasets "
    "to be used for training and validating the model, possibly including all "
    "pre-processing pipelines required.",
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--type",
    "-t",
    help="Type of data to visualize (e.g. raw, misclassified, wellclassified)",
    type=click.STRING,
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--subset",
    "-s",
    help="Subset where the sample you want to visualize is located (e.g. train, test)",
    type=click.STRING,
    required=True,
    cls=ResourceOption,
)
@click.option(
    "--sample",
    "-n",
    help="Sample number, 0-index based",
    required=True,
    type=click.IntRange(min=0),
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
@verbosity_option(logger=logger, cls=ResourceOption, expose_value=False)
def visualize(dataset, type, subset, sample, prediction_folder, **_):
    import joblib

    from ..data.utils import plot_PSG_and_annotation
    from ..engine.utils import load_from_hdf5
    from ..utils.misclassification import plot_misclassified_epochs

    logger.info("Start analysis")

    if isinstance(dataset, str):
        dataset = joblib.load(dataset)

    if not isinstance(dataset, dict):
        logger.error("Dataset should be path to a dataset or a dataset object")

    dataset = load_from_hdf5(dataset, prediction_folder, "prob")

    if subset not in dataset.keys():
        logger.error(f"{subset} is not a key of the dataset")

    if sample > len(dataset[subset]) - 1:
        logger.error(
            f"{subset} is of size {len(dataset[subset])-1} and you want to access index {sample}"
        )

    sample_data = dataset[subset][sample]

    if type == "raw":
        plot_PSG_and_annotation(
            sample_data.data["data"], sample_data.data["label"]
        )
        import matplotlib.pyplot

        matplotlib.pyplot.show()

    if type == "misclassified":
        plot_misclassified_epochs(sample_data, True)

    if type == "wellclassified":
        plot_misclassified_epochs(sample_data, True, True)
