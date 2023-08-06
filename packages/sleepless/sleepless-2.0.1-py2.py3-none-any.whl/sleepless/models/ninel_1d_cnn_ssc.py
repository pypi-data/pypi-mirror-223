# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from torch import nn


class _CnnBlock(nn.Module):
    """Convolutional neural network block, composed of 1d-cnn layer, one batch
    normalization layer and one ReLu activation layer.

    Parameters
    ----------
    n_channels : int
        Number of input channels.

    n_out : int
        Number of output channels.

    kernel_size_cnn : int
        kernel size

    stride_cnn : int
        stride size

    padding_cnn : int
        padding size
    """

    def __init__(
        self,
        n_channels: int,
        n_out: int,
        kernel_size_cnn: int | tuple,
        stride_cnn: int,
        padding_cnn: int | str = 0,
    ):
        super().__init__()

        self.cnn = nn.Sequential(
            nn.Conv1d(
                in_channels=n_channels,
                out_channels=n_out,
                kernel_size=kernel_size_cnn,
                stride=stride_cnn,
                padding=padding_cnn,
            ),
            nn.BatchNorm1d(num_features=n_out),
            nn.ReLU(),
        )

    def forward(self, x):
        x = self.cnn(x)
        return x


class NineL_1DCNN_SSC(nn.Module):
    """Sleep staging architecture from [Satapathy-2023]_. Convolutional neural
    network for sleep staging described in [Satapathy-2023]_.

    Parameters
    ----------
    n_channels : int
        Number of EEG channels.

    n_classes : int
        Number of classes.

    n_hidden_state : int
        output size of the feature extractor

    References
    ----------
    .. [Satapathy-2023]_
    """

    def __init__(self, n_channels: int, n_hidden_state: int, n_classes: int):
        super().__init__()

        self.cnn1 = _CnnBlock(n_channels, n_hidden_state * 16, 8, 4, 2)
        self.mp1 = nn.MaxPool1d(2, 2)

        self.feature_extractor = nn.Sequential(
            _CnnBlock(n_hidden_state * 16, n_hidden_state * 32, 3, 1, 1),
            nn.MaxPool1d(2, 2),
            _CnnBlock(n_hidden_state * 32, n_hidden_state * 64, 3, 1, 1),
            nn.MaxPool1d(2, 2),
            _CnnBlock(n_hidden_state * 64, n_hidden_state * 64, 3, 1, 1),
            nn.MaxPool1d(2, 2),
            _CnnBlock(n_hidden_state * 64, n_hidden_state * 64, 3, 1, 1),
            nn.MaxPool1d(2, 2),
            _CnnBlock(n_hidden_state * 64, n_hidden_state * 64, 3, 1, 1),
            nn.MaxPool1d(2, 2),
            _CnnBlock(n_hidden_state * 64, n_hidden_state * 64, 3, 1, 1),
            nn.MaxPool1d(2, 2),
            _CnnBlock(n_hidden_state * 64, n_hidden_state * 64, 3, 1, 1),
            nn.MaxPool1d(2, 2),
            _CnnBlock(n_hidden_state * 64, n_hidden_state * 64, 3, 1, 1),
            nn.MaxPool1d(2, 2),
        )

        self.classifier = nn.Sequential(
            nn.Linear(n_hidden_state * 64, 100),
            nn.ReLU(),
            nn.Linear(100, n_classes),
        )

    def forward(self, x):
        """Forward pass.

        :param x: Batch of signals windows of shape (batch_size,
            n_channels, n_times).
        """
        if len(x) == 2:
            x = x.unsqueeze(1)

        x = self.cnn1(x)
        x = self.mp1(x)
        features = self.feature_extractor(x).flatten(start_dim=1)
        x = self.classifier(features)

        return x, features
