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
* Protocol ``st-filtered``:

  * Train split: 28 (from ST subset)
  * Validation split: 8 (from ST subset)
  * Test split: 8 (from ST subset)
"""

from . import raw

dataset = raw.subsets("st-filtered")

dataset_as_test = {
    "edf_st_train": dataset["train"],
    "edf_st_validation": dataset["validation"],
    "edf_st_test": dataset["test"],
}
