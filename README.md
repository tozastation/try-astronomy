# 🌌 Try Astronomy - 天文学とテクノロジーの探求

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.6.0+-red.svg)](https://pytorch.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

**ITエンジニアが天文学を学ぶための個人的な学習リポジトリです。**

## 👋 このリポジトリについて

このリポジトリは、ITエンジニアである私が天文学の初学者として、機械学習、データ解析、可視化などの技術を活用しながら宇宙について学ぶための場所です。

- 🎯 **対象**: 自分自身（ITエンジニア、天文学初学者）
- 📖 **目的**: 教科書の演習問題を解き、実際にコードを書いて理解を深める
- 🛠️ **アプローチ**: とっかかりやすい領域（Python、機械学習、インフラ）から実践的に学習

機械学習による天体データ解析、インタラクティブな教育コンテンツ、そして再現性の高い開発環境を組み合わせることで、複雑な宇宙の謎を探求しています。

## ✨ 特徴と技術

本プロジェクトは、以下の主要な機能領域から構成されています。

### 🔬 **機械学習による天体解析 (PyTorch, scikit-learn, Ray)**
-   **測光赤方偏移推定**: CEERSデータセットを用いた深層学習モデルの学習。
-   **天体領域の自動推定**: 天体画像から関心領域を特定する手法の実装。
-   **ハイパーパラメータ最適化**: Ray Tuneによる効率的なモデル探索の実践。

### 🎓 **インタラクティブな教育コンテンツ (Jupyter, VPython)**
-   **教科書連動**: 『極・宇宙を解く』の演習問題をJupyterで解きながら学習。
-   **3Dシミュレーション**: VPythonで宇宙膨張や物理法則を視覚的に理解。
-   **段階的学習**: 宇宙のスケールから始まり、徐々に専門的なトピックへ進行。

### 🛰️ **天文計算と軌道力学シミュレーション (NumPy, Astropy, Plotly)**
-   **物理法則の実装**: ケプラーの法則、質量光度関係、シュワルツシルト半径などを実装。
-   **軌道設計**: 衛星軌道投入（LEO→GTO→GEO）や太陽同期軌道（SSO）の計算を実践。
-   **データ可視化**: MatplotlibやPlotlyを用いたインタラクティブなグラフ描画の学習。

### ☸️ **再現性の高い開発・研究環境 (Kubernetes, Terraform, Coder)**
-   **Infrastructure as Code**: Terraformでインフラをコード管理する実践。
-   **ローカルKubernetes**: Kindで手軽にローカル環境を構築。
-   **リモート開発環境**: CoderとJupyterHubによる開発環境の構築と活用。

## 📊 使用データセット

機械学習プロジェクトでは、以下の天文データセットを使用しています。

### CEERS (Cosmic Evolution Early Release Science)
-   **用途**: 測光赤方偏移推定モデルの学習
-   **特徴**: JWST（ジェームズ・ウェッブ宇宙望遠鏡）による多波長観測データ
-   **内容**: 複数のフィルター（F070W, F090W, F115W, F150W, F200W, F277W, F356W, F444Wなど）の測光データ

### Multimodal Universe
HuggingFace上で公開されている天文データセットコレクション：

-   **Legacy Survey**: 銀河の多波長画像データ
-   **SDSS (Sloan Digital Sky Survey)**: スペクトルデータ
-   **PLAsTiCC (Photometric LSST Astronomical Time-Series Classification Challenge)**: 時系列光度曲線データ

詳細は[Multimodal Universe](https://huggingface.co/MultimodalUniverse)を参照。

## 📁 プロジェクト構造

```
try-astronomy/
├── README.md
├── auto_area_estimation/   # 機械学習（測光赤方偏移推定）
├── extreme_unraveling-the-universe/ # 教育コンテンツ（『極・宇宙を解く』）
├── kubernetes/             # Kubernetesマニフェスト (Helmfile)
├── playground/             # 天文計算・可視化スクリプトの実験場
├── scripts/                # ユーティリティスクリプト（PDF変換など）
└── terraform/              # インフラ定義 (Terraform)
```

## 📚 参考資料

本プロジェクトの教育コンテンツ `extreme_unraveling-the-universe` は、以下の書籍を参考に作成されています。

-   **『極・宇宙を解く』** (恒星社厚生閣, 2020年)
    -   編者：福江 純、沢 武文、高橋 真聡
    -   ISBN: 9784769916437
-   **『極・宇宙を解く 詳解』** (恒星社厚生閣)
    -   [公式情報](https://www.kouseisha.com/news/n32789.html)


