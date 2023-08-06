# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Nine-layers-CNN.

Reference: [Satapathy-2023]_
"""

from torch.nn import CrossEntropyLoss
from torch.optim import Adam

from ....data.transforms import ToTorchDataset
from ....models.ninel_1d_cnn_ssc import NineL_1DCNN_SSC

# config
lr = 2e-6
weight_decay = 0
betas = (0.9, 0.999)
eps = 1e-08


scheduler_milestones = [300]
scheduler_gamma = 0.1

sfreq = 100

n_channels = 3

n_hidden_state = 1

model = NineL_1DCNN_SSC(
    n_channels=n_channels, n_hidden_state=n_hidden_state, n_classes=5
)

optimizer = Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
criterion = CrossEntropyLoss()

scheduler = None

model_parameters = {
    "transform": [
        ToTorchDataset(
            normalize=True, pick_chan=["Fpz-Cz", "Pz-Oz", "horizontal"]
        )
    ],
    "optimizer": optimizer,
    "epochs": 300,
    "batch_size": 50,
    "valid_batch_size": 50,
    "batch_chunk_count": 1,
    "drop_incomplete_batch": True,
    "criterion": criterion,
    "scheduler": scheduler,
    "checkpoint_period": 5,
    "device": "cuda:0",
    "seed": 42,
    "parallel": -1,
    "monitoring_interval": 10,
    "patience": 50,
}
