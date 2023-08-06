.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
.. SPDX-FileContributor: Samuel Michel <samuel.michel@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _sleepless.usage.experiment:

==========
Experiment
==========

The experiment script will run in series the :ref:`train <sleepless.cli>`, :ref:`predict <sleepless.cli>`, :ref:`analyze <sleepless.cli>`

To run an experiment, use the sub-command :ref:`experiment <sleepless.cli>`:

.. code:: sh

   sleepless experiment -vv <model> <dataset> -o <path/to/output_folder>


Replace ``<model>`` and ``<dataset>`` by the appropriate :ref:`configuration
files <sleepless.config>`. ``<path/to/output_folder>`` an output folder also need to be defined to store,
the trained model, the predictions and the analysis tables and plots.

Examples
========

To run an experiment (training, prediction and evaluation) on the cross-dataset protocol EDF-MASSA with the Chambon CNN model
with no scheduler:

.. code:: sh

   sleepless experiment -vv edf-massa rf-gs-mne chambon-noscheduler -o <path/to/output_folder>

.. include:: ../links.rst
