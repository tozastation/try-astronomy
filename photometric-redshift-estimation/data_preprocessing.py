import h5py
import numpy as np
import pandas as pd


def load_ceers_data(filepath, filters, redshift_col):
    """
    hdf5ファイルからCEERSデータを読み込み、Pandas DataFrameに変換する関数。

    Args:
        filepath (str): hdf5ファイルのパス。
        filters (list): 使用するフィルター名のリスト。
        redshift_col (str): 赤方偏移の列名。
    Returns:
        pandas.DataFrame: 必要なデータを含むDataFrame。
    """

    with h5py.File(filepath, 'r') as f:
        # データセットの構造に合わせて、適切なグループ/データセットを指定
        # 例:  f['some_group']['some_dataset']
        data = f['your_group']['your_dataset'][:]

    df = pd.DataFrame(data)
    # 必要なカラムを選択
    selected_cols = filters + [redshift_col]
    df = df[selected_cols]

    # fluxが0以下の場合の処理 (必要に応じて適宜修正)
    for filter_name in filters:
        df.loc[df[filter_name] <= 0, filter_name] = np.nan  # 0以下のfluxをNaNで置き換え

    # magnitudeへの変換 (zeropointの値を適切に設定)
    zeropoint = 25.0 # 適切なzeropointを設定
    for filter_name in filters:
        df[filter_name] = -2.5 * np.log10(df[filter_name]) + zeropoint
    # 欠損値処理 (必要に応じて適宜修正)
    df.dropna(inplace=True)
    return df


# 使用例:
filepath = 'your_hdf5_file.h5'  # hdf5ファイルのパスを指定
# 使用するフィルター名
filters = ['f115w', 'f150w', 'f200w', 'f277w', 'f356w', 'f410m', 'f444w']
# 赤方偏移のカラム名
redshift_col = 'redshift' 
df = load_ceers_data(filepath, filters, redshift_col)
