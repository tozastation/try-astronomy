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

#### 🎮 可視化プレイグラウンド

```bash
# ブラウザでインタラクティブな可視化を開く
open playground/diurnal_motion.html              # 日周運動
open playground/satellite_orbit_insertion.html   # 衛星軌道投入
open playground/satellite_orbit_gto.html         # 静止トランスファ軌道
open playground/satellite_orbit_sso.html         # 太陽同期軌道

# Pythonスクリプトの実行例
cd playground
python3 hubble_expansion_spectral_shift_demo.py  # ハッブル膨張とスペクトルシフト
python3 keplers_third_law_binary.py              # ケプラーの第3法則（連星系）
python3 schwarzschild_radius_example.py          # シュワルツシルト半径計算
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
│   ├── 🌅 diurnal_motion.html      # 日周運動可視化
│   ├── 🛰️ satellite_orbit_*.html   # 衛星軌道シミュレーション
│   ├── 🌌 hubble_expansion_spectral_shift_demo.py  # ハッブル膨張デモ
│   ├── ⭐ keplers_third_law_binary.py              # ケプラーの第3法則
│   ├── 🌟 mass_luminosity_relation.py              # 質量光度関係
│   ├── ⚫ schwarzschild_radius_example.py         # シュワルツシルト半径
│   ├── 🔭 magnitude_*.py           # 等級・光度計算
│   ├── 🚀 specific_impulse_to_velocity.py         # 比推力と速度変換
│   └── 📊 output/                   # 出力画像ディレクトリ
├── 🌌 vpython/                      # VPython可視化プロジェクト
│   └── cosmic_expansion/            # 宇宙膨張シミュレーション
│       ├── cosmic_expansion_redshift.ipynb         # 赤方偏移デモ
│       └── cosmic_expansion_redshift_fixed.ipynb   # 修正版
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

### 📊 **データサイエンス & 可視化**
- **Jupyter Notebook**: インタラクティブ開発
- **Ray Tune**: ハイパーパラメータ最適化
- **TensorBoard**: 実験記録・可視化
- **VPython**: 3D物理シミュレーション
- **Plotly**: インタラクティブグラフ

### ☸️ **インフラストラクチャ**
- **Kubernetes**: コンテナオーケストレーション
- **Helm/Helmfile**: パッケージ管理
- **JupyterHub**: マルチユーザー環境
- **Coder**: リモート開発環境

### 🏗️ **Infrastructure as Code**
- **Terraform**: インフラ管理
- **Kind**: ローカルKubernetes環境

### 🎯 **主要機能**

#### 🔬 機械学習・データ解析
- 測光赤方偏移推定モデル
- 天体領域の自動推定
- CEERS（Cosmic Evolution Early Release Science）データセット対応

#### 📐 天文計算
- ケプラーの法則計算
- 質量光度関係
- シュワルツシルト半径計算
- 等級と光度の変換
- ハッブルの法則とスペクトルシフト

#### 🛰️ 軌道力学シミュレーション
- 衛星軌道投入（LEO → GTO → GEO）
- 静止トランスファ軌道（GTO）
- 太陽同期軌道（SSO）
- 比推力と速度変換

#### 🌌 可視化
- インタラクティブHTML/JavaScript可視化
- VPythonによる3D宇宙膨張シミュレーション
- 赤方偏移の視覚的デモンストレーション
- 日周運動の可視化

## 📚 引用・参考文献

### extreme_unraveling-the-universe 教育教材

**主要参考書**
- **『極・宇宙を解く』** (恒星社厚生閣, 2020年)
- 編者：福江 純、沢 武文、高橋 真聡
- ISBN: 9784769916437
- URL: https://www.kouseisha.com/book/b492698.html

**詳解版**
- **『極・宇宙を解く 詳解』** (恒星社厚生閣)
- 編者：福江 純、沢 武文、高橋 真聡
- URL: https://www.kouseisha.com/news/n32789.html

## 🎓 学習リソース

### 📚 教育教材
- **Chapter 1**: 宇宙のスケールと基本概念
  - フラーレン構造の理解
  - 原子構造と星間物質
  - 時間・距離スケールの把握
  - プランク角単位系

### 🧪 実践プロジェクト
- **Playground**: 20以上の天文計算・シミュレーションスクリプト
- **VPython**: 宇宙膨張の3D可視化
- **機械学習**: 実際の天文データを用いたモデル訓練

