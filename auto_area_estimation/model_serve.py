import torch
import torch.nn as nn
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib  # モデルと一緒に scaler を保存・ロードするために使用

# デバイスの設定 (推論時は GPU が利用可能であれば利用する)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 特徴量として使用する列名 (学習時と同じである必要があります)
features = [
    'x2_image',
    'y2_image',
    'cxx_image',
    'cyy_image',
    'fluxerr_auto',
    'flux_radius',
    'area_iso',
    'xy_image',
    'npix',
    'flux_aper_1',
]


# 線形回帰モデルの定義 (学習時と同じである必要があります)
class LinearRegressionModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LinearRegressionModel, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        return self.linear(x)

# Flask アプリケーションの初期化
app = Flask(__name__)

# モデルのロード
model_path = "best_linear_regression_model.pth"
loaded_model = None
try:
    # モデルの状態辞書をロード
    state_dict = torch.load(model_path, map_location=device)

    # モデルの入力次元数を特定 (特徴量の数)
    input_dim = len(features)
    output_dim = 1
    loaded_model = LinearRegressionModel(input_dim, output_dim)
    loaded_model.load_state_dict(state_dict)
    loaded_model.eval()  # 推論モードに設定
    loaded_model.to(device)
    print(f"Model loaded successfully from {model_path}")
except FileNotFoundError:
    print(f"Error: Model file not found at {model_path}")
    loaded_model = None
except Exception as e:
    print(f"Error loading the model: {e}")
    loaded_model = None

# 標準化のためのスケーラー (学習時に使用したスケーラーを保存していればロードする)
# 今回の学習スクリプトではスケーラーを保存していないため、
# 推論リクエストごとにデータを標準化するロジックをここに記述する必要があります。
# 注意: 本番環境では、学習済みのスケーラーを保存してロードすることを強く推奨します。
# 例: joblib.load('scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    if loaded_model is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # リクエストデータが辞書のリスト形式であることを想定
        if isinstance(data, dict):
            input_df = pd.DataFrame([data])
        elif isinstance(data, list):
            input_df = pd.DataFrame(data)
        else:
            return jsonify({"error": "Invalid JSON data format. Expected a dictionary or a list of dictionaries."}), 400

        # 必要な特徴量がすべて揃っているか確認
        if not all(feature in input_df.columns for feature in features):
            missing_features = [f for f in features if f not in input_df.columns]
            return jsonify({"error": f"Missing required features: {missing_features}"}), 400

        # 特徴量の順序を学習時と同じにする
        input_data = input_df[features].values

        # 標準化 (学習時と同じように行う)
        # 注意: ここでは、学習データ全体で fit された scaler を使用する必要があります。
        #       理想的には、この scaler をファイルに保存してロードします。
        #       ここでは、推論ごとに簡易的な標準化を行う例を示します。
        scaler = StandardScaler()
        # 推論データのみで fit_transform すると、学習時とスケールが異なる可能性があります。
        # 本番環境では、学習済みの scaler をロードして transform のみを行うべきです。
        # ここでは、デモンストレーションとして、簡易的に標準化を行います。
        # 実際には、学習時に fit した scaler を保存し、ここで load して使用してください。
        # 例: loaded_scaler = joblib.load('scaler.pkl')
        #    scaled_input_data = loaded_scaler.transform(input_data)
        scaled_input_data = scaler.fit_transform(input_data) # デモ用

        # PyTorch Tensor に変換し、適切なデバイスに移動
        input_tensor = torch.tensor(scaled_input_data, dtype=torch.float32).to(device)

        # 推論の実行
        with torch.no_grad():
            predictions = loaded_model(input_tensor)

        # 結果を NumPy 配列に変換し、リスト形式にする
        predicted_areas = predictions.cpu().numpy().flatten().tolist()

        return jsonify({"predicted_area_auto": predicted_areas})

    except Exception as e:
        return jsonify({"error": f"Prediction error: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8085)