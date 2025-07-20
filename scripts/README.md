# Scripts Directory
スクリプト ディレクトリ

このディレクトリには、天文学プロジェクトで使用する各種ユーティリティスクリプトが含まれています。

## 📁 ディレクトリ構成

```
scripts/
├── README.md              # このファイル
├── pdf_converter/         # PDF変換ツール
│   ├── README.md          # PDF変換ツールの詳細説明
│   ├── requirements.txt   # 必要なPythonライブラリ
│   ├── install.sh         # 自動インストールスクリプト
│   ├── pdf_to_png_converter.py    # 単一PDF変換
│   ├── batch_pdf_converter.py     # 一括PDF変換
│   └── convert_section1.sh        # section1.pdf専用変換
└── (その他のツール)        # 今後追加予定
```

## 🚀 クイックスタート

### PDF変換ツールの使用

1. **環境セットアップ**
   ```bash
   cd pdf_converter/
   ./install.sh
   ```

2. **section1.pdfの変換**
   ```bash
   cd pdf_converter/
   ./convert_section1.sh
   ```

3. **任意のPDFファイルの変換**
   ```bash
   cd pdf_converter/
   python3 pdf_to_png_converter.py /path/to/your/file.pdf
   ```

## 📋 利用可能なツール

### PDF Converter
- **目的**: PDFファイルをPNG画像に変換
- **場所**: `pdf_converter/`
- **対象**: 演習問題のPDFファイルを可視化するため

### 今後追加予定のツール
- 天文データ解析ツール
- 可視化ユーティリティ
- デプロイメントスクリプト
- テストユーティリティ

## 📚 詳細情報

各ツールの詳細な使用方法は、それぞれのディレクトリ内のREADME.mdを参照してください。

## 🔧 開発者向け情報

新しいユーティリティスクリプトを追加する場合は、以下の構造に従ってください：

```
scripts/
└── your_tool_name/
    ├── README.md          # ツールの説明
    ├── requirements.txt   # 依存関係（必要な場合）
    ├── install.sh         # セットアップスクリプト（必要な場合）
    └── main_script.py     # メインスクリプト
```

## 💡 使用例

```bash
# PDF変換環境の準備
cd scripts/pdf_converter && ./install.sh

# section1.pdfを変換
cd scripts/pdf_converter && ./convert_section1.sh

# 変換結果の確認
ls -la ../extreme_unraveling-the-universe/chapter1/section1_images/
```