.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
.. SPDX-FileContributor: Samuel Michel <samuel.michel@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _sleepless.usage.visualize:

=========
Visualize
=========

The goal of the visualize script is to help the user analyzing the results,
by providing interactive plotting of mis/well-classified epochs and visualizing
it's respective raw data in another window by selecting a epochs on the figure.

While launching the script this first figure appears:

.. figure:: img/fig_wellclass_epochs.jpg
   :width: 800 px

By selecting an epoch on the previous figure the next window with the raw data will open.

.. figure:: img/raw_data.jpg
   :width: 800 px

You can also select another epoch, the raw data window will update.

You may issue ``sleepless visualize --help`` for a help message containing more
detailed instructions.

To visualize predictions for one specific psg file, use the sub-command :ref:`visualize <sleepless.cli>`:

.. code:: sh

   sleepless visualize -vv <dataset> -p <path/to/predictions> -s <subset> -n <sample> -t <type> -o <path/to/output_folder>


Replace ``<dataset>`` by the appropriate :ref:`configuration
files <sleepless.config>`.  Replace ``<path/to/predictions>`` with a path leading to
the model predictions. Replace ``<path/to/output_folder>`` with a path where the tables and plot
from the analysis will be stored, and choose a subset and a patient number by replacing <subset> and <sample>.
replace <type> by one of the following options: misclassified, wellclassified.


.. include:: ../links.rst
