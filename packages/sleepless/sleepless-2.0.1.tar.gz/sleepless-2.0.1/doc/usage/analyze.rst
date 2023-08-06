.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
.. SPDX-FileContributor: Samuel Michel <samuel.michel@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _sleepless.usage.analyze:

=======
Analyze
=======

The analyze script, evaluate the model predictions and compare it with the
labels from one or several annotators. The script generates metrics tables and plots of confusion matrixes
for each subset defined in the protocol.

You may issue ``sleepless analyze --help`` for a help message containing more
detailed instructions.

To run analysis, use the sub-command :ref:`analyze <sleepless.cli>`:

.. code:: sh

   sleepless analyze -vv <dataset> -p <path/to/predictions> -o <path/to/output_folder>


Replace ``<dataset>`` by the appropriate :ref:`configuration
files <sleepless.config>`.  Replace ``<path/to/predictions>`` with a path leading to
the model predictions. Replace ``<path/to/output_folder>`` with a path where the tables and plot
from the analysis will be stored.


.. include:: ../links.rst
