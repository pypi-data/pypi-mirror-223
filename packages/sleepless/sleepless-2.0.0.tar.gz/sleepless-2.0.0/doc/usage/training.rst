.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
.. SPDX-FileContributor: Samuel Michel <samuel.michel@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _sleepless.usage.training:

========
Training
========

Run the following command-line :ref:`train <sleepless.cli>`
to train a model:

.. code:: sh

   sleepless train -vv <dataset> <model> -o <path/to/output_folder>

Replace ``<dataset>`` and ``<model>``  by the appropriate :ref:`configuration
files <sleepless.config>`.

Pytorch Model
-------------

To train a pytorch model, use the command-line interface (CLI) application ``sleepless
train``, available on your prompt.  To use this CLI, you must define the input
dataset that will be used to train, as well as the type of model that
will be trained and its parameters (See examples in :ref:`sleepless.config`). An output path must
be also defined, where the model weights and the training data will be stored.
You may issue ``sleepless train --help`` for a help message containing more detailed instructions.

.. tip::

   We strongly advice training with a GPU (using "cuda:0").
   Depending on the available GPU memory you might have to adjust your batch
   size.


Examples
========

To train Chambon CNN on the sc-edf dataset:

.. code:: sh

   sleepless train -vv sc_filtered chambon -o <path/to/output_folder>


Scikit-learn Model or Grid-search
---------------------------------

To train a scikit-learn model or grid-search use the command-line
interface (CLI) application ``sleepless train``, available on your prompt. To use
this CLI, you must define the input dataset that will be used to train the
model and its parameters, as well as the type of model that will be trained.
An output path must be also defined, where the model and the training data will be stored.

You may issue ``sleepless train --help`` for a help message containing more
detailed instructions.

Examples
========

To train a grid-search for a random forest model on the sc-edf dataset:

.. code:: sh

   sleepless train -vv sc_filtered rf-gs-mne -o <path/to/output_folder>

.. include:: ../links.rst
