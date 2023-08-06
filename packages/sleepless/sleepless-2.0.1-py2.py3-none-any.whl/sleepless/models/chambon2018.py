# SPDX-FileCopyrightText: Copyright (c) 2017-2020 Braindecode Developers
#
# SPDX-FileContributor: Hubert Banville <hubert.jbanville@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

from torch import nn


class SleepStagerChambon2018(nn.Module):
    """Sleep staging architecture from [Chambon-2018]_.

    This class was copied with minor modifications from https://github.com/braindecode/braindecode/blob/master/braindecode/models/sleep_stager_chambon_2018.py v0.7.0

    Modification: remove condition to return features extracted before classification,now there are always returned

    Convolutional neural network for sleep staging described in [Chambon-2018]_.

    Parameters
    ----------
    n_channels : int
        Number of EEG channels.
    sfreq : float
        EEG sampling frequency.
    n_conv_chs : int
        Number of convolutional channels. Set to 8 in [Chambon-2018]_.
    time_conv_size_s : float
        Size of filters in temporal convolution layers, in seconds. Set to 0.5
        in [Chambon-2018]_ (64 samples at sfreq=128).
    max_pool_size_s : float
        Max pooling size, in seconds. Set to 0.125 in [Chambon-2018]_ (16 samples at
        sfreq=128).
    n_classes : int
        Number of classes.
    input_size_s : float
        Size of the input, in seconds.
    dropout : float
        Dropout rate before the output dense layer.

    References
    ----------
    .. [Chambon-2018]_
    """

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
    ):
        super().__init__()

        time_conv_size = int(time_conv_size_s * sfreq)
        max_pool_size = int(max_pool_size_s * sfreq)
        input_size = int(input_size_s * sfreq)
        pad_size = time_conv_size // 2
        self.n_channels = n_channels
        len_last_layer = self._len_last_layer(
            n_channels, input_size, max_pool_size, n_conv_chs
        )

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
            nn.MaxPool2d((1, max_pool_size)),
        )
        self.fc = nn.Sequential(
            nn.Dropout(dropout), nn.Linear(len_last_layer, n_classes)
        )

    @staticmethod
    def _len_last_layer(n_channels, input_size, max_pool_size, n_conv_chs):
        return n_channels * (input_size // (max_pool_size**2)) * n_conv_chs

    def forward(self, x):
        """Forward pass.

        Parameters
        ---------
        x: torch.Tensor
            Batch of EEG windows of shape (batch_size, n_channels, n_times).
        """
        if x.ndim == 3:
            x = x.unsqueeze(1)
        if self.n_channels > 1:
            x = self.spatial_conv(x)
            x = x.transpose(1, 2)

        x = self.feature_extractor(x)
        x = x.flatten(start_dim=1)

        # we are always returning the features extracted before classification
        return self.fc(x), x
