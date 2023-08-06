.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
.. SPDX-FileContributor: Samuel Michel <samuel.michel@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _sleepless.usage.predict:

=======
Predict
=======

In prediction mode, we input data, the trained model with its weights, and output
probabilities prediction which are stored in h5py files.

You may issue ``sleepless predict --help`` for a help message containing more
detailed instructions.


To run predictions, use the sub-command :ref:`predict <sleepless.cli>` to run
prediction on an existing dataset:

.. code:: sh

   sleepless predict -vv <model> <dataset> -w <path/to/model.pth>  -o <path/to/output_folder>


Replace ``<model>`` and ``<dataset>`` by the appropriate :ref:`configuration
files <sleepless.config>`.  Replace ``<path/to/model.pth>`` to a path leading to
the model weights.

Examples
========

To predict with the trained Chambon CNN on the sc-edf dataset:

.. code:: sh

   sleepless train -vv sc_filtered chambon -w <path/to/model.pth> -o <path/to/output_folder>

.. include:: ../links.rst
