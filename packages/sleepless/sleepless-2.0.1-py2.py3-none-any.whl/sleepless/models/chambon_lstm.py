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

"""Sleep staging architecture based on [1]_ with added LSTM layer.

    This class was copied and modified from https://github.com/braindecode/braindecode/blob/master/braindecode/models/sleep_stager_chambon_2018.py v0.7.0

    Modification: adding Lstm layer

    Convolutional neural network for sleep staging [1]_ with an lstm layer addition.

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
    input_size_s : float
        Size of the input, in seconds.
    dropout : float
        Dropout rate before the output dense layer.
    lstm_hidden_size : int
        Size of the lstm hidden layer, that is, the number of features in the hidden state.

    References
    ----------
    .. [1] Chambon, S., Galtier, M. N., Arnal, P. J., Wainrib, G., &
           Gramfort, A. (2018). A deep learning architecture for temporal sleep
           stage classification using multivariate and multimodal time series.
           IEEE Transactions on Neural Systems and Rehabilitation Engineering,
           26(4), 758-769.
"""


class SleepStagerChambon2018LSTM(nn.Module):
    def __init__(
        self,
        n_channels,
        sfreq,
        n_conv_chs=8,
        time_conv_size_s=0.5,
        max_pool_size_s=0.125,
        n_classes=5,
        input_size_s=30,
        dropout=0.25,
        lstm_hidden_size=32,
    ):
        super().__init__()

        time_conv_size = int(time_conv_size_s * sfreq)
        max_pool_size = int(max_pool_size_s * sfreq)
        pad_size = time_conv_size // 2
        self.n_channels = n_channels

        self.lstm_hidden_size = lstm_hidden_size

        if n_channels > 1:
            self.spatial_conv = nn.Conv2d(1, n_channels, (n_channels, 1))

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
            # global average pooling
            nn.MaxPool2d((1, max_pool_size)),
        )
        self.lstm = nn.LSTM(
            input_size=n_channels * n_conv_chs,
            hidden_size=self.lstm_hidden_size,
        )

        # Define the fully connected layer
        self.fc = nn.Sequential(
            nn.Dropout(dropout), nn.Linear(self.lstm_hidden_size, n_classes)
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

        # Pass the tensor through the LSTM layer - x = (input_size,hidden_size,n_layers)
        x, _ = self.lstm(x)

        # Get the last output of the GRU (input_size,n_layers)
        x_last = x[:, -1]

        # Pass the last output through the fully connected layer to get the prediction
        return self.fc(x_last)
