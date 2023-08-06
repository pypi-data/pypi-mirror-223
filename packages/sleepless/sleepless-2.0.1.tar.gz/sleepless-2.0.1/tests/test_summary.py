# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from sleepless.models.chambon2018 import SleepStagerChambon2018
from sleepless.utils.summary import summary


def test_summary_SleepStagerChambon2018():
    model = SleepStagerChambon2018(n_channels=2, sfreq=100)
    s, param = summary(model)
    assert isinstance(s, str)
    assert isinstance(param, int)
