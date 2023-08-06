# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Setup functions for scripts."""

import logging
import os
import sys
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pkg_resources

logger = logging.getLogger(__name__)


def save_sh_command(destfile):
    if os.path.exists(destfile):
        logger.info(f"Not overwriting existing file '{destfile}'")
        return

    logger.info(f"Writing command-line for reproduction at '{destfile}'...")
    os.makedirs(os.path.dirname(destfile), exist_ok=True)

    with open(destfile, "w") as f:
        f.write("#!/usr/bin/env sh\n")
        f.write(f"# date: {time.asctime()}\n")
        version = pkg_resources.require("sleepless")[0].version
        f.write(f"# version: {version} (sleepless)\n")
        f.write(f"# platform: {sys.platform}\n")
        f.write("\n")
        args = []
        for k in sys.argv:
            if " " in k:
                args.append(f'"{k}"')
            else:
                args.append(k)
        if os.environ.get("CONDA_DEFAULT_ENV") is not None:
            f.write(f"#conda activate {os.environ['CONDA_DEFAULT_ENV']}\n")
        f.write(f"#cd {os.path.realpath(os.curdir)}\n")
        f.write(" ".join(args) + "\n")
    os.chmod(destfile, 0o755)


def default(obj):
    if "sleepless.data.transforms" in str(obj):
        return {str(obj).split(" ")[0]: obj.__dict__}
    else:
        return str(obj)


def _loss_evolution(df: pd.DataFrame) -> matplotlib.figure.Figure:
    """Plots the loss evolution over time (epochs)

    :param df: dataframe containing the training logs
    :return: Figure to be displayed or saved to file
    """

    figure = plt.figure()
    axes = figure.gca()

    axes.plot(df.epoch.values, df.loss.values, label="Training")
    if "validation_loss" in df.columns:
        axes.plot(
            df.epoch.values, df.validation_loss.values, label="Validation"
        )
        # shows a red dot on the location with the minima on the validation set
        lowest_index = np.argmin(df["validation_loss"])

        axes.plot(
            df.epoch.values[lowest_index],
            df.validation_loss[lowest_index],
            "mo",
            label=f"Lowest validation ({df.validation_loss[lowest_index]:.3f}@{df.epoch[lowest_index]})",
        )

    if "extra_validation_losses" in df.columns:
        # These losses are in array format. So, we read all rows, then create a
        # 2d array.  We transpose the array to iterate over each column and
        # plot the losses individually.  They are numbered from 1.
        df["extra_validation_losses"] = df["extra_validation_losses"].apply(
            lambda x: np.fromstring(x.strip("[]"), sep=" ")
        )
        losses = np.vstack(df.extra_validation_losses.values).T
        for n, k in enumerate(losses):
            axes.plot(df.epoch.values, k, label=f"Extra validation {n+1}")

    axes.set_title("Loss over time")
    axes.set_xlabel("Epoch")
    axes.set_ylabel("Loss")

    axes.legend(loc="best")
    axes.grid(alpha=0.3)
    figure.set_layout_engine("tight")

    return figure


def _hardware_utilisation(
    df: pd.DataFrame, const: dict
) -> matplotlib.figure.Figure:
    """Plot the CPU utilisation over time (epochs).

    :param df: dataframe containing the training logs
    :param const: training and hardware constants
    :return: figure to be displayed or saved to file
    """
    figure = plt.figure()
    axes = figure.gca()

    cpu_percent = df.cpu_percent.values / const["cpu_count"]
    cpu_memory = 100 * df.cpu_rss / const["cpu_memory_total"]

    axes.plot(
        df.epoch.values,
        cpu_percent,
        label=f"CPU usage (cores: {const['cpu_count']})",
    )
    axes.plot(
        df.epoch.values,
        cpu_memory,
        label=f"CPU memory (total: {const['cpu_memory_total']:.1f} Gb)",
    )
    if "gpu_percent" in df:
        axes.plot(
            df.epoch.values,
            df.gpu_percent.values,
            label=f"GPU usage (type: {const['gpu_name']})",
        )
    if "gpu_memory_percent" in df:
        axes.plot(
            df.epoch.values,
            df.gpu_memory_percent.values,
            label=f"GPU memory (total: {const['gpu_memory_total']:.1f} Gb)",
        )
    axes.set_title("Hardware utilisation over time")
    axes.set_xlabel("Epoch")
    axes.set_ylabel("Relative utilisation (%)")
    axes.set_ylim([0, 100])

    axes.legend(loc="best")
    axes.grid(alpha=0.3)
    figure.set_layout_engine("tight")

    return figure
