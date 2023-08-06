.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
.. SPDX-FileContributor: Samuel Michel <samuel.michel@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _sleepless.api:

============
 Python API
============

This section includes information for using the Python API of
``sleepless``.


.. To update these lists, run the following command on the root of the package:
.. find src -name '*.py' | sed -e 's#/#.#g;s#.py$##g;s#.__init__##g' | sort
.. You may apply further filtering to update only one of the subsections below


Data Manipulation
-----------------

.. autosummary::
   :toctree: api/data

   sleepless.data.dataset
   sleepless.data.loader
   sleepless.data.utils
   sleepless.data.sample
   sleepless.data.transforms
   sleepless.configs.datasets


.. _sleepless.api.data.raw:

Raw Dataset Access
------------------

Direct data-access through iterators.

.. autosummary::
   :toctree: api/data/raw

   sleepless.data.EDF
   sleepless.data.MASS


.. _sleepless.api.models:

Models
------

CNN and other models implemented.

.. autosummary::
   :toctree: api/models

   sleepless.models.chambon2018
   sleepless.models.ninel_1d_cnn_ssc

.. _sleepless.api.engines:

Command engines
---------------

Functions to actuate on the data.

.. autosummary::
   :toctree: api/engine

   sleepless.engine.trainer_scikit
   sleepless.engine.predictor_scikit
   sleepless.engine.trainer_torch
   sleepless.engine.predictor_torch
   sleepless.engine.analyze


.. _sleepless.api.utils:

Various utilities
-----------------

Reusable auxiliary functions.

.. autosummary::
   :toctree: api/utils

   sleepless.utils.checkpointer
   sleepless.utils.matplotlib_utils
   sleepless.utils.misclassification
   sleepless.utils.stats_protocol
   sleepless.utils.rc
   sleepless.utils.resources
   sleepless.utils.summary
   sleepless.utils.utils_fig_table_df


.. include:: links.rst
