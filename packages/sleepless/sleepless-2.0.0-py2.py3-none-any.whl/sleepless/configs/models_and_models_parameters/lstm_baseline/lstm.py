# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Baseline LSTM layer model."""

from torch.nn import CrossEntropyLoss
from torch.optim import Adam
from torch.optim.lr_scheduler import MultiStepLR

# from sleepless.configs.models_and_models_parameters.lstm_baseline.lstm2 import model
from sleepless.data.transforms import ToTorchDataset

# from torch.optim import SGD
from sleepless.models.lstm import PlainLSTM

# config
lr = 1e-3
weight_decay = 0
betas = (0.9, 0.999)
eps = 1e-08
weight_decay = 0
final_lr = 0.1
gamma = 1e-3
eps = 1e-8

scheduler_milestones = [900]
scheduler_gamma = 0.1

sfreq = 100

n_channels = 2

configs = {
    "max_epochs": 500,
    "dataset": "Sleep-EDF",
    "signal_type": "Fpz-Cz",
    "sampling_rate": 100,
    "seq_len": 1,
    "target_idx": -1,
    "n_splits": 20,
    # "hidden_dim": 128,
    "batch_size": 128,
    "patience": 10,
    "num_layers": 50,
    "dropout_rate": 0.25,
    "num_classes": 5,
    "early_stopping_mode": "min",
    "bidirectional": False,
    "learning_rate": 0.000005,
    "weight_decay": 0.000001,
}

model = PlainLSTM(configs, hidden_dim=128, num_classes=5)

optimizer = Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
criterion = CrossEntropyLoss()

scheduler = MultiStepLR(
    optimizer, milestones=scheduler_milestones, gamma=scheduler_gamma
)

model_parameters = {
    "transform": [
        ToTorchDataset(normalize=True, pick_chan=["Fpz-Cz", "Pz-Oz"])
    ],
    "optimizer": optimizer,
    "epochs": 1,
    "batch_size": 128,
    "valid_batch_size": 128,
    "batch_chunk_count": 1,
    "drop_incomplete_batch": True,
    "criterion": criterion,
    "scheduler": scheduler,
    "checkpoint_period": 5,
    "device": "cpu",
    "seed": 42,
    "parallel": -1,
    "monitoring_interval": 10,
}
