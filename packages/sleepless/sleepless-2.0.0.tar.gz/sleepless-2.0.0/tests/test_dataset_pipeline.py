# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Test code for datasets."""


def test_dataset_pipelines(
    dataset_test, transform_dataset_1sample, transform_dataset_5samples
):
    assert len(dataset_test["train"]) == 1

    assert len(dataset_test["test"]) == 1

    assert hasattr(transform_dataset_1sample["train"][0], "features")

    assert hasattr(transform_dataset_1sample["test"][0], "features")

    assert len(transform_dataset_1sample["train"]) == 1

    assert len(transform_dataset_1sample["test"]) == 1

    assert hasattr(transform_dataset_5samples["train"][0], "features")

    assert hasattr(transform_dataset_5samples["test"][0], "features")

    assert len(transform_dataset_5samples["train"]) == 5

    assert len(transform_dataset_5samples["test"]) == 5
