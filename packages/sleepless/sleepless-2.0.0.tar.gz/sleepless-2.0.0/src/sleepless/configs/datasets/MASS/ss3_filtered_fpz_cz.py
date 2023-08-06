# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Montreal Archive of Sleep Studies (MASS)

This cohort comprises polysomnograms of 200 complete nights recorded
(SS1-SS5: 97 males aged 42.9 ± 19.8 years and 103 females aged 38.3 ± 18.9 years; total sample 40.6 ± 19.4 years, age range: 18-76 years).

All recordings feature a sampling frequency of 256 Hz and an electroencephalography (EEG) montage of
4-20 channels plus standard electro-oculography (EOG), electromyography (EMG), electrocardiogra- phy (ECG) and respiratory signals.

In this protocol all the raw data have been filtered with a pass band filter [0.3,30] Hz. Fpz-LER and Cz-LER have been computed respectively using the mean of (Fp1-LER and Fp2-LER), (C3-LER and C4-LER).
Then 2 Bipolar reference have been computed Fpz-Cz (Fpz-LER and Cz-LER) and Pz-Oz (Fpz-LER and Cz-LER)


* Reference: [MASS-2014]_
* Protocol ``ss3-filtered-fpz-cz``:

  * Train split: 38 (from SS3 subset)
  * Validation split: 12 (from SS3 subset)
  * Test split: 12 (from SS3 subset)
"""
from . import raw

dataset = raw.subsets("ss3-filtered-fpz-cz-100Hz")

dataset_as_test = {
    "mass_ss3_train": dataset["train"],
    "mass_ss3_validation": dataset["validation"],
    "mass_ss3_test": dataset["test"],
}
