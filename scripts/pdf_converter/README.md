# PDF to PNG Converter

PDFファイルをPNG画像に変換するためのシンプルなツールです。

## 📁 ファイル構成

```
pdf_converter/
├── README.md           # このファイル
├── requirements.txt    # 必要なPythonライブラリ
├── setup.sh           # 環境セットアップスクリプト
└── pdf_converter.py   # 統合変換スクリプト
```

## 🚀 クイックスタート

### 1. 環境セットアップ
```bash
./setup.sh
```

### 2. section1.pdfの変換
```bash
python3 pdf_converter.py --section1
```

### 3. 任意のPDFファイルの変換
```bash
python3 pdf_converter.py your_file.pdf
```

## 📦 手動インストール

requirements.txtを使用する場合：
```bash
pip3 install -r requirements.txt
```

個別にインストールする場合：
```bash
pip3 install pdf2image Pillow
```

**重要**: システムパッケージも必要です：
- Ubuntu/Debian: `sudo apt-get install poppler-utils`
- macOS: `brew install poppler`

## 💡 使用例

### section1.pdf専用変換
```bash
python3 pdf_converter.py --section1
```

### 基本的な変換
```bash
python3 pdf_converter.py input.pdf
```

### 高解像度で変換（400 DPI）
```bash
python3 pdf_converter.py input.pdf --dpi 400
```

### 出力ディレクトリを指定
```bash
python3 pdf_converter.py input.pdf --output-dir ./images
```

### ディレクトリ内の全PDFを一括変換
```bash
python3 pdf_converter.py --batch ./pdf_directory/
```

## 🔧 オプション

- `--section1, -s`: section1.pdf専用変換
- `--batch, -b`: ディレクトリ内の全PDFを一括変換
- `--output-dir, -o`: 出力ディレクトリ
- `--dpi, -d`: 解像度（デフォルト: 300）

## 📋 出力ファイル命名規則

### 単一ページPDF
```
input.pdf → input.png
```

### 複数ページPDF
```
input.pdf → input_page_001.png
          → input_page_002.png
          → input_page_003.png
```

## ⚠️ トラブルシューティング

### エラー: "pdf2image not found"
```bash
pip3 install pdf2image
```

### エラー: "Unable to get page count"
poppler-utilsがインストールされていません：
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

### 権限エラー
スクリプトに実行権限を付与：
```bash
chmod +x pdf_to_png_converter.py
chmod +x batch_pdf_converter.py
```

## 📊 対応形式

### 入力
- PDF (Portable Document Format)

### 出力
- PNG (推奨、デフォルト)
- JPEG
- TIFF

## 🔍 動作確認

インストール後の動作確認：
```bash
python3 pdf_to_png_converter.py --help
python3 batch_pdf_converter.py --help
```

## 📈 パフォーマンス

- **解像度**: 300 DPI（デフォルト）- 印刷品質
- **メモリ使用量**: PDFサイズと解像度に依存
- **処理速度**: 1ページあたり数秒（300 DPI時）

解像度の目安：
- 150 DPI: 画面表示用
- 300 DPI: 印刷品質（推奨）
- 600 DPI: 高精細印刷

## 🎯 section1.pdf変換の例

```bash
# section1.pdfを300 DPIで変換
python3 pdf_to_png_converter.py ../extreme_unraveling-the-universe/chapter1/section1.pdf

# 高解像度で変換してimagesフォルダに保存
python3 pdf_to_png_converter.py ../extreme_unraveling-the-universe/chapter1/section1.pdf --dpi 400 --output-dir ./images

# chapter1フォルダの全PDFを一括変換
python3 batch_pdf_converter.py ../extreme_unraveling-the-universe/chapter1/ --output-dir ./converted_pdfs
```