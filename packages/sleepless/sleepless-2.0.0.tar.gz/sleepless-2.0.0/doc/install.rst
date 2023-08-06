.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
.. SPDX-FileContributor: Samuel Michel <samuel.michel@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _sleepless.install:


==============
 Installation
==============

We support two installation modes, through pip_, or mamba_ (conda).


.. tab:: pip

   Stable, from PyPI:

   .. code:: sh

      pip install sleepless

   Latest beta, from GitLab package registry:

   .. code:: sh

      pip install --pre --index-url https://gitlab.idiap.ch/api/v4/groups/bob/-/packages/pypi/simple --extra-index-url https://pypi.org/simple sleepless

   .. tip::

      To avoid long command-lines you may configure pip to define the indexes
      and package search priorities as you like.


.. tab:: mamba/conda

   Stable:

   .. code:: sh

      mamba install -c https://www.idiap.ch/software/biosignal/conda -c conda-forge sleepless

   Latest beta:

   .. code:: sh

      mamba install -c https://www.idiap.ch/software/biosignal/conda/label/beta -c conda-forge sleepless


.. _sleepless.setup:

Setup
-----

A configuration file may be useful to setup global options that should be often
reused.  The location of the configuration file depends on the value of the
environment variable ``$XDG_CONFIG_HOME``, but defaults to
``~/.config/sleepless.toml``.  You may edit this file using your preferred
editor.

Here is an example configuration file that may be useful as a starting point:

.. code:: toml

   [datadir]
   EDF = "/Users/myself/dbs/EDF"
   MASS = "/Users/myself/dbs/MASS"


.. tip::

   To get a list of valid data directories that can be configured, execute:

   .. code:: sh

      sleepless dataset list

   You must procure and download datasets by yourself.  The raw data is not
   included in this package as we are not authorised to redistribute it.

   To check whether the downloaded version is consistent with the structure
   that is expected by this package, run:

   .. code:: sh

      sleepless dataset check EDF

.. _sleepless.setup.datasets:

Supported Datasets
==================

Here is a list of currently supported datasets in this package, alongside
notable properties.  Each dataset name is linked to the location where raw data
can be downloaded.

.. list-table::
   :header-rows: 1

   * - Datasets
     - EEG channels
     - EOG channels
     - EMG channels
     - Annotation method
     - Train
     - Validation
     - Test
     - Reference
   * - ST-EDF
     - 3
     - 1
     - 1
     - R&K
     - 28
     - 8
     - 8
     - [SLEEP_EDF-2018]_
   * - SC-EDF
     - 3
     - 1
     - 1
     - R&K
     - 97
     - 28
     - 28
     - [SLEEP_EDF-2018]_
   * - _SS3-MASS
     - 20
     - 2
     - 3
     - AASM
     - 33
     - 10
     - 10
     - [MASS-2014]_


.. include:: links.rst
