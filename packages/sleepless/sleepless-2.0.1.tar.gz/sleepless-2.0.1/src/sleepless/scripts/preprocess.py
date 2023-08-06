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
    1. Save dataset after preprocessing:

       .. code:: sh

          sleepless preprocess stedf-filtered

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
@verbosity_option(logger=logger, cls=ResourceOption, expose_value=False)
def preprocess(dataset, **_):
    import time

    from ..data.utils import saving_preprocess

    tic = time.perf_counter()

    saving_preprocess(dataset)

    toc = time.perf_counter()

    logger.info(
        f"Dataset transformed and saved, it took {toc - tic:0.1f} seconds"
    )
