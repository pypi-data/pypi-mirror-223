.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
.. SPDX-FileContributor: Samuel Michel <samuel.michel@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _sleepless.usage.compare:

=======
Compare
=======

The compare script, compare a list of system using the aggregated balanced accuracy, which is a cross-dataset,
evaluation protocol. An example of this evaluation protocol can be seen on the following figure.

.. figure:: img/evaluation_protocol.jpg
   :width: 800 px

The aggreagted method is the weighted average, where the weights are the number of 30s-window (name epoch in the package) in the subset.

You may issue ``sleepless compare --help`` for a help message containing more
detailed instructions.

To compare systems A and B, use the sub-command :ref:`compare <sleepless.cli>` to generate table and plot to compare
both systems:

.. code:: sh

   sleepless compare -vv <A> <path/to/A/metric_table.csv> <B> <path/to/B/metric_table.csv> -o <path/to/output_folder>


Replace ``<A>`` and ``<B>`` by the names you want to give to each system, and ``<path/to/A/metric_table.csv>`` and ``<path/to/B/metric_table.csv>``
by the respective paths to the csv metrics table of each system.

You can compare more than 2 systems by following the same pattern (name + path).


.. include:: ../links.rst
