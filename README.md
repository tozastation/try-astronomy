# 🌌 Try Astronomy - 天文学プロジェクト

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.6.0+-red.svg)](https://pytorch.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

天文学と機械学習の融合プロジェクト。自動領域推定モデル、極限宇宙の解明教育教材、インフラストラクチャ設定を統合した包括的な学習・研究環境です。

## 📚 プロジェクト概要

このリポジトリは、以下の主要コンポーネントから構成されています：

### 🔬 **自動領域推定 (Auto Area Estimation)**
- PyTorchベースの機械学習モデル
- 測光赤方偏移推定
- 天体データの自動解析

### 🎓 **極限宇宙の解明 (Extreme Unraveling the Universe)**
- 天文学教育教材とJupyterノートブック
- 段階的学習プログラム
- 理論・計算・可視化の統合アプローチ

### ☸️ **インフラストラクチャ**
- Kubernetes環境（JupyterHub + Coder）
- Terraformによるインフラコード
- Helmチャートによるデプロイメント

### 🛠️ **ユーティリティツール**
- PDF変換ツール
- 天文データ処理スクリプト
- 可視化プレイグラウンド

## 🚀 クイックスタート

### 1. 環境セットアップ

```bash
# リポジトリのクローン
git clone https://github.com/tozastation/try-astronomy.git
cd try-astronomy

# 機械学習環境のセットアップ (uv使用)
cd auto_area_estimation
uv sync
```

### 2. 基本的な使用方法

#### 🔬 機械学習モデルの実行

```bash
cd auto_area_estimation
uv run jupyter notebook main.ipynb
```

#### 🎓 教育教材の学習

```bash
cd extreme_unraveling-the-universe/chapter1
jupyter notebook section1_detailed_solutions.ipynb
```

#### 🛠️ PDFツールの使用

```bash
cd scripts/pdf_converter
./setup.sh
python3 pdf_converter.py --section1
```

### 3. 開発環境の起動

#### Kubernetes環境 (Local)

```bash
# KindクラスターでのKubernetes環境
kind create cluster --config kind.yaml

# Helmfileでサービスをデプロイ
cd kubernetes
helmfile sync
```

#### 可視化プレイグラウンド

```bash
# ブラウザで以下を開く
open playground/diurnal_motion.html
```

## 📁 プロジェクト構造

```
try-astronomy/
├── 📋 README.md                    # このファイル
├── ⚙️ CLAUDE.md                    # Claude設定・開発ガイドライン
├── 🤖 auto_area_estimation/        # 機械学習プロジェクト
│   ├── 📊 ceers_training.ipynb     # データ訓練ノートブック
│   ├── 📈 ceers_visualize.ipynb    # 可視化ノートブック
│   ├── 🎯 main.ipynb               # メインノートブック
│   ├── 🧮 model_serve.py           # モデルサービング
│   ├── 📦 pyproject.toml           # Python依存関係管理
│   └── 🔄 uv.lock                  # 依存関係ロック
├── 🎓 extreme_unraveling-the-universe/  # 教育教材
│   └── chapter1/                   # 第1章：宇宙のスケール
│       ├── section1/               # セクション1
│       │   ├── 📄 section1.pdf    # 問題PDF
│       │   └── 🖼️ *.png            # 変換済み画像
│       └── 📖 section1_detailed_solutions.ipynb  # 詳細解答
├── ☸️ kubernetes/                   # Kubernetes設定
│   ├── 📋 helmfile.yaml            # Helmfile設定
│   └── values/                     # Helm Values
│       ├── 🪐 jupyterhub.yaml      # JupyterHub設定
│       ├── 💻 coder.yaml           # Coder設定
│       └── 🌐 ingress-nginx.yaml   # Ingress設定
├── 🎮 playground/                   # 可視化プレイグラウンド
│   └── 🌅 diurnal_motion.html      # 日周運動可視化
├── 🛠️ scripts/                     # ユーティリティスクリプト
│   ├── 📄 pdf_converter/           # PDF変換ツール
│   │   ├── 🔧 pdf_converter.py     # 統合変換スクリプト
│   │   ├── 📦 requirements.txt     # Python依存関係
│   │   └── ⚙️ setup.sh             # セットアップスクリプト
│   └── 🖥️ cat-hosts-on-windows.sh  # Windows用ユーティリティ
└── 🏗️ terraform/                   # Infrastructure as Code
    └── coder/                      # Coder用Terraform設定
        └── analyze/                # インフラ分析設定
```

## 🔧 技術スタック

### 🐍 **Python & 機械学習**
- **Python**: 3.10+
- **PyTorch**: 2.6.0+ (深層学習)
- **scikit-learn**: 1.6.1+ (機械学習)
- **NumPy/Pandas**: 数値計算・データ処理
- **Matplotlib/Seaborn**: データ可視化
- **Astropy**: 天文データ処理

### 📊 **データサイエンス**
- **Jupyter Notebook**: インタラクティブ開発
- **Ray Tune**: ハイパーパラメータ最適化
- **TensorBoard**: 実験記録・可視化

### ☸️ **インフラストラクチャ**
- **Kubernetes**: コンテナオーケストレーション
- **Helm/Helmfile**: パッケージ管理
- **JupyterHub**: マルチユーザー環境
- **Coder**: リモート開発環境

### 🏗️ **Infrastructure as Code**
- **Terraform**: インフラ管理
- **Kind**: ローカルKubernetes環境

## 📖 学習パス

### 👶 **初級者向け**
1. **Chapter 1 - 宇宙のスケール**
   - `extreme_unraveling-the-universe/chapter1/section1_detailed_solutions.ipynb`
   - 基本的な天文学概念の理解

### 🎯 **中級者向け**
2. **機械学習モデルの理解**
   - `auto_area_estimation/main.ipynb`
   - 測光赤方偏移推定の実装

### 🚀 **上級者向け**
3. **インフラストラクチャ構築**
   - `kubernetes/` でのKubernetes環境構築
   - `terraform/` でのインフラコード管理

## 🎯 主要機能

### 🔬 **自動領域推定**
- **測光赤方偏移推定**: CEERS データセットを使用
- **機械学習パイプライン**: データ前処理から学習まで自動化
- **モデルサービング**: Flask APIでの推論サービス
- **実験管理**: TensorBoardによる学習過程の可視化

### 🎓 **教育教材**
- **段階的学習**: 理論→計算→可視化の3段階アプローチ
- **詳細解説**: 各問題の背景理論と物理的意味
- **インタラクティブ可視化**: matplotlib/seabornによるグラフ作成
- **日本語対応**: 完全日本語での学習支援

### ☸️ **開発環境**
- **マルチユーザー対応**: JupyterHubによる複数ユーザー同時利用
- **リモート開発**: Coderによるクラウド開発環境
- **自動デプロイ**: Helmfileによる一括環境構築

## 🛠️ 開発者ガイド

### 📋 **コントリビュート方法**

1. **Issue作成**: バグ報告や機能要求
2. **フォーク**: リポジトリをフォーク
3. **ブランチ作成**: `feature/新機能名` or `fix/バグ修正名`
4. **開発**: CLAUDE.mdのガイドラインに従って開発
5. **プルリクエスト**: 詳細な説明とともに提出

### 🔍 **コード品質**

```bash
# リンタとフォーマッタの実行
cd auto_area_estimation
uv run ruff check .
uv run black .

# テストの実行
uv run pytest tests/
```

### 📚 **ドキュメント**
- **CLAUDE.md**: 開発ガイドライン・プロジェクト指針
- **各README.md**: ディレクトリ固有の詳細情報
- **Jupyter Notebook**: 実行可能なドキュメント

## 🌟 使用例

### 🔬 **研究利用**
```python
# 測光赤方偏移推定
from model_serve import PhotometricRedshiftEstimator

estimator = PhotometricRedshiftEstimator()
redshift = estimator.predict(photometric_data)
```

### 🎓 **教育利用**
```python
# 宇宙スケールの学習
import section1_solutions as sol

# C60フラーレンの構造解析
sol.analyze_fullerene_structure()

# 星間空間密度の計算
sol.calculate_interstellar_density()
```

### 🛠️ **ツール利用**
```bash
# PDF変換
python3 scripts/pdf_converter/pdf_converter.py input.pdf

# Kubernetes環境起動
cd kubernetes && helmfile sync
```

## 🤝 コミュニティ

### 💬 **サポート**
- **GitHub Issues**: バグ報告・機能要求
- **Discussions**: 質問・議論
- **Wiki**: 詳細なドキュメント

### 🎯 **ロードマップ**
- [ ] Chapter 2: 重力と重力エネルギー
- [ ] 分光データ解析機能
- [ ] リアルタイム観測データ対応
- [ ] Web UIの開発
- [ ] Docker対応強化

## 📄 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

## 🙏 謝辞

- **CEERS**: James Webb Space Telescope のデータ提供
- **Astropy**: 天文学Pythonライブラリ
- **PyTorch**: 深層学習フレームワーク
- **Jupyter**: インタラクティブ開発環境
- **Kubernetes**: コンテナオーケストレーション

## 📞 連絡先

- **GitHub**: [@tozastation](https://github.com/tozastation)
- **Issues**: [プロジェクトIssues](https://github.com/tozastation/try-astronomy/issues)

---

**⭐ このプロジェクトが役に立ったら、ぜひスターをお願いします！**