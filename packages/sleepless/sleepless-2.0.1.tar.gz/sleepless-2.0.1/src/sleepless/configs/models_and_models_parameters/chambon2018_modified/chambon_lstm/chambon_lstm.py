# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Hybrid sleep staging architecture composed of Chambon model and lstm layer
parameters."""

from torch.nn import CrossEntropyLoss
from torch.optim import Adam
from torch.optim.lr_scheduler import MultiStepLR

from sleepless.models.chambon_lstm import SleepStagerChambon2018LSTM

from .....data.transforms import ToTorchDataset

# config
lr = 1e-3
weight_decay = 0
betas = (0.9, 0.999)
eps = 1e-08
weight_decay = 0
final_lr = 0.001
gamma = 1e-4
eps = 1e-9

scheduler_milestones = [30, 80]
scheduler_gamma = 0.1

sfreq = 100

n_channels = 2

model = SleepStagerChambon2018LSTM(
    n_channels=n_channels, sfreq=sfreq, n_classes=5, lstm_hidden_size=32
)

optimizer = Adam(model.parameters(), lr=lr, weight_decay=weight_decay)

criterion = CrossEntropyLoss()

scheduler = MultiStepLR(
    optimizer, milestones=scheduler_milestones, gamma=scheduler_gamma
)

model_parameters = {
    "transform": [
        ToTorchDataset(
            normalize=True, pick_chan=["Fpz-Cz", "Pz-Oz"], n_past_epochs=0
        )
    ],
    "optimizer": optimizer,
    "epochs": 100,
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
    "patience": 10,
}
