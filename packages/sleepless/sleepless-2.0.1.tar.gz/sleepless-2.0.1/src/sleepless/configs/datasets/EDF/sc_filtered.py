# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Sleep-EDF (expanded) dataset for sleep analysis.

The database includes 197 all night PSGs recording in 2 subsets (SC and ST):

ST contains 44 PSG (9-hours-night) of 22 Caucasian (between  18-79 years old),
healthy (without medication) but with difficulty to fall asleep.

SC contains 153 PSG (20 hours) of 78 Caucasian (between  25-101 years old),
healthy (without medication)

In this protocol all the raw data have been filtered with a pass band filter [0.3,30] Hz.

* Reference: [SLEEP_EDF-2018]_
* Protocol ``sc-filtered``:

  * Train split: 97 (from Sc subset)
  * Validation split: 28 (from SC subset)
  * Test split: 28 (from SC subset)
"""

from . import raw

dataset = raw.subsets("sc-filtered")

dataset_as_test = {
    "edf_sc_train": dataset["train"],
    "edf_sc_validation": dataset["validation"],
    "edf_sc_test": dataset["test"],
}
