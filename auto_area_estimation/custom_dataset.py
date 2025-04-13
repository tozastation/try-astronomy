import h5py  # HDF5ファイルの読み書きを行うためのライブラリ
import torch  # PyTorchのテンソル操作などを行うためのライブラリ
import numpy as np  # 数値計算を行うためのライブラリ
from torch.utils.data import Dataset  # PyTorchのデータセットの抽象クラス
from sklearn.preprocessing import LabelEncoder  # カテゴリカルなラベルを数値に変換するためのライブラリ


class HDF5Dataset(Dataset):
    def __init__(self, file_path, keys, transform=None):
        """
        HDF5ファイルからデータを読み込むカスタムデータセットクラス。

        Args:
            file_path (str): HDF5ファイルのパス。
            keys (list): HDF5ファイルから読み込むキーのリスト。各キーはデータセット内の要素に対応する。
            transform (callable, optional): データに適用する変換関数。デフォルトはNone。
        """
        self.file_path = file_path  # HDF5ファイルのパスを保存
        self.keys = keys  # 読み込むキーのリストを保存
        self.transform = transform  # 適用する変換関数を保存
        self.band_le = LabelEncoder()  # 'image_band'の値を数値に変換するためのLabelEncoderを初期化
        self.h5_file = h5py.File(self.file_path, 'r')  # HDF5ファイルを読み取りモードで開く
        self.dataset_len = len(self.h5_file[self.keys[0]])  # データセットの長さを最初のキーのデータの長さから取得

        # 全てのキーの長さが同じであることを確認
        for key in keys:
            assert len(self.h5_file[key]) == self.dataset_len, "All keys must have the same length."

        all_bands = []
        # 全てのサンプルに含まれるバンド名（文字列）を収集
        for i in range(self.dataset_len):
            for band in self.h5_file['image_band'][i]:
                all_bands.append(band.decode('utf-8'))  # バイト文字列をUTF-8でデコードしてリストに追加
        self.band_le.fit(all_bands)  # 収集した全てのバンド名に基づいてLabelEncoderを学習

    def __len__(self):
        """
        データセットの長さを返す。

        Returns:
            int: データセットの長さ。
        """
        return self.dataset_len

    def __getitem__(self, index):
        """
        指定されたインデックスのデータを取得する。

        Args:
            index (int): 取得するデータのインデックス。

        Returns:
            dict: データの辞書。キーは初期化時に指定されたキーに対応し、値は対応するデータ。
        """
        data = {}  # データを格納する空の辞書を初期化
        for key in self.keys:
            value = self.h5_file[key][index][()]  # HDF5ファイルから指定されたキーとインデックスのデータを読み込む
            if key == "image_band":
                data[key] = torch.from_numpy(self.band_le.transform(value)).long()  # 'image_band'の場合、LabelEncoderで数値に変換し、PyTorchのLongTensorに変換
            elif isinstance(value, np.ndarray):
                data[key] = torch.from_numpy(value).float()  # NumPy配列の場合、PyTorchのFloatTensorに変換
            elif isinstance(value, (np.float16, np.float32, np.float64)):
                data[key] = torch.tensor(value).float()  # NumPyのfloat型の場合、PyTorchのFloatTensorに変換
            elif isinstance(value, list):
                data[key] = torch.from_numpy(np.array(value)).float()  # Pythonのリストの場合、NumPy配列に変換後、PyTorchのFloatTensorに変換
            elif isinstance(value, (str, bytes)):
                raise TypeError(f"Unsupported type for key {key}: {type(value)}")  # 文字列またはバイト列の場合、TypeErrorを発生させる（現状サポートしていない型）
            else:
                data[key] = torch.tensor(value)  # その他の型の場合、PyTorchのテンソルに変換
        return data  # 読み込んだデータを格納した辞書を返す

    def __del__(self):
        """
        オブジェクトが削除される際にHDF5ファイルを閉じる。
        """
        if hasattr(self, 'h5_file') and self.h5_file:
            self.h5_file.close()