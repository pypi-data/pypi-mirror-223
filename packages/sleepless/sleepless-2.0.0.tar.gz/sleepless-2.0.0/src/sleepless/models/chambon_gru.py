# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# SPDX-FileCopyrightText: Copyright (c) 2017-2020 Braindecode Developers
#
# SPDX-FileContributor: Hubert Banville <hubert.jbanville@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

from torch import nn


class SleepStagerGRU(nn.Module):
    """Sleep staging architecture from [1]_ with added GRU layer.

    This class was copied and modified from https://github.com/braindecode/braindecode/blob/master/braindecode/models/sleep_stager_chambon_2018.py v0.7.0

    Modification: adding GRU layer

    Convolutional neural network for sleep staging described in [1]_.

    Parameters
    ----------
    n_channels : int
        Number of EEG channels.
    sfreq : float
        EEG sampling frequency.
    n_conv_chs : int
        Number of convolutional channels. Set to 8 in [1]_.
    time_conv_size_s : float
        Size of filters in temporal convolution layers, in seconds. Set to 0.5
        in [1]_ (64 samples at sfreq=128).
    max_pool_size_s : float
        Max pooling size, in seconds. Set to 0.125 in [1]_ (16 samples at
        sfreq=128).
    n_classes : int
        Number of classes.
    dropout : float
        Dropout rate before the output dense layer.
    hidden_size : int
        The number of features in the hidden state h
    num_layers : int
        Number of recurrent layers. E.g.,
        setting num_layers=2 would mean stacking two GRUs together to form a stacked GRU,
        with the second GRU taking in outputs of the
        first GRU and computing the final results. Default: 1

    References
    ----------
    .. [1] Chambon, S., Galtier, M. N., Arnal, P. J., Wainrib, G., &
           Gramfort, A. (2018). A deep learning architecture for temporal sleep
           stage classification using multivariate and multimodal time series.
           IEEE Transactions on Neural Systems and Rehabilitation Engineering,
           26(4), 758-769.
    """

    def __init__(
        self,
        n_channels,
        sfreq,
        n_conv_chs=8,
        time_conv_size_s=0.5,
        max_pool_size_s=0.125,
        n_classes=5,
        dropout=0.25,
        hidden_size=64,
        num_layers=1,
    ):
        super().__init__()

        # Calculate size of convolutional filter and max pool
        time_conv_size = int(time_conv_size_s * sfreq)
        max_pool_size = int(max_pool_size_s * sfreq)

        # Calculate size of padding
        pad_size = time_conv_size // 2

        # Store number of channels
        self.n_channels = n_channels

        # If there is more than one channel, use a 2D convolutional filter
        if n_channels > 1:
            self.spatial_conv = nn.Conv2d(1, n_channels, (n_channels, 1))

        # Define the feature extractor part
        self.feature_extractor = nn.Sequential(
            nn.Conv2d(
                1, n_conv_chs, (1, time_conv_size), padding=(0, pad_size)
            ),
            nn.ReLU(),
            nn.MaxPool2d((1, max_pool_size)),
            nn.Conv2d(
                n_conv_chs,
                n_conv_chs,
                (1, time_conv_size),
                padding=(0, pad_size),
            ),
            nn.ReLU(),
            nn.MaxPool2d((1, max_pool_size)),
        )

        # Define the GRU layer
        self.gru = nn.GRU(
            input_size=n_channels * n_conv_chs,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
        )

        # Define the fully connected layer
        self.fc = nn.Sequential(
            nn.Dropout(dropout), nn.Linear(hidden_size, n_classes)
        )

    # Forward pass through the network
    def forward(self, x):
        # If input tensor is 3D, add a new dimension to represent the channel
        if x.ndim == 3:
            x = x.unsqueeze(1)

        # Pass the input through the feature extractor (size: [B,1,C,S])
        x = self.feature_extractor(x)

        # Transpose the tensor to be compatible with the GRU layer (dimension 1 is switched with 3 in the input)
        x = x.transpose(1, 3)

        # Flatten the tensor starting from dimension 2 onward (multiply n_channels with n_conv_chs)
        x = x.flatten(start_dim=2)

        # Pass the tensor through the GRU layer - x = (input_size,hidden_size,n_layers)
        x, _ = self.gru(x)

        # Get the last output of the GRU (input_size,n_layers)
        x_last = x[:, -1]

        # Pass the last output through the fully connected layer to get the prediction
        return self.fc(x_last)
