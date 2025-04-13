import h5py
import torch
import numpy as np
from torch.utils.data import Dataset
from sklearn.preprocessing import LabelEncoder
import pandas as pd

class HDF5Dataset(Dataset):
    def __init__(self, file_path, feature_keys, target_key, transform=None):
        self.file_path = file_path
        self.feature_keys = feature_keys
        self.target_key = target_key
        self.transform = transform
        self.band_le = LabelEncoder()
        with h5py.File(self.file_path, 'r') as f:
            data_dict = {}
            self.dataset_len = len(f[self.feature_keys[0]])
            for key in self.feature_keys:
                data = f[key][()]
                if data.dtype.byteorder == '>':
                    data = data.byteswap().view(data.dtype.newbyteorder('<'))
                data_dict[key] = data
            target_data = f[self.target_key][()]
            if target_data.dtype.byteorder == '>':
                target_data = target_data.byteswap().view(target_data.dtype.newbyteorder('<'))
            data_dict[self.target_key] = target_data
            self.df = pd.DataFrame(data_dict)

            all_bands = []
            for i in range(self.dataset_len):
                for band in f['image_band'][i]:
                    all_bands.append(band.decode('utf-8'))
            self.band_le.fit(all_bands)

    def __len__(self):
        return self.dataset_len

    def _get_tensor_from_value(self, value):
        if isinstance(value, np.ndarray):
            if value.dtype.byteorder == '>':
                value = value.byteswap().view(value.dtype.newbyteorder('<'))
            return torch.from_numpy(value).float().unsqueeze(0) # 明示的に unsqueeze(0)
        elif isinstance(value, (np.float16, np.float32, np.float64)):
            if np.array(value).dtype.byteorder == '>':
                value = np.array(value).byteswap().view(np.array(value).dtype.newbyteorder('<')).item()
            return torch.tensor(value).float().unsqueeze(0) # 明示的に unsqueeze(0)
        elif isinstance(value, list):
            np_array_value = np.array(value)
            if np_array_value.dtype.byteorder == '>':
                np_array_value = np_array_value.byteswap().view(np_array_value.dtype.newbyteorder('<'))
            return torch.from_numpy(np_array_value).float().unsqueeze(0) # 明示的に unsqueeze(0)
        elif isinstance(value, (str, bytes)):
            raise TypeError(f"Unsupported type: {type(value)}")
        else:
            return torch.tensor(value).float().unsqueeze(0) # 明示的に unsqueeze(0)

    def __getitem__(self, index):
        data = {}
        features = []
        with h5py.File(self.file_path, 'r') as f: # __getitem__ 内でファイルを開く
            for key in self.feature_keys:
                value = f[key][index][()]
                if key == "image_band":
                    if value.dtype.byteorder == '>':
                        value = value.byteswap().view(value.dtype.newbyteorder('<'))
                    feature_tensor = torch.from_numpy(self.band_le.transform(value)).long().unsqueeze(0)
                    features.append(feature_tensor)
                    print(f"Feature '{key}' shape: {feature_tensor.shape}")
                else:
                    feature_tensor = self._get_tensor_from_value(value)
                    features.append(feature_tensor)
                    print(f"Feature '{key}' shape: {feature_tensor.shape}")

            target_value = f[self.target_key][index][()]
            data['target'] = self._get_tensor_from_value(target_value).unsqueeze(0)

        data['features'] = torch.cat(features, dim=1)
        return data