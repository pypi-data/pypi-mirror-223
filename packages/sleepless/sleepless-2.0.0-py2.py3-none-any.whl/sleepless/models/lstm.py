# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import torch
import torch.nn as nn


class PlainLSTM(nn.Module):
    def __init__(self, config, hidden_dim, num_classes, dropout=0.25):
        super().__init__()
        self.config = config
        self.hidden_dim = hidden_dim
        self.num_layers = 3
        self.num_classes = num_classes
        self.bidirectional = config["bidirectional"]
        self.n_channels = 2

        self.input_dim = 2

        if self.n_channels > 1:
            self.spatial_conv = nn.Conv2d(
                1, self.n_channels, kernel_size=(self.n_channels, 1)
            )

        # architecture
        self.lstm = nn.LSTM(
            self.input_dim,
            self.hidden_dim,
            batch_first=True,
            num_layers=self.num_layers,
            bidirectional=config["bidirectional"],
        )
        self.fc = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(
                self.hidden_dim * (2 if self.bidirectional else 1),
                self.num_classes,
            ),
        )

    def init_hidden(self, x):
        h0 = torch.zeros(
            (
                self.num_layers * (2 if self.bidirectional else 1),
                x.size(0),
                self.hidden_dim,
            )
        )
        c0 = torch.zeros(
            (
                self.num_layers * (2 if self.bidirectional else 1),
                x.size(0),
                self.hidden_dim,
            )
        )
        return h0, c0

    def forward(self, x):
        hidden = self.init_hidden(x)
        x = x.transpose(1, 2)
        out, hidden = self.lstm(x, hidden)

        out_f = out[:, -1, : self.hidden_dim]
        out_b = out[:, 0, self.hidden_dim :]
        out = torch.cat((out_f, out_b), dim=1)
        out = self.fc(out.flatten(start_dim=1))
        return out
