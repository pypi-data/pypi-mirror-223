# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Analyze script."""

from __future__ import annotations

import logging
import typing

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    balanced_accuracy_score,
    cohen_kappa_score,
    hamming_loss,
    matthews_corrcoef,
)

from ..data.sample import DelayedSample
from ..utils.matplotlib_utils import get_sleep_stage_labels
from ..utils.stats_protocol import make_stats
from ..utils.utils_fig_table_df import create_df, make_rst_tabulate

logger = logging.getLogger(__name__)


def metric_stats(
    dataset: dict[str, list[DelayedSample]],
    bins: list[int] = [0, 18, 60, 70, 80, 90, 100, 110],
) -> tuple[list, list, typing.Iterable[tuple]]:
    """Compute different metrics on a dataset and saved them as table and
    figure.

    :param dataset: A dictionary containing different sets (e.g.
        train,test).
    :param bins: definition of the age categories
    :param out_path: the path location where fils will be saved
    :return: list of figures, list of tables and dictionary of metrics
    """

    # for now only stats for these attribute can be computed
    # ATTENTION for now attribute name is hardcode, attribute names has to exactly match these names in keep
    keep = ["age", "gender"]

    keys = [key for key in dataset.keys()]

    attributes = [att for att in dir(dataset[keys[0]][0]) if att in keep]

    figures = []

    list_df = [pd.DataFrame() for attr in range(len(attributes) + 1)]

    table_names = ["metrics table"]

    table_names += [attr + " metrics table" for attr in attributes]

    for key in keys:
        name_subset = str(key)

        df_subset = create_df(dataset[key], attributes, bins)
        df_subset["output_prob"] = [_id.output_prob for _id in dataset[key]]
        df_subset["y_label"] = [sample.label for sample in dataset[key]]

        return_metric_key, return_figures_key = metrics_computation(
            df_subset, name_subset
        )

        list_df[0][str(name_subset)] = return_metric_key
        figures += return_figures_key

        for index, attribute in enumerate(attributes, 1):
            if attribute == "age":
                attribute = "ageGroup"

                df_index = df_subset[str(attribute)].unique()

                df_index = df_index[np.argsort(df_index.codes)]

            else:
                df_index = df_subset[str(attribute)].unique()

            name_attribute = name_subset + " " + str(attribute)

            for value in df_index:
                df_value = df_subset[df_subset[str(attribute)] == value]

                name_value = name_attribute + " " + str(value)

                (
                    return_metric_attrib,
                    return_figures_attrib,
                ) = metrics_computation(df_value, name_value)

                list_df[index][str(name_value)] = return_metric_attrib
                figures += return_figures_attrib

    tables_metrics = []

    for index, df in enumerate(list_df):
        tables_metrics.append(make_rst_tabulate(table_names[index], df))

    figures += make_stats(dataset, attributes=attributes)

    return figures, tables_metrics, zip(table_names, list_df)


def metrics_computation(
    data: pd.DataFrame, name: str
) -> tuple[pd.DataFrame, list[plt.Figure]]:
    """Compute metrics for the scikit-learn pipeline,6 metrics are computed:
    accuracy, confusion matrix, matthews_corrcoef, balanced_accuracy, linear
    weighted Kappa and quadratic weighted Kappa.

    :param data: a dataframe containing label and prediction for
        different samples
    :param name: path location where files will be saved
    :return: Matthews_corrcoef, accuracy, linear weighted Kappa,
        quadratic weighted Kappa and balanced_accuracy are return in
        common pd.Dataframe(df_metrics) Figure of confusion matrix are
        return as list of figure
    """

    dic_sample = data["output_prob"].to_numpy()

    nb_samples = dic_sample.shape[0]

    y_label = np.concatenate(data["y_label"].to_numpy(), axis=0)

    output = np.concatenate(dic_sample, axis=0)

    output = np.argmax(output, axis=1)

    nb_epochs = output.shape[0]

    labels = get_sleep_stage_labels([y_label, output])

    _accuracy_score = accuracy_score(y_label, output)

    _confusion_matrix = ConfusionMatrixDisplay.from_predictions(
        y_label,
        output,
        normalize="true",
        display_labels=labels.keys(),
        values_format=".2f",
        xticks_rotation="vertical",
    )

    _confusion_matrix_total_number = ConfusionMatrixDisplay.from_predictions(
        y_label,
        output,
        normalize=None,
        display_labels=labels.keys(),
        xticks_rotation="vertical",
    )

    _linear_kappa_score = cohen_kappa_score(y_label, output, weights="linear")

    _quadratic_kappa_score = cohen_kappa_score(
        y_label, output, weights="quadratic"
    )

    _balanced_accuracy_score = balanced_accuracy_score(y_label, output)

    _matthews_corrcoef = matthews_corrcoef(y_label, output)

    _hamming_loss = hamming_loss(y_label, output)

    key = [
        "Samples number",
        "Total number of epochs",
        "Balanced accuracy",
        "Accuracy score",
        "Linear Weighted Kappa",
        "Quadratic Weighted Kappa",
        "Mcc",
        "Hamming Loss",
    ]

    value = [
        int(nb_samples),
        int(nb_epochs),
        _balanced_accuracy_score,
        _accuracy_score,
        _linear_kappa_score,
        _quadratic_kappa_score,
        _matthews_corrcoef,
        _hamming_loss,
    ]

    df_metrics = pd.DataFrame(value, key)

    _confusion_matrix.ax_.set_title(
        " ".join(name.split("_")).capitalize() + " normalized"
    )

    _confusion_matrix.figure_.set_tight_layout(True)

    plt.close()

    _confusion_matrix_total_number.ax_.set_title(
        " ".join(name.split("_")).capitalize()
    )

    _confusion_matrix_total_number.figure_.set_tight_layout(True)

    plt.close()

    figures = [
        _confusion_matrix.figure_,
        _confusion_matrix_total_number.figure_,
    ]

    return df_metrics, figures


def misclassified_analyze(
    dataset: dict[str, list[DelayedSample]],
) -> tuple[list, dict[str, dict]]:
    """Compute an analysis of the misclassified and well classified Epochs of a
    dataset, for each samples of the dataset, one figure (prediction/true
    label) and a table is generated.

    :param dataset: a sample of a data
    :return: list of figures and a dictionary
    """

    from ..utils.misclassification import plot_misclassified_epochs

    fig_list = []

    dic_output = {}

    for key in dataset.keys():
        for index_sample, sample in enumerate(dataset[key]):
            for boolean in [True, False]:
                tab_name = "Misclassified"

                if boolean:
                    tab_name = "Well classified"

                fig, dic_miss = plot_misclassified_epochs(
                    sample, return_well_classified=boolean
                )

                fig.suptitle(
                    str(key).capitalize()
                    + " set, Sample "
                    + str(index_sample)
                    + " ( "
                    + str(sample.key)
                    + " )"
                )

                plt.close()

                name_dic = (
                    str(tab_name)
                    + " Epochs for : "
                    + str(key).capitalize()
                    + " set, Sample "
                    + str(index_sample)
                    + " ( "
                    + str(sample.key)
                    + " )"
                )

                fig_list.append(fig)

                dic_output[name_dic] = dic_miss

    return fig_list, dic_output
