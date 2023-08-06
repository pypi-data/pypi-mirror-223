# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# For Class FocalLoss :
# SPDX-FileCopyrightText: Copyright (c) 2017 carwin
#
# SPDX-License-Identifier: MIT
"""Setup functions for engine."""

import logging

logger = logging.getLogger(__name__)


import torch
import torch.nn as nn
import torch.nn.functional as F


class FocalLoss(nn.Module):
    """This class was copied and mofified from
    https://github.com/clcarwin/focal_loss_pytorch/blob/master/focalloss.py
    v(13 May 2023)"""

    def __init__(self, gamma=0, size_average=True):
        super().__init__()
        self.gamma = gamma
        self.size_average = size_average

    def forward(self, input, target):
        target = target.view(-1, 1)

        logpt = F.log_softmax(input)
        logpt = logpt.gather(1, target)
        logpt = logpt.view(-1)
        # Variable() function deprecated. Variable(tensor) and Variable(tensor, requires_grad)
        # still work as expected, but they return Tensors instead of Variables.
        pt = logpt.data.exp()

        loss = -1 * (1 - pt) ** self.gamma * logpt
        return loss.sum()


class MSEloss(nn.Module):
    def __init__(self, num_classes=5):
        super().__init__()

        self.num_classes = num_classes
        self.targets_one_hot = torch.eye(self.num_classes)

    def forward(self, predictions, targets):
        g = torch.nn.functional.softmax(predictions, dim=1)

        device = predictions.device
        self.targets_one_hot = self.targets_one_hot.to(device)

        targets_one_hot = self.targets_one_hot[targets]

        mse_loss = torch.mean((g - targets_one_hot) ** 2)

        return mse_loss


class KL_MSE_Loss(nn.Module):
    def __init__(self):
        super().__init__()
        self.mse_loss = MSEloss()
        self.kl_loss = KLloss()

    def forward(self, predictions, targets):
        mse_loss = self.mse_loss(predictions, targets)
        kl_loss = self.kl_loss(predictions, targets)
        combined_loss = mse_loss + kl_loss
        return combined_loss


class KLloss(nn.Module):
    def __init__(self, num_classes=5):
        super().__init__()

        self.num_classes = num_classes
        self.targets_one_hot = torch.eye(self.num_classes)

    def forward(self, predictions, targets):
        # Compute the KL divergence loss
        device = predictions.device
        self.targets_one_hot = self.targets_one_hot.to(device)

        targets_one_hot = self.targets_one_hot[targets]
        pred_dist = F.log_softmax(predictions, dim=1)
        kl_loss = F.kl_div(
            pred_dist, targets_one_hot.float(), reduction="batchmean"
        )
        return kl_loss
