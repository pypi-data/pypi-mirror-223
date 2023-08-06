# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Some matplotlib variables."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


def get_sleep_stage_labels(y_class: list[np.ndarray]) -> dict[str, int]:
    """Filter event dictionary with events code present in a list, this list
    should only contains, y_label, y_pred (both or only one of them)

    Event index must follow the following mapping:

    event_dic = {
        "Stage W": 0,
        "N1": 1,
        "N2": 2,
        "N3": 3,
        "REM": 4,
        "Stage ?": 5,
        }

    :param y_label: a list of np.ndarray(n_epochs),containing event index.
    """
    event_dic = {
        "Stage W": 0,
        "N1": 1,
        "N2": 2,
        "N3": 3,
        "REM": 4,
        "Stage ?": 5,
    }

    labels_code = np.unique(np.concatenate(y_class))

    new_dic = {k: v for k, v in event_dic.items() if v in labels_code}

    return new_dic


# variable to color sleep stage always the same way
stage_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]


class PointBrowser:
    def __init__(self, x, y, label, ypred, misclassified_epochs, fig):
        self.ypred = ypred

        self.x = x

        self.y = y

        self.label = label

        self.misclassified_epochs = misclassified_epochs

        self.fig = fig

        self.fig2 = plt.figure(2)

        self.lastind = x[0]

        self.text = self.fig.axes[0].text(
            0.01,
            0.90,
            "selected: none",
            transform=self.fig.axes[0].transAxes,
            va="top",
        )
        (self.selected,) = self.fig.axes[0].plot(
            [x[0]], [y[0]], "o", ms=12, alpha=0.4, color="yellow", visible=False
        )

    def on_press(self, event):
        if self.lastind is None:
            return
        if event.key not in ("n", "p"):
            return
        if event.key == "n":
            inc = 1
        else:
            inc = -1

        self.lastind += inc
        self.lastind = np.clip(self.lastind, 0, len(self.x) - 1)
        self.update()

    def on_pick(self, event):
        N = len(event.ind)
        if not N:
            return True

        xs = event.mouseevent.xdata
        ys = event.mouseevent.ydata

        dataind = np.hypot(xs - self.x, ys - self.y).argmin()

        self.lastind = dataind
        self.update()

    def update(self):
        from mne.viz import plot_epochs

        if self.lastind is None:
            return

        dataind = self.lastind

        plt.close(2)

        self.fig2 = plot_epochs(
            self.misclassified_epochs[dataind],
            scalings=dict(eeg=2e-4, resp=1e3, eog=1e-4, emg=1e-7, misc=1e-1),
            picks="all",
        )

        self.fig2.axes[0].text(
            0.01,
            0.95,
            f"prediction={str(self.ypred[dataind])}\nlabel={str(self.label[dataind])}",
            transform=self.fig2.axes[0].transAxes,
            va="top",
        )
        self.selected.set_visible(True)
        self.selected.set_data(self.x[dataind], self.y[dataind])

        self.text.set_text(
            f"Epochs index selected:{self.x[dataind]}\nstart-end time={self.x[dataind]*30}-{self.x[dataind]*30+30}"
        )
        self.fig.canvas.draw()


def loss_graph_xgboost(results):
    _label = ["Training loss", "Validation loss"]

    fig = plt.figure(figsize=(10, 7))

    for index, key in enumerate(results.keys()):
        for key_metric in results[key].keys():
            plt.plot(results[key][key_metric], label=_label[index])

    plt.xlabel("Number of trees")
    plt.ylabel("Loss")
    plt.legend()
    plt.close()

    return fig
