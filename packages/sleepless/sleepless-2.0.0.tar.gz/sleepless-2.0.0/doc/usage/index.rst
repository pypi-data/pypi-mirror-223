.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
.. SPDX-FileContributor: Samuel Michel <samuel.michel@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _sleepless.usage:

=======
 Usage
=======

This package supports a fully reproducible research experimentation cycle for
automatic sleep stages classification.

The following flowchart shows the global architecture of the package:

.. figure:: img/sleepless_architecture.jpg
   :width: 800 px

The package supports the following activities:

* Preprocessing: A directory can be set up to cache the 30-second windows (samples) after the preprocessing step,
                to avoid rerunning it every time a new experiment is performed.

* Training: 30s windows (samples) are fed to a model which is trained to output the prediction of the sleep stages.
            The package can handle models from _scikit-learn or _pytorch libraries.

* Prediction: The trained model is then used to generate a prediction for each 30s window (samples).

* Analysis: The samples predictions are then used to evaluate the model performance based on the labels provided by one or several annotators.

* Experiment: A script which run in series the training of the model, the predictions of all samples and the analysis to evaluate the model.

* Vizualize: A script to visualize the well/mis-classified samples and display it's corresponding raw signals.

* Compare: A script to compare 2 systems by generating table and plot


We provide :ref:`command-line interfaces (CLI) <sleepless.cli>` that implement
each of the phases above. This interface is configurable using :ref:`clapper's
extensible configuration framework <clapper.config>`.  In essence, each
command-line option may be provided as a variable with the same name in a
Python file.  Each file may combine any number of variables that are pertinent
to an application.

.. tip::

   For reproducibility, we recommend you stick to configuration files when
   parameterizing our CLI. Notice some of the options in the CLI interface
   (e.g. ``--dataset``) cannot be passed via the actual command-line as it
   may require complex Python types that cannot be synthetized in a single
   input parameter.

We provide a number of :ref:`preset configuration files <sleepless.config>` that
can be used in one or more of the activities described in this section. Our
command-line framework allows you to refer to these preset configuration files
using special names (a.k.a. "resources"), that procure and load these for you
automatically.


.. _sleepless.usage.commands:

Commands
--------

.. toctree::
   :maxdepth: 2

   preprocessing
   training
   predict
   analyze
   experiment
   visualize
   compare

.. include:: ../links.rst
