.. Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _sleepless.config:

Preset Configurations
---------------------

This module contains preset configurations for baseline architectures and
datasets.


.. _sleepless.configs.models:

Models
======

.. autosummary::
   :toctree: api/configs/models
   :template: config.rst

.. _sleepless.configs.models_and_models_parameters:

Pytorch Models
==============

.. autosummary::
   :toctree: api/configs/models_and_models_parameters
   :template: config.rst

   sleepless.configs.models_and_models_parameters.chambon2018_baseline.chambon2018
   sleepless.configs.models_and_models_parameters.chambon2018_baseline.chambon2018_noscheduler
   sleepless.configs.models_and_models_parameters.chambon2018_modified.chambon_lstm.chambon_lstm
   sleepless.configs.models_and_models_parameters.lstm_baseline.lstm
   sleepless.configs.models_and_models_parameters.blanco_baseline.blanco
   sleepless.configs.models_and_models_parameters.chambon2018_modified.chambon_gru.chambon_gru
   sleepless.configs.models_and_models_parameters.nine_layers_cnn_baseline.ninel_1d_cnn_ssc

.. _sleepless.configs.scikit_learn_model:

Scikit-learn Models (with grid-search)
======================================

.. autosummary::
   :toctree: api/configs/grid_search
   :template: config.rst

   sleepless.configs.models_and_models_parameters.mne_baseline.randomforest
   sleepless.configs.models_and_models_parameters.chambon2018_baseline.randomforest
   sleepless.configs.models_and_models_parameters.chambon2018_baseline.randomforest_2eeg_eog
   sleepless.configs.models_and_models_parameters.chambon2018_baseline.randomforest_2eeg_emg
   sleepless.configs.models_and_models_parameters.chambon2018_baseline.randomforest_2eeg_eog_emg
   sleepless.configs.models_and_models_parameters.chambon2018_baseline.randomforest_eog
   sleepless.configs.models_and_models_parameters.chambon2018_baseline.randomforest_emg
   sleepless.configs.models_and_models_parameters.chambon2018_baseline.randomforest_fpzcz
   sleepless.configs.models_and_models_parameters.chambon2018_baseline.randomforest_pzoz
   sleepless.configs.models_and_models_parameters.mne_baseline.xgboost
   sleepless.configs.models_and_models_parameters.chambon2018_baseline.xgboost_chambon
   sleepless.configs.models_and_models_parameters.mne_baseline.gbc

.. _sleepless.configs.datasets:

Datasets
========

Datasets include iterative accessors to raw data
(:ref:`sleepless.setup.datasets`) including data pre-processing and
augmentation, if applicable.  Use these datasets for training and evaluating
your models.


.. autosummary::
   :toctree: api/configs/datasets
   :template: config.rst


   sleepless.configs.datasets.EDF.sc_filtered
   sleepless.configs.datasets.EDF.st_filtered
   sleepless.configs.datasets.EDF.sc_unfiltered
   sleepless.configs.datasets.EDF.st_unfiltered
   sleepless.configs.datasets.EDF.sc_filtered_crop_wake

   sleepless.configs.datasets.EDF.train_sc_filtered
   sleepless.configs.datasets.EDF.train_st_filtered
   sleepless.configs.datasets.EDF.train_st_sc_filtered

   sleepless.configs.datasets.MASS.ss3_unfiltered_fpz_cz
   sleepless.configs.datasets.MASS.ss3_filtered_fpz_cz


   sleepless.configs.datasets.EDF_X_MASS.train_edf_sc
   sleepless.configs.datasets.EDF_X_MASS.train_edf_st
   sleepless.configs.datasets.EDF_X_MASS.train_edf_st_sc
   sleepless.configs.datasets.EDF_X_MASS.train_edf_sc_crop_wake
   sleepless.configs.datasets.EDF_X_MASS.train_mass_ss3

   sleepless.configs.datasets.mixed_all_db.mixed_all_db

.. include:: links.rst
