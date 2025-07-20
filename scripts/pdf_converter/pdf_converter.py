#!/usr/bin/env python3
"""
Unified PDF to PNG Converter
統合PDFからPNG変換ツール

Usage:
    python3 pdf_converter.py input.pdf
    python3 pdf_converter.py input.pdf --dpi 400
    python3 pdf_converter.py --batch /path/to/pdfs/
    python3 pdf_converter.py --section1
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from pdf2image import convert_from_path
    from PIL import Image
except ImportError as e:
    print(f"❌ 必要なライブラリがインストールされていません: {e}")
    print("以下のコマンドでインストールしてください:")
    print("./setup.sh")
    sys.exit(1)

def convert_pdf_to_png(pdf_path, output_dir=None, dpi=300):
    """PDFをPNG画像に変換"""
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")
    
    if output_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📄 変換中: {pdf_path.name}")
    print(f"📁 出力先: {output_dir}")
    print(f"🎯 解像度: {dpi} DPI")
    
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
        converted_files = []
        base_name = pdf_path.stem
        
        for i, image in enumerate(images, 1):
            if len(images) == 1:
                output_filename = f"{base_name}.png"
            else:
                output_filename = f"{base_name}_page_{i:03d}.png"
            
            output_path = output_dir / output_filename
            image.save(output_path, 'PNG')
            converted_files.append(output_path)
            print(f"✅ 保存: {output_filename}")
        
        print(f"🎉 変換完了! {len(converted_files)}個のファイルを生成")
        return converted_files
        
    except Exception as e:
        print(f"❌ 変換エラー: {e}")
        raise

def batch_convert(input_dir, output_dir=None, dpi=300):
    """ディレクトリ内の全PDFファイルを一括変換"""
    input_dir = Path(input_dir)
    pdf_files = list(input_dir.rglob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ {input_dir} にPDFファイルが見つかりません")
        return []
    
    print(f"📁 検索ディレクトリ: {input_dir}")
    print(f"📄 見つかったPDF: {len(pdf_files)}個")
    print()
    
    all_converted = []
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] {pdf_file.name}")
        try:
            converted = convert_pdf_to_png(pdf_file, output_dir, dpi)
            all_converted.extend(converted)
        except Exception as e:
            print(f"❌ エラー: {e}")
        print("-" * 40)
    
    return all_converted

def convert_section1():
    """section1.pdf専用変換"""
    script_dir = Path(__file__).parent
    pdf_path = script_dir / "../../extreme_unraveling-the-universe/chapter1/section1.pdf"
    output_dir = script_dir / "../../extreme_unraveling-the-universe/chapter1/section1_images"
    
    if not pdf_path.exists():
        print(f"❌ section1.pdfが見つかりません: {pdf_path}")
        return []
    
    print("🎯 section1.pdf専用変換")
    print("=" * 30)
    
    try:
        converted = convert_pdf_to_png(pdf_path, output_dir, dpi=400)
        print("\n📋 変換されたファイル:")
        for file_path in converted:
            print(f"  {file_path}")
        return converted
    except Exception as e:
        print(f"❌ section1.pdf変換エラー: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(
        description="PDFファイルをPNG画像に変換",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python3 pdf_converter.py input.pdf
  python3 pdf_converter.py input.pdf --dpi 400 --output-dir ./images
  python3 pdf_converter.py --batch ./pdf_directory/
  python3 pdf_converter.py --section1
        """
    )
    
    parser.add_argument("pdf_file", nargs="?", help="変換するPDFファイル")
    parser.add_argument("--batch", "-b", help="ディレクトリ内の全PDFを一括変換")
    parser.add_argument("--section1", "-s", action="store_true", help="section1.pdf専用変換")
    parser.add_argument("--output-dir", "-o", help="出力ディレクトリ")
    parser.add_argument("--dpi", "-d", type=int, default=300, help="解像度（デフォルト: 300）")
    
    args = parser.parse_args()
    
    print("🖼️  PDF to PNG Converter")
    print("=" * 40)
    
    try:
        if args.section1:
            # section1.pdf専用変換
            convert_section1()
        elif args.batch:
            # 一括変換
            batch_convert(args.batch, args.output_dir, args.dpi)
        elif args.pdf_file:
            # 単一ファイル変換
            convert_pdf_to_png(args.pdf_file, args.output_dir, args.dpi)
        else:
            print("❌ 変換するPDFファイルを指定してください")
            parser.print_help()
            return 1
        
        return 0
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())