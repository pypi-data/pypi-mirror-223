# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later


import os

import click

from clapper.click import verbosity_option
from clapper.logging import setup

logger = setup(__name__.split(".")[0], format="%(levelname)s: %(message)s")


@click.command(
    epilog="""Examples:

\b
    1. Compares system A and B, with their own metric table files:

       .. code:: sh

          sleepless compare -vv A path/to/A/metric_table.csv B path/to/B/metric_table.csv
""",
)
@click.argument(
    "label_path",
    nargs=-1,
)
@click.option(
    "--output-folder",
    "-o",
    help="Path where to store table and plot",
    required=True,
    type=click.Path(),
)
@verbosity_option(logger=logger, expose_value=False)
def compare(label_path, output_folder, **_) -> None:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    from sleepless.utils.utils_fig_table_df import (
        make_rst_tabulate,
        save_fig,
        save_tables,
    )

    os.makedirs(output_folder, exist_ok=True)

    # hack to get a dictionary from arguments passed to input
    if len(label_path) % 2 != 0:
        raise click.ClickException(
            "Input label-paths should be doubles"
            " composed of name-path entries"
        )
    data = dict(zip(label_path[::2], label_path[1::2]))

    output_name = "compare_" + "_".join(data.keys())

    df_new = pd.DataFrame()

    for index, (k, v) in enumerate(data.items()):
        df = pd.read_csv(v)
        metric_col = [col for col in df if col.startswith("Unnamed")][0]
        df = df.set_index(df[metric_col])

        if index == 0:
            df_new = df.head(2)
            df_new = df_new.set_index(df_new[metric_col])

        raw = df.xs("Balanced accuracy").copy()

        raw.name = str(k)

        weigth_epochs = df.xs("Total number of epochs")

        col_val = [
            col
            for col in df_new
            if ("train" in col or "validation" in col)
            and col != "train"
            and col != "validation"
        ]

        raw["Validation aggregated balanced accuracy"] = np.average(
            a=raw[col_val], weights=weigth_epochs[col_val]
        )

        col_test = [col for col in df_new if "test" in col and col != "test"]

        raw["Test aggregated balanced accuracy"] = np.average(
            a=raw[col_test], weights=weigth_epochs[col_test]
        )

        df_new = pd.concat([df_new, raw.to_frame().T])

    df_new = df_new.drop(df_new.columns[0], axis=1)
    df_new = df_new.where(pd.notnull(df_new), None)

    # save csv and tables
    df_new.to_csv(os.path.join(output_folder, output_name + ".csv"))
    save_tables(
        output_folder,
        [make_rst_tabulate(output_name, df_new.T)],
        output_name,
    )

    fig, axes = plt.subplots(
        nrows=1, ncols=1, sharey=True, subplot_kw=dict(frameon=False)
    )

    ax2 = fig.add_subplot(111, zorder=-1)
    for _, spine in ax2.spines.items():
        spine.set_visible(False)
    ax2.tick_params(labelleft=False, labelbottom=False, left=False, right=False)
    ax2.sharey(axes)
    ax2.grid(axis="y")
    ax2.get_xaxis().set_visible(False)

    selection = df_new[
        [
            "Validation aggregated balanced accuracy",
            "Test aggregated balanced accuracy",
        ]
    ][2:]

    selection.plot(
        ax=axes,
        kind="bar",
        stacked=False,
        ylabel="Aggregated\n Balanced Accuracy",
        title="",
        legend=None,
        xlabel="",
    )

    for p in axes.patches:
        axes.annotate(
            f"{p.get_height():.3f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height() / 2.0),
            ha="center",
            va="center",
            xytext=(0, 0),
            textcoords="offset points",
            rotation=90,
            fontweight="bold",
        )

    fig.legend(labels=["Validation", "Test"], loc="lower left", ncol=1)

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    plt.figure(figsize=(4, 3), dpi=300)

    save_fig(output_folder, [fig], output_name + ".pdf")

    plt.close()
