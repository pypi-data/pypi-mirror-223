# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for our CLI applications."""

import fnmatch
import logging
import os
import tempfile

import pytest

from click.testing import CliRunner


def _assert_exit_0(result):
    assert (
        result.exit_code == 0
    ), f"Exit code {result.exit_code} != 0 -- Output:\n{result.output}"


@pytest.mark.skip_if_rc_var_not_set("datadir.EDF")
def test_check_experiment(caplog):
    from sleepless.scripts.experiment import experiment

    cli_runner = CliRunner()
    # ensures we capture only ERROR messages and above by default
    caplog.set_level(logging.ERROR)

    with cli_runner.isolated_filesystem(), caplog.at_level(
        logging.INFO, logger="sleepless"
    ), tempfile.NamedTemporaryFile(mode="wt") as config:
        # re-write dataset configuration for test
        config.write(
            "from sleepless.configs.datasets.EDF.st_testing import dataset"
        )
        config.flush()

        output_folder = "results"

        options = [
            "chambon-test",
            config.name,
            f"--output-folder={output_folder}",
        ]

        result = cli_runner.invoke(experiment, options)

        _assert_exit_0(result)

        # check model was saved
        train_folder = os.path.join(output_folder, "train")
        assert os.path.exists(
            os.path.join(train_folder, "model_final_epoch.pth")
        )
        assert os.path.exists(
            os.path.join(train_folder, "model_lowest_valid_loss.pth")
        )
        assert os.path.exists(os.path.join(train_folder, "last_checkpoint"))
        assert os.path.exists(os.path.join(train_folder, "constants.csv"))
        assert os.path.exists(os.path.join(train_folder, "trainlog.csv"))
        assert os.path.exists(os.path.join(train_folder, "model_summary.txt"))

        # check predictions are there
        predict_folder = os.path.join(output_folder, "prediction")
        traindir = os.path.join(predict_folder, "train", "sleep-telemetry")
        assert os.path.exists(traindir)
        assert len(fnmatch.filter(os.listdir(traindir), "*.hdf5")) == 4
        valdir = os.path.join(predict_folder, "validation", "sleep-telemetry")
        assert os.path.exists(valdir)
        assert len(fnmatch.filter(os.listdir(valdir), "*.hdf5")) == 2
        testdir = os.path.join(predict_folder, "test", "sleep-telemetry")
        assert os.path.exists(testdir)
        assert len(fnmatch.filter(os.listdir(testdir), "*.hdf5")) == 2

        # check evaluation outputs
        analyze_folder = os.path.join(output_folder, "analysis")
        assert (
            len(
                fnmatch.filter(
                    os.listdir(analyze_folder), "metrics_tables_*.rst"
                )
            )
            == 1
        )
        assert (
            len(
                fnmatch.filter(
                    os.listdir(analyze_folder), "Plot_metrics_analyze_*.pdf"
                )
            )
            == 1
        )


def _check_help(entry_point):
    runner = CliRunner()
    result = runner.invoke(entry_point, ["--help"])
    _assert_exit_0(result)
    assert result.output.startswith("Usage:")


def test_dataset_help():
    from sleepless.scripts.dataset import dataset

    _check_help(dataset)


def test_dataset_list_help():
    from sleepless.scripts.dataset import list

    _check_help(list)


def test_dataset_list():
    from sleepless.scripts.dataset import list

    runner = CliRunner()
    result = runner.invoke(list)
    _assert_exit_0(result)
    assert result.output.startswith("Supported datasets:")


def test_dataset_check_help():
    from sleepless.scripts.dataset import check

    _check_help(check)


def test_main_help():
    from sleepless.scripts.cli import cli

    _check_help(cli)


def test_train_help():
    from sleepless.scripts.train import train

    _check_help(train)


def test_analyze_help():
    from sleepless.scripts.analyze import analyze

    _check_help(analyze)


def test_predict_help():
    from sleepless.scripts.predict import predict

    _check_help(predict)


def test_transform_help():
    from sleepless.scripts.preprocess import preprocess

    _check_help(preprocess)


def test_experiment_help():
    from sleepless.scripts.experiment import experiment

    _check_help(experiment)


def test_visualize_help():
    from sleepless.scripts.visualize import visualize

    _check_help(visualize)


def test_compare_help():
    from sleepless.scripts.compare import compare

    _check_help(compare)
