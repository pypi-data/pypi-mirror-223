import torch

from sleepless.engine.loss_classes import (
    FocalLoss,
    KL_MSE_Loss,
    KLloss,
    MSEloss,
)


def test_FocalLoss():
    outputs = torch.Tensor(
        [
            [1.9306e-01, 9.5935e-03, -5.2158e-02, -1.5635e-01, -3.1056e-02],
            [2.1769e-01, 4.3076e-02, -3.6981e-02, -9.6315e-02, -4.4662e-02],
            [1.4245e-01, 1.0206e-02, -7.2900e-02, -1.0242e-01, -3.0809e-02],
            [1.0156e-01, -5.0833e-02, 9.6766e-03, -1.7058e-01, -4.2939e-02],
            [3.3972e-01, 9.3182e-02, -6.3031e-02, -1.1571e-01, -3.9865e-02],
        ]
    ).float()

    labels = torch.Tensor([0.0, 1.0, 2.0, 3.0, 4.0]).type(torch.int64)
    criterion = FocalLoss()
    loss = criterion(outputs, labels)
    assert outputs.shape[0] == labels.shape[0]
    assert isinstance(outputs, torch.Tensor)
    assert isinstance(labels, torch.Tensor)
    assert isinstance(loss, torch.Tensor)
    assert loss.size() == torch.Size([])


def test_MSEloss():
    outputs = torch.Tensor(
        [
            [1.9306e-01, 9.5935e-03, -5.2158e-02, -1.5635e-01, -3.1056e-02],
            [2.1769e-01, 4.3076e-02, -3.6981e-02, -9.6315e-02, -4.4662e-02],
            [1.4245e-01, 1.0206e-02, -7.2900e-02, -1.0242e-01, -3.0809e-02],
            [1.0156e-01, -5.0833e-02, 9.6766e-03, -1.7058e-01, -4.2939e-02],
            [3.3972e-01, 9.3182e-02, -6.3031e-02, -1.1571e-01, -3.9865e-02],
        ]
    ).float()

    labels = torch.Tensor([0.0, 1.0, 2.0, 3.0, 4.0]).type(torch.int64)
    criterion = MSEloss()
    loss = criterion(outputs, labels)
    assert outputs.shape[0] == labels.shape[0]
    assert isinstance(outputs, torch.Tensor)
    assert isinstance(labels, torch.Tensor)
    assert isinstance(loss, torch.Tensor)
    assert loss.size() == torch.Size([])


def test_KL_MSE_Loss():
    outputs = torch.Tensor(
        [
            [1.9306e-01, 9.5935e-03, -5.2158e-02, -1.5635e-01, -3.1056e-02],
            [2.1769e-01, 4.3076e-02, -3.6981e-02, -9.6315e-02, -4.4662e-02],
            [1.4245e-01, 1.0206e-02, -7.2900e-02, -1.0242e-01, -3.0809e-02],
            [1.0156e-01, -5.0833e-02, 9.6766e-03, -1.7058e-01, -4.2939e-02],
            [3.3972e-01, 9.3182e-02, -6.3031e-02, -1.1571e-01, -3.9865e-02],
        ]
    ).float()

    labels = torch.Tensor([0.0, 1.0, 2.0, 3.0, 4.0]).type(torch.int64)
    criterion = KL_MSE_Loss()
    loss = criterion(outputs, labels)
    assert outputs.shape[0] == labels.shape[0]
    assert isinstance(outputs, torch.Tensor)
    assert isinstance(labels, torch.Tensor)
    assert isinstance(loss, torch.Tensor)
    assert loss.size() == torch.Size([])


def test_KLloss():
    outputs = torch.Tensor(
        [
            [1.9306e-01, 9.5935e-03, -5.2158e-02, -1.5635e-01, -3.1056e-02],
            [2.1769e-01, 4.3076e-02, -3.6981e-02, -9.6315e-02, -4.4662e-02],
            [1.4245e-01, 1.0206e-02, -7.2900e-02, -1.0242e-01, -3.0809e-02],
            [1.0156e-01, -5.0833e-02, 9.6766e-03, -1.7058e-01, -4.2939e-02],
            [3.3972e-01, 9.3182e-02, -6.3031e-02, -1.1571e-01, -3.9865e-02],
        ]
    ).float()

    labels = torch.Tensor([0.0, 1.0, 2.0, 3.0, 4.0]).type(torch.int64)
    criterion = KLloss()
    loss = criterion(outputs, labels)
    assert outputs.shape[0] == labels.shape[0]
    assert isinstance(outputs, torch.Tensor)
    assert isinstance(labels, torch.Tensor)
    assert isinstance(loss, torch.Tensor)
    assert loss.size() == torch.Size([])
