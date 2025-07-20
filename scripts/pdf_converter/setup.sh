#!/bin/bash
# PDF to PNG Converter Installation Script (Fixed Version)
# バージョン互換性問題を修正したインストールスクリプト

set -e  # エラー時に停止

echo "🔧 PDF to PNG Converter セットアップ (修正版)"
echo "=============================================="

# 現在のディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Python環境の確認
echo "📋 Python環境の確認..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3がインストールされていません"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python ${PYTHON_VERSION} を検出"

# pip の確認とアップグレード
echo ""
echo "📦 pip の確認とアップグレード..."
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pipがインストールされていません"
    echo "pipをインストールしてください: sudo apt-get install python3-pip"
    exit 1
fi

# pipをアップグレード
pip3 install --upgrade pip

# システムパッケージのインストール
echo ""
echo "📦 システムパッケージのインストール..."
if command -v apt-get &> /dev/null; then
    echo "Ubuntu/Debian系のシステムを検出"
    echo "poppler-utilsをインストール中..."
    sudo apt-get update -qq
    sudo apt-get install -y poppler-utils
    echo "✅ poppler-utils インストール完了"
elif command -v yum &> /dev/null; then
    echo "RedHat/CentOS系のシステムを検出"
    sudo yum install -y poppler-utils
    echo "✅ poppler-utils インストール完了"
elif command -v dnf &> /dev/null; then
    echo "Fedora系のシステムを検出"
    sudo dnf install -y poppler-utils
    echo "✅ poppler-utils インストール完了"
elif command -v brew &> /dev/null; then
    echo "macOSを検出"
    brew install poppler
    echo "✅ poppler インストール完了"
else
    echo "⚠️  パッケージマネージャーを検出できませんでした"
    echo "手動でpoppler-utilsをインストールしてください:"
    echo "  Ubuntu/Debian: sudo apt-get install poppler-utils"
    echo "  macOS: brew install poppler"
fi

# Pythonライブラリのインストール（バージョン指定で個別インストール）
echo ""
echo "🐍 Pythonライブラリのインストール..."
cd "${SCRIPT_DIR}"

echo "利用可能なpdf2imageバージョンを確認中..."
# 利用可能な最新バージョンを使用
echo "pdf2imageをインストール中..."
pip3 install "pdf2image>=1.16.0,<2.0.0"

echo "Pillowをインストール中..."
pip3 install "Pillow>=8.0.0"

echo "tqdmをインストール中..."
pip3 install "tqdm>=4.0.0"

# インストール確認
echo ""
echo "✅ インストール確認..."
python3 -c "
import sys
try:
    import pdf2image
    print(f'✅ pdf2image: OK (version: {pdf2image.__version__})')
except ImportError as e:
    print(f'❌ pdf2image: エラー - {e}')
    sys.exit(1)

try:
    from PIL import Image
    import PIL
    print(f'✅ Pillow: OK (version: {PIL.__version__})')
except ImportError as e:
    print(f'❌ Pillow: エラー - {e}')
    sys.exit(1)

try:
    import tqdm
    print(f'✅ tqdm: OK (version: {tqdm.__version__})')
except ImportError as e:
    print(f'⚠️ tqdm: エラー - {e} (オプションなので続行)')
"

# 実行権限の設定
echo ""
echo "🔑 実行権限の設定..."
chmod +x pdf_to_png_converter.py
chmod +x batch_pdf_converter.py
chmod +x convert_section1.sh

# 簡単な機能テスト
echo ""
echo "🧪 機能テスト..."
python3 -c "
try:
    from pdf2image import convert_from_path
    print('✅ pdf2image import: OK')
except ImportError as e:
    print(f'❌ pdf2image import: エラー - {e}')
    exit(1)

try:
    from PIL import Image
    print('✅ PIL import: OK')
except ImportError as e:
    print(f'❌ PIL import: エラー - {e}')
    exit(1)
"

# ヘルプテスト
if python3 pdf_to_png_converter.py --help > /dev/null 2>&1; then
    echo "✅ pdf_to_png_converter.py: OK"
else
    echo "❌ pdf_to_png_converter.py: エラー"
fi

echo ""
echo "🎉 セットアップ完了!"
echo ""
echo "インストールされたバージョン:"
python3 -c "
import pdf2image, PIL
print(f'  pdf2image: {pdf2image.__version__}')
print(f'  Pillow: {PIL.__version__}')
"

echo ""
echo "使用方法:"
echo "  section1.pdf変換:"
echo "    ./convert_section1.sh"
echo ""
echo "  その他のPDF変換:"
echo "    python3 pdf_to_png_converter.py your_file.pdf"
echo ""
echo "  ヘルプ:"
echo "    python3 pdf_to_png_converter.py --help"
echo ""