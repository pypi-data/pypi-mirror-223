.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
.. SPDX-FileContributor: Samuel Michel <samuel.michel@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _sleepless.usage.preprocessing:

=============
Preprocessing
=============

To earn time while running experiments the samples can be cached in a local
directory after the preprocessing steps.

To setup this feature you can just add the following line
in the ``~/.config/sleepless.toml`` file:

.. code:: toml

   [cachedatadir]
   EDF = "/Users/myself/preproc_data/EDF"
   MASS = "/Users/myself/preproc_data/MASS"

Then run the following command to cache
the samples.

.. code-block:: sh

   $ sleepless <dataset> -vv

Replace ``<dataset>`` by the appropriate :ref:`configuration
files <sleepless.config>`.


Examples
========

.. code-block:: sh

   $ sleepless stedf-unfiltered -vv

The next time you run a script with the ``stedf-unfiltered`` dataset,
the cached samples will be loaded.

.. warning::

   If any preprocessing steps get modified, you need to delete the directory where samples are cached and
   recompute the preprocessing


.. include:: ../links.rst
