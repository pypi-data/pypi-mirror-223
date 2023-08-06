# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Compute Statistics for protocols."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.figure import Figure

from ..data.sample import DelayedSample
from .utils_fig_table_df import create_df, save_fig


def make_stats(
    dataset: dict[str, list[DelayedSample]],
    out_path: str | None = None,
    attributes: list[str] = ["age", "gender"],
    bins: list[int] = [0, 18, 60, 70, 80, 90, 100, 110],
) -> list[Figure]:
    """Compute different statistics on the subsets of dataset and created
    figure of the statistics saved.

    :param dataset: A dictionary containing different sets (e.g.
        train,test).
    :param keep: a list of attribute on which we perform analysis
    :param out_path: the path location where files will be saved
    :param bins: definition of the age categories
    """

    keys = list(dataset.keys())

    _attributes = [att for att in dir(dataset[keys[0]][0]) if att in attributes]

    keys.append("protocol")

    frames = []

    list_fig = []

    df_subset = {}

    for key in keys:
        if key != "protocol":
            df_subset[key] = create_df(dataset[key], _attributes, bins)

            frames.append(df_subset[key])

        else:
            df_subset[key] = pd.concat(frames)

    for attribute in _attributes:
        fig, axes = plt.subplots(nrows=1, ncols=len(keys))

        axes_index = 0

        for key in keys:
            if attribute == "gender":
                class_count = df_subset[key].groupby(["gender"]).size()

                class_count.plot(
                    ax=axes[axes_index],
                    kind="pie",
                    title=str(key).capitalize(),
                    autopct=lambda p: "{:.1f}%({:.0f})".format(
                        p, (p / 100) * class_count.sum()
                    ),
                    ylabel="",
                )

                axes_index += 1

            if attribute == "age":
                class_count = (
                    df_subset[key]
                    .groupby(["ageGroup", "gender"])
                    .age.count()
                    .unstack()
                )

                class_count.plot(
                    ax=axes[axes_index],
                    kind="bar",
                    stacked=False,
                    ylabel="",
                    title=str(key).capitalize(),
                )

                axes_index += 1

            if attribute == "medication":
                class_count = df_subset[key].groupby(["medication"]).size()

                class_count.plot(
                    ax=axes[axes_index],
                    kind="pie",
                    title=str(key).capitalize(),
                    autopct=lambda p: "{:.1f}%({:.0f})".format(
                        p, (p / 100) * class_count.sum()
                    ),
                    ylabel="",
                )

                axes_index += 1

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        fig.suptitle(str(attribute).capitalize())

        plt.close()

        list_fig.append(fig)

    if out_path is not None:
        save_fig(out_path, list_fig)

    return list_fig
