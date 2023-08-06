from sleepless.models.chambon2018 import SleepStagerChambon2018
from sleepless.models.chambon_gru import SleepStagerGRU
from sleepless.models.chambon_lstm import SleepStagerChambon2018LSTM


def test_chambon_gru():
    sfreq = 100

    n_channels = 2

    model = SleepStagerGRU(n_channels=n_channels, sfreq=sfreq, n_classes=5)

    assert model.n_channels == n_channels
    if n_channels > 1:
        assert hasattr(model, "spatial_conv")

    assert hasattr(model, "feature_extractor")
    assert hasattr(model, "gru")
    assert hasattr(model, "fc")


def test_chambon():
    sfreq = 100

    n_channels = 2

    model = SleepStagerChambon2018(
        n_channels=n_channels, sfreq=sfreq, n_classes=5
    )

    assert model.n_channels == n_channels
    if n_channels > 1:
        assert hasattr(model, "spatial_conv")

    assert hasattr(model, "feature_extractor")
    assert hasattr(model, "fc")


def test_chambon_lstm():
    sfreq = 100

    n_channels = 2

    lstm_hidden_size = 32

    model = SleepStagerChambon2018LSTM(
        n_channels=n_channels, sfreq=sfreq, n_classes=5, lstm_hidden_size=32
    )

    assert model.n_channels == n_channels
    assert model.lstm_hidden_size == lstm_hidden_size

    if n_channels > 1:
        assert hasattr(model, "spatial_conv")

    assert hasattr(model, "feature_extractor")
    assert hasattr(model, "lstm")
    assert hasattr(model, "fc")
