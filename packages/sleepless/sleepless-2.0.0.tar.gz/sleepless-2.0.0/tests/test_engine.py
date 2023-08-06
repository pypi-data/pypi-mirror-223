# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests the engine scripts."""

import copy
import os

import joblib
import numpy as np

from sklearn.linear_model import LinearRegression

from sleepless.data.sample import DelayedSample
from sleepless.engine.analyze import metric_stats
from sleepless.engine.predictor_scikit import predict_scikit
from sleepless.engine.trainer_scikit import train_scikit
from sleepless.engine.utils import load_from_hdf5


def test_train_test_linear_regression(tmp_path):
    path = str(tmp_path)

    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])

    delayed_sample_train = DelayedSample(
        None,
        features=X,
        label=(np.dot(X, np.array([1, 2])) + 3),
        key="key/train_sample",
    )

    expected = np.array([16])

    delayed_sample_test = DelayedSample(
        None, features=np.array([[3, 5]]), key="key/test_sample", label=expected
    )

    dataset = {"train": [delayed_sample_train], "test": [delayed_sample_test]}

    model = LinearRegression()

    train_scikit(model, dataset["train"], [], path, {})

    predict_scikit(dataset, joblib.load(path + "/fit_model"), path, {})

    dataset_out = load_from_hdf5(dataset, path, "prob")

    assert np.isclose(
        dataset_out["test"][0].output_prob, dataset_out["test"][0].label
    )


def test_engine_pipelines_rf(transform_dataset_5samples, tmp_path):
    from sklearn.ensemble import RandomForestClassifier as model

    path = str(tmp_path)

    train_scikit(model(), transform_dataset_5samples["train"], [], path, {})

    predict_scikit(
        transform_dataset_5samples, joblib.load(path + "/fit_model"), path, {}
    )

    dataset_out = load_from_hdf5(transform_dataset_5samples, path, "prob")

    dataset_out_modify = copy.deepcopy(dataset_out)

    for sample in dataset_out_modify["test"]:
        sample.output_prob[:, :] = 0

        sample.output_prob[:, 4] = 1

    figures_met_modify, _, zip_list_dic_modify = metric_stats(
        dataset_out_modify
    )

    figures_met, _, zip_list_dic = metric_stats(dataset_out)

    list_dic = list(zip(*zip_list_dic))[1]
    list_dic_modify = list(zip(*zip_list_dic_modify))[1]

    # to visually check, if metrics plot are correct
    from sleepless.utils.utils_fig_table_df import save_fig

    save_fig(str(tmp_path), figures_met_modify, "Plot_metrics_analyze_modif")
    save_fig(str(tmp_path), figures_met, "Plot_metrics_analyze")

    nb_samples = len(dataset_out["train"])

    nb_epochs = dataset_out["train"][0].output_prob.shape[0]

    for dic_metric_ in list_dic:
        for k, v in dic_metric_.items():
            if k.split(" ")[-1] in ["train", "test", "1", "2"]:
                assert v["Samples number"] == nb_samples
                assert v["Total number of epochs"] == (nb_samples * nb_epochs)

            else:
                assert v["Samples number"] == 1
                assert v["Total number of epochs"] == nb_epochs

            assert v["Accuracy score"] == 1
            assert v["Linear Weighted Kappa"] == 1
            assert v["Quadratic Weighted Kappa"] == 1
            assert v["Balanced accuracy"] == 1
            assert v["Mcc"] == 1
            assert v["Hamming Loss"] == 0

    for dic_metric_modify in list_dic_modify:
        for k, v in dic_metric_modify.items():
            if k.split(" ")[0] in ["test"]:
                if k.split(" ")[-1] in ["test", "1", "2"]:
                    assert v["Samples number"] == nb_samples
                    assert v["Total number of epochs"] == (
                        nb_samples * nb_epochs
                    )

                else:
                    assert v["Samples number"] == 1
                    assert v["Total number of epochs"] == nb_epochs

                assert v["Accuracy score"] < 0.1
                assert v["Linear Weighted Kappa"] == 0
                assert v["Quadratic Weighted Kappa"] == 0
                assert v["Balanced accuracy"] == 0.2
                assert v["Mcc"] == 0
                assert v["Hamming Loss"] > 0.9

    from sleepless.engine.analyze import misclassified_analyze

    fig_mis_modif, dic_miss_modif = misclassified_analyze(dataset_out_modify)
    fig_mis, dic_miss = misclassified_analyze(dataset_out)

    # to visually check, if misclassified plot are correct
    from sleepless.utils.utils_fig_table_df import save_fig

    save_fig(str(tmp_path), fig_mis_modif, "Plot_misclassified_Epochs_modif")
    save_fig(str(tmp_path), fig_mis, "Plot_misclassified_Epochs")

    nb_rem_stage = 125

    for k, v in dic_miss_modif.items():
        if "Train" in k:
            if "Well classified" in k:
                assert v["Epochs index"].shape == (nb_epochs,)

            else:
                assert v["Epochs index"].shape == (0,)

        if "Test" in k:
            if "Well classified" in k:
                assert v["Epochs index"].shape == (nb_rem_stage,)

            else:
                assert v["Epochs index"].shape == (nb_epochs - nb_rem_stage,)

    for k, v in dic_miss.items():
        if "Well classified" in k:
            assert v["Epochs index"].shape == (nb_epochs,)

        else:
            assert v["Epochs index"].shape == (0,)


def test_engine_torch_chambon(dataset_for_torch, tmp_path):
    from torch.nn import CrossEntropyLoss
    from torch.optim import Adam

    from sleepless.engine.predictor_torch import predict_torch
    from sleepless.engine.trainer_torch import train_torch
    from sleepless.models.chambon2018 import SleepStagerChambon2018

    output_fold = str(tmp_path)

    dataset, dataset_transformed = dataset_for_torch

    model = SleepStagerChambon2018(n_channels=2, sfreq=100)

    lr = 1e-3
    weight_decay = 0

    optimizer = Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    criterion = CrossEntropyLoss()

    model_parameters = {
        "optimizer": optimizer,
        "epochs": 10,
        "batch_size": 512,
        "valid_batch_size": 256,
        "batch_chunk_count": 1,
        "drop_incomplete_batch": True,
        "criterion": criterion,
        "scheduler": None,
        "checkpoint_period": 5,
        "device": "cpu",
        "seed": 42,
        "parallel": -1,
        "monitoring_interval": 10,
    }

    train_torch(
        model,
        dataset_transformed["train"],
        [dataset_transformed["validation"]],
        output_fold,
        model_parameters,
    )

    predict_torch(
        dataset_transformed,
        model,
        os.path.join(output_fold, "model_final_epoch.pth"),
        output_fold,
        model_parameters,
    )

    dataset_out = load_from_hdf5(dataset, output_fold, "prob")

    _, _, zip_list_dic = metric_stats(dataset_out)

    list_dic = list(zip(*zip_list_dic))[1]

    nb_epochs = dataset_out["train"][0].output_prob.shape[0]

    for dic_metric_ in list_dic:
        for k, v in dic_metric_.items():
            if k.split(" ") in [
                "train",
                "test",
                "validation",
            ]:
                assert v["Samples number"] == len(dataset_out[k])
                assert v["Total number of epochs"] == (
                    len(dataset_out[k]) * nb_epochs
                )

                assert v["Accuracy score"] >= 0.8
