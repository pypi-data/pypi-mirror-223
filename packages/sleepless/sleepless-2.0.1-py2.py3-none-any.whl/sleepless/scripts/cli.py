# Copyright © 2022 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import click

from clapper.click import AliasedGroup

from . import (
    analyze,
    compare,
    dataset,
    experiment,
    predict,
    preprocess,
    train,
    train_analysis,
    visualize,
)


@click.group(
    cls=AliasedGroup,
    context_settings=dict(help_option_names=["-?", "-h", "--help"]),
)
def cli():
    """Sleep stage classification Benchmark commands."""
    pass


cli.add_command(analyze.analyze)
cli.add_command(dataset.dataset)
cli.add_command(experiment.experiment)
cli.add_command(predict.predict)
cli.add_command(train.train)
cli.add_command(preprocess.preprocess)
cli.add_command(visualize.visualize)
cli.add_command(train_analysis.train_analysis)
cli.add_command(compare.compare)
