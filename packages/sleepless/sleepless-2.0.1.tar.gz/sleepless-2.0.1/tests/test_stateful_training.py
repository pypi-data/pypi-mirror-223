import torch

from torch.utils.data import DataLoader
from tqdm import tqdm

from sleepless.data.utils import ListSampleDataset


def test_stateful_training(dataset_from_json):
    normalize = True
    pick_chan = None

    for n_past_epochs in range(0, 5):
        dataset = dataset_from_json.subsets("unfiltered")
        sample = dataset["train"][0]

        sample_list = ListSampleDataset(
            sample, normalize, pick_chan, n_past_epochs
        )

        epochs = sample.data["data"]

        data = epochs.get_data(picks="eeg")

        data_tensor = torch.from_numpy(data)
        mean_data = torch.mean(data_tensor, dim=-1, keepdim=True)
        std_data = torch.std(data_tensor, dim=-1, keepdim=True)

        data_norm = torch.where(
            std_data != 0,
            (data_tensor - mean_data) / std_data,
            torch.zeros(data_tensor.shape),
        )

        data = data_norm
        assert (
            torch.sum(data == sample_list.data)
            == data.shape[0] * data.shape[1] * data.shape[2]
        )

        assert sample_list.n_past_epochs == n_past_epochs

        data_loader = DataLoader(
            dataset=sample_list,
            shuffle=True,
            batch_size=128,
            drop_last=True,
            pin_memory=torch.cuda.is_available(),
        )

        for idx, samples in enumerate(
            tqdm(data_loader, desc="train", leave=False, disable=None)
        ):
            assert samples[0][0] == sample_list.key

            assert sample_list.data.dtype == torch.float64

            win_epochs = samples[1].to(
                device="cpu",
                non_blocking=torch.cuda.is_available(),
                dtype=sample_list.data.dtype,
            )
            labels = samples[2].to(
                device="cpu",
                non_blocking=torch.cuda.is_available(),
                dtype=sample_list.data.dtype,
            )

            assert isinstance(win_epochs, torch.Tensor)
            assert isinstance(labels, torch.Tensor)
            assert win_epochs.shape[0] == 128
            assert win_epochs.shape[1] == data.shape[1]
            assert win_epochs.shape[2] == data.shape[2] + (
                n_past_epochs * data.shape[2]
            )
            assert win_epochs.shape[0] == labels.shape[0]
