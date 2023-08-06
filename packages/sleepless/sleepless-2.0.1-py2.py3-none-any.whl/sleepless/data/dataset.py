# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import csv
import importlib.abc
import json
import logging
import os
import pathlib
import typing

from collections.abc import Mapping

from .sample import DelayedSample

logger = logging.getLogger(__name__)


class JSONDataset:
    """Generic multi-protocol/subset filelist dataset that yields samples.

    To create a new dataset, you need to provide one or more JSON formatted
    filelists (one per protocol) with the following contents:

    .. code-block:: json

       {
           "subset1": [
               [
                   "value1",
                   "value2",
                   "value3"
               ],
               [
                   "value4",
                   "value5",
                   "value6"
               ]
           ],
           "subset2": [
           ]
       }

    Your dataset many contain any number of subsets, but all sample entries
    must contain the same number of fields.


    :param protocols: Paths to one or more JSON formatted files containing the various
                        protocols to be recognized by this dataset, or a dictionary, mapping
                        protocol names to paths (or opened file objects) of CSV files.
                        Internally, we save a dictionary where keys default to the basename of
                        paths (list input).

    :param fieldnames: An iterable over the field names (strings) to assign to each entry in
                        the JSON file.  It should have as many items as fields in each entry of
                        the JSON file.

    :param loader: A function that receives as input, a context dictionary (with at least
                    a "protocol" and "subset" keys indicating which protocol and subset are
                    being served), and a dictionary with ``{fieldname: value}`` entries,
                    and returns an object with at least 2 attributes:

                        * ``key``: which must be a unique string for every sample across
                                    subsets in a protocol, and
                        * ``data``: which contains the data associated witht this sample
    """

    _protocols: dict[
        str,
        tuple[
            str | pathlib.Path | importlib.abc.Traversable,
            Mapping,
        ],
    ]

    def __init__(
        self,
        protocols: typing.Iterable[
            tuple[
                str | pathlib.Path | importlib.abc.Traversable,
                Mapping,
            ]
        ]
        | dict[
            str,
            tuple[
                str | pathlib.Path | importlib.abc.Traversable,
                Mapping,
            ],
        ],
        fieldnames: typing.Iterable[str],
        loader: typing.Callable,
    ) -> None:
        if isinstance(protocols, dict):
            self._protocols = protocols
        else:
            self._protocols = {
                os.path.splitext(os.path.basename(str(k)))[0]: k
                for k in protocols
            }
        self.fieldnames = fieldnames
        self._loader = loader

    def check(self, limit: int = 0) -> int:
        """For each protocol, check if all data can be correctly accessed.

        This function assumes each sample has a ``data`` and a ``key``
        attribute.  The ``key`` attribute should be a string, or representable
        as such.

        :param limit: Maximum number of samples to check (in each protocol/subset
                        combination) in this dataset.  If set to zero, then check
                        everything.

        :return: Number of errors during check
        """
        logger.info("Checking dataset...")
        errors = 0
        for proto in self._protocols:
            logger.info(f"Checking protocol '{proto}'...")
            for name, samples in self.subsets(proto).items():
                logger.info(f"Checking subset '{name}'...")
                if limit:
                    logger.info(f"Checking at most first '{limit}' samples...")
                    samples = samples[:limit]
                for pos, sample in enumerate(samples):
                    try:
                        sample.data  # may trigger data loading
                        logger.info(f"{sample.key}: OK")
                    except Exception as e:
                        logger.error(
                            f"Found error loading entry {pos} in subset {name} "
                            f"of protocol {proto} from file "
                            f"'{self._protocols[proto]}': {e}"
                        )
                        errors += 1
        return errors

    def subsets(self, protocol: str) -> dict[str, list[DelayedSample]]:
        """Returns all subsets in a protocol.

        This method will load JSON information for a given protocol and return
        all subsets of the given protocol after converting each entry through
        the loader function.

        Parameters:

        :param protocol: Name of the protocol data to load

        :return: A dictionary mapping subset names to lists of objects (respecting
                    the ``key``, ``data`` interface).
        """
        fileobj, preproc_params = self._protocols[protocol]
        if isinstance(
            fileobj, (str, bytes, pathlib.Path, importlib.abc.Traversable)
        ):
            with open(str(fileobj)) as f:
                data = json.load(f)
        else:
            data = json.load(fileobj)
            fileobj.seek(0)

        csv_subset = protocol.split("-")[0]

        protoc_loader = self._loader(preproc_params, csv_subset, protocol)

        retval = {}
        for subset, samples in data.items():
            retval[subset] = [
                protoc_loader._loader(
                    dict(protocol=protocol, subset=subset, order=n),
                    dict(zip(self.fieldnames, k)),
                )
                for n, k in enumerate(samples)
            ]

        return retval


class CSVDataset:
    """Generic multi-subset filelist dataset that yields samples.

    To create a new dataset, you only need to provide a CSV formatted filelist
    using any separator (e.g. comma, space, semi-colon) with the following
    information:

    .. code-block:: text

       value1,value2,value3
       value4,value5,value6
       ...

    Notice that all rows must have the same number of entries.

    :param subsets:
        Paths to one or more CSV formatted files containing the various subsets
        to be recognized by this dataset, or a dictionary, mapping subset names
        to paths (or opened file objects) of CSV files.  Internally, we save a
        dictionary where keys default to the basename of paths (list input).

    :param fieldnames: An iterable over the field names (strings) to assign to each column in
                        the CSV file. It should have as many items as fields in each row of
                        the CSV file(s).

    :param loader: A function that receives as input, a context dictionary (with, at
                    least, a "subset" key indicating which subset is being served), and a
                    dictionary with ``{key: path}`` entries, and returns a dictionary with
                    the loaded data.
    """

    _subsets: dict[str, str]

    def __init__(
        self,
        subsets: typing.Iterable[str] | dict[str, str],
        fieldnames: typing.Iterable[str],
        loader: typing.Callable,
    ) -> None:
        if isinstance(subsets, dict):
            self._subsets = subsets
        else:
            self._subsets = {
                os.path.splitext(os.path.basename(k))[0]: k for k in subsets
            }
        self.fieldnames = fieldnames
        self._loader = loader

    def check(self, limit: int = 0) -> float:
        """For each subset, check if all data can be correctly accessed.

        This function assumes each sample has a ``data`` and a ``key``
        attribute.  The ``key`` attribute should be a string, or representable
        as such.

        :param limit: Maximum number of samples to check (in each protocol/subset
                        combination) in this dataset.  If set to zero, then check
                        everything.

        :return: Number of errors during check
        """
        logger.info("Checking dataset...")
        errors = 0
        for name in self._subsets.keys():
            logger.info(f"Checking subset '{name}'...")
            samples = self.samples(name)
            if limit:
                logger.info(f"Checking at most first '{limit}' samples...")
                samples = samples[:limit]
            for pos, sample in enumerate(samples):
                try:
                    sample.data  # may trigger data loading
                    logger.info(f"{sample.key}: OK")
                except Exception as e:
                    logger.error(
                        f"Found error loading entry {pos} in subset {name} "
                        f"from file '{self._subsets[name]}': {e}"
                    )
                    errors += 1
        return errors

    def subsets(self) -> dict[str, list[DelayedSample]]:
        """Returns all available subsets at once.

        :return: A dictionary mapping subset names to lists of objects (respecting
                    the ``key``, ``data`` interface).
        """
        return {k: self.samples(k) for k in self._subsets.keys()}

    def samples(self, subset: str) -> list[DelayedSample]:
        """Returns all samples in a subset.

        This method will load CSV information for a given subset and return
        all samples of the given subset after passing each entry through the
        loading function.

        :param subset: Name of the subset data to load

        :return: A lists of objects (respecting the ``key``, ``data`` interface).
        """
        fileobj = self._subsets[subset]
        if isinstance(fileobj, (str, bytes, pathlib.Path)):
            with open(self._subsets[subset], newline="") as f:
                cf = csv.reader(f)
                samples = [k for k in cf]
        else:
            cf = csv.reader(fileobj)
            samples = [k for k in cf]
            fileobj.seek(0)

        return [
            self._loader(
                dict(subset=subset, order=n), dict(zip(self.fieldnames, k))
            )
            for n, k in enumerate(samples)
        ]
