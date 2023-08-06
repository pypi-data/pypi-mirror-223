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
    1. Analyzes a training log and produces various plots:

       .. code:: sh

          sleepless train-analysis -vv log.csv constants.csv

""",
)
@click.argument(
    "log",
    type=click.Path(dir_okay=False, exists=True),
)
@click.argument(
    "constants",
    type=click.Path(dir_okay=False, exists=True),
)
@click.option(
    "--output-folder",
    "-o",
    help="Path where to store the figures (created if does not exist)",
    required=True,
    default="results",
    cls=ResourceOption,
    type=click.Path(),
)
@verbosity_option(logger=logger, cls=ResourceOption, expose_value=False)
def train_analysis(
    log,
    constants,
    output_folder,
    **_,
):
    """Analyzes the training logs for loss evolution and resource
    utilisation."""
    import os

    import pandas

    from ..utils.utils_fig_table_df import save_fig
    from .utils import _hardware_utilisation, _loss_evolution

    output_folder = os.path.join(output_folder, "train_anaylsis")

    os.makedirs(output_folder, exist_ok=True)

    constants = pandas.read_csv(constants)
    constants = dict(zip(constants.keys(), constants.values[0]))
    data = pandas.read_csv(log)

    # now, do the analysis
    fig_list = [_loss_evolution(data), _hardware_utilisation(data, constants)]

    save_fig(output_folder, fig_list)
