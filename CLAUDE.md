# Claude アシスタント設定

このファイルには、このプロジェクトでClaudeがより良く支援するための指示とコンテキストが含まれています。

## プロジェクト概要
天文学プロジェクトで、以下を含みます：
- 自動領域推定機械学習モデル
- 極限宇宙の解明教育教材
- Kubernetesデプロイメント設定
- Terraformインフラストラクチャコード
- 天文学可視化プレイグラウンド

## 開発コマンド
- Python環境: 依存関係管理に`uv`を使用（pyproject.tomlを参照）
- データ分析と可視化にJupyterノートブック
- モデル訓練とサービング機能

## プロジェクト構造
- `auto_area_estimation/` - PyTorchを使った領域推定MLモデル
- `extreme_unraveling-the-universe/` - 天文学教育コンテンツと演習
- `kubernetes/` - Helmチャートとデプロイメント設定
- `terraform/` - Infrastructure as Code
- `playground/` - HTMLビジュアライゼーション（日周運動）
- `scripts/` - 開発用ユーティリティスクリプト

## 重要な指示
**Claudeは必ず日本語で応答してください。すべての出力、説明、コメントは日本語で行ってください。**

## 注意事項
- 機械学習モデルにPyTorchを使用
- インタラクティブ開発にJupyterノートブック
- JupyterHubとCoderを使ったKubernetes設定
- 天文学の概念とデータ分析に教育的焦点