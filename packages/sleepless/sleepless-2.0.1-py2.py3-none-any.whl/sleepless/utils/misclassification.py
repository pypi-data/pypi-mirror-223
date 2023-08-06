# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Compute misclassified Epochs and function to visualize them."""

from __future__ import annotations

import matplotlib.pyplot as plt
import mne.epochs
import numpy as np

from matplotlib.figure import Figure

from ..data.sample import DelayedSample
from .matplotlib_utils import PointBrowser, get_sleep_stage_labels, stage_colors


def compute_misclassification(
    sample: DelayedSample, return_well_classified: bool = False
) -> tuple[mne.Epochs, dict[str, np.ndarray]]:
    """Compute the misclassification epochs of a sample.

    :param sample: a sample of a dataset
    :param return_well_classified: If True, the function return well
        classified epochs instead of misclassified
    :return: the misclassified epochs and a dictionary with label,
        prediction and labels of the misclassified epochs.
    """

    prob = sample.output_prob

    y_pred = np.argmax(prob, axis=1)

    y_label = sample.label

    index = np.argwhere(y_pred != y_label).flatten()

    if return_well_classified:
        index = np.argwhere(y_pred == y_label).flatten()

    y_prob = [str(prob[i, :]) for i in index]

    misclassified_epochs = sample.data["data"][index]

    misclassified_pred = y_pred[index]

    misclassified_labels = y_label[index]

    df_mis = dict(
        zip(
            ["output_probability", "prediction", "label", "Epochs index"],
            [
                y_prob,
                misclassified_pred,
                misclassified_labels,
                index,
            ],
        )
    )

    return misclassified_epochs, df_mis


def plot_misclassified_epochs(
    sample: DelayedSample,
    vizu_epochs: bool = False,
    return_well_classified: bool = False,
) -> tuple[Figure, dict[str, np.ndarray]]:
    """Generate a plot and a dictionary of the misclassified epochs.

    :param sample: a sample of a dataset :vizu_epochs: open an
        interactive plot of misclassified epochs
    :return_well_classified: If True, return well classified epochs
        instead of misclassified
    :return: a figure and a dictionary of the misclassified epochs
    """

    misclassified_epochs, dic_miss = compute_misclassification(
        sample, return_well_classified
    )

    fig = plt.figure(1)

    x = dic_miss["Epochs index"]

    y_pred = dic_miss["prediction"]

    y = dic_miss["label"]

    event_dic_sample_label = get_sleep_stage_labels([y])

    event_dic_sample_pred = get_sleep_stage_labels([y_pred])

    if return_well_classified:
        for index, colors in enumerate(stage_colors[: len(np.unique(y_pred))]):
            plt.scatter(
                x[y == np.unique(y_pred)[index]],
                y[y == np.unique(y_pred)[index]],
                color=colors,
                picker=True,
            )

            plt.title("Well classified Epochs")

    else:
        for index, colors in enumerate(stage_colors[: len(np.unique(y_pred))]):
            plt.scatter(
                x[y_pred == np.unique(y_pred)[index]],
                y[y_pred == np.unique(y_pred)[index]],
                color=colors,
                picker=True,
            )

            plt.title("Misclassified Epochs")

    plt.legend(
        event_dic_sample_pred.keys(),
        title="Prediction",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )

    plt.yticks(np.unique(y), event_dic_sample_label.keys())

    plt.ylabel(ylabel="True label")

    plt.xlabel("Epochs index")

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    if vizu_epochs:
        fig.suptitle(
            "Sample (Key="
            + str(sample.key)
            + ", Age ="
            + str(sample.age)
            + ", Gender ="
            + str(sample.gender)
            + " )"
        )

        y_pred = [
            list(event_dic_sample_pred.keys())[int(pred)] for pred in y_pred
        ]

        label = [list(event_dic_sample_label.keys())[int(label)] for label in y]

        browser = PointBrowser(x, y, label, y_pred, misclassified_epochs, fig)

        fig.canvas.mpl_connect("pick_event", browser.on_pick)
        fig.canvas.mpl_connect("key_press_event", browser.on_press)

        plt.show()

    return fig, dic_miss
