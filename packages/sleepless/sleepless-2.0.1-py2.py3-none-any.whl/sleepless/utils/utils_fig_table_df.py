# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Concatenate and save a list of figure or table."""

from __future__ import annotations

import textwrap

from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.backends.backend_pdf import PdfPages
from tabulate import tabulate

from ..data.sample import DelayedSample


def create_df(
    subset: list[DelayedSample], attributes: list[str], bins: list[int]
) -> pd.DataFrame:
    """Create a dataframe from a list of Samples and for a list of attributes,
    if "age" is in attribute, a new column "ageGroup" is added to the dataframe
    which assign an ageGroup to the patient.

    For the creation of "ageGroup" column bins has to be a list of int
    which define the different categories of age.

    :param subset: a list of Samples
    :param attributes: a list of attribute which are attribute of
        Samples
    :param bins: definition of the age categories
    """

    data: dict = {name: list() for name in attributes}

    for _instance in subset:
        for attribute in attributes:
            if hasattr(_instance, attribute):
                data[attribute].append(getattr(_instance, attribute))

    df = pd.DataFrame(data=data)

    if "age" in attributes:
        df["ageGroup"] = pd.cut(df["age"], bins=bins, labels=None, right=True)

        df["ageGroup"].cat.add_categories("unknown").fillna("unknown")

    return df


def make_rst_tabulate(
    name: str, table: pd.DataFrame, min_column_width: int = 0
):
    """Create Rst table from pandas.DataFrame.

    :param name: title of the table
    :param table: dataframe to be tabulate and save
    :param min_column_width: fixed a minimum column width
    """

    title = "".join(name)

    len_title = len(title)

    if len_title < min_column_width:
        title = title.ljust(min_column_width)

    index_name = list(table.T.index)

    if isinstance(index_name[0], int):
        index = [" "] * len(index_name)

    else:
        index = list(table.T.index.get_level_values(0))

    df = pd.Series(index, name=str(title))

    table = pd.concat([df, table.T.reset_index(drop=True)], axis=1)

    tabulate_table = textwrap.indent(
        tabulate(
            table,
            headers="keys",
            tablefmt="rst",
            floatfmt=".2f",
            showindex=False,
        ),
        "  ",
    )

    return tabulate_table


def save_fig(
    out_path: str, fig_list: list[plt.figure], name: str = "plot"
) -> None:
    with PdfPages(
        out_path
        + "/"
        + str(name)
        + "_"
        + datetime.now().strftime("%Y%m%d-%H%M%S")
        + ".pdf"
    ) as pdf:
        for fig in fig_list:
            pdf.savefig(fig)

    return


def save_tables(
    out_path: str,
    tables: list[str],
    name: str = "tables",
):
    out_path += (
        "/"
        + str(name)
        + "_"
        + datetime.now().strftime("%Y%m%d-%H%M%S")
        + ".rst"
    )
    with open(out_path, "w") as f:
        f.write("".join(".. table:: " + name) + "\n\n\n")

        for table1 in tables:
            f.write(table1)
            f.write("\n\n\n\n")

    return out_path
