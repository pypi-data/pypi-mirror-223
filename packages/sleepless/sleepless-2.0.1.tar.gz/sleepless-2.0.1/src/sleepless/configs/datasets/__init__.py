# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Script for dataset config."""

from __future__ import annotations

from ...data.sample import DelayedSample


def make_dataset(
    subsets: dict[str, list[DelayedSample]], transforms: list[object]
) -> dict[str, list[DelayedSample]]:
    """Creates a new configuration dataset from dictionary and transforms Take
    the subset of a database and apply on it a list of transforms.

    :param subsets: A subset of a database; dictionary containing a
        train and a test set.
    :param transforms: A list of transforms that needs to be applied to
        all samples.
    :param dataset: A new subset dictionary containing a train and a
        test set but where data have been transform through the
        transform pipeline.
    """

    from ...data.utils import ComposeTransform

    compose_transform = ComposeTransform(transforms)

    retval = {}

    for key in subsets.keys():
        retval[key] = compose_transform(subsets[key])

    return retval
