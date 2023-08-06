# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Chambon2018.

Reference: [Chambon-2018]_
"""

from torch.nn import CrossEntropyLoss
from torch.optim import Adam

from sleepless.data.transforms import ToTorchDataset
from sleepless.models.chambon2018 import SleepStagerChambon2018

# config
lr = 1e-4
betas = (0.9, 0.999)
eps = 1e-08
weight_decay = 0


scheduler_milestones = [300]
scheduler_gamma = 0.1

sfreq = 100

n_channels = 3

model = SleepStagerChambon2018(
    n_channels=n_channels, sfreq=sfreq, n_classes=5, dropout=0.5
)

optimizer = Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
criterion = CrossEntropyLoss()

scheduler = None

model_parameters = {
    "transform": [
        ToTorchDataset(
            normalize=True,
            pick_chan=["Fpz-Cz", "Pz-Oz", "horizontal"],
        )
    ],
    "optimizer": optimizer,
    "epochs": 300,
    "patience": 50,
    "batch_size": 128,
    "valid_batch_size": 128,
    "batch_chunk_count": 1,
    "drop_incomplete_batch": True,
    "criterion": criterion,
    "scheduler": scheduler,
    "checkpoint_period": 5,
    "device": "cuda:0",
    "seed": 42,
    "parallel": -1,
    "monitoring_interval": 10,
}
