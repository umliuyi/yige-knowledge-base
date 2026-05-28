#!/usr/bin/env python3
"""
批量图片文件处理器
扫描指定目录下的图片文件，生成包含分辨率、大小、修改时间的 CSV 报告。
"""

import os
import sys
import argparse
import csv
from pathlib import Path
from datetime import datetime

# 图片扩展名白名单
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def get_image_resolution(filepath: str) -> tuple:
    """获取图片分辨率，返回 (width, height) 或 (None, None)"""
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            return img.size  # (width, height)
    except Exception:
        return (None, None)


def format_filesize(size_bytes: int) -> str:
    """将字节数转换为可读字符串"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024 ** 2):.1f} MB"
    else:
        return f"{size_bytes / (1024 ** 3):.2f} GB"


def scan_images(directory: str) -> list:
    """递归扫描目录下所有支持的图片文件"""
    image_files = []
    directory = Path(directory)

    if not directory.exists():
        raise FileNotFoundError(f"目录不存在: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(f"路径不是目录: {directory}")

    print(f"[INFO] 开始扫描目录: {directory.resolve()}")

    # 遍历目录
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = Path(root) / filename
            if filepath.suffix.lower() in SUPPORTED_EXTENSIONS:
                image_files.append(str(filepath))

    print(f"[INFO] 共发现 {len(image_files)} 个图片文件")
    return image_files


def gather_file_info(filepath: str, index: int, total: int) -> dict:
    """收集单个文件的详细信息"""
    path = Path(filepath)

    # 文件基本信息
    stat = path.stat()
    filesize = stat.st_size
    mtime = datetime.fromtimestamp(stat.st_mtime)
    mtime_str = mtime.strftime("%Y-%m-%d %H:%M:%S")

    # 分辨率
    width, height = get_image_resolution(filepath)

    # 进度输出
    status = "OK" if width else "?"
    print(f"[{index}/{total}] {path.name} [{status}]")

    return {
        'filename': path.name,
        'filepath': str(path.resolve()),
        'width': width,
        'height': height,
        'resolution': f"{width}x{height}" if width else "未知",
        'filesize_bytes': filesize,
        'filesize_readable': format_filesize(filesize),
        'mtime': mtime_str,
    }


def write_csv(records: list, output_path: str):
    """将记录写入 CSV 文件"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ['filename', 'resolution', 'width', 'height',
                  'filesize_readable', 'filesize_bytes', 'mtime', 'filepath']

    with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"[INFO] CSV 报告已保存: {output_path.resolve()}")


def main():
    parser = argparse.ArgumentParser(
        description='批量图片文件处理器 - 扫描目录并生成图片信息 CSV 报告',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python batch_file_processor.py -i ./photos -o report.csv
  python batch_file_processor.py --input C:/images --output ./report.csv
        """
    )
    parser.add_argument('-i', '--input', required=True,
                        help='要扫描的输入目录路径')
    parser.add_argument('-o', '--output', required=True,
                        help='CSV 报告输出路径')

    args = parser.parse_args()

    try:
        print("=" * 50)
        print("批量图片文件处理器")
        print("=" * 50)

        # 扫描图片
        image_files = scan_images(args.input)

        if not image_files:
            print("[WARN] 未找到任何图片文件")
            return

        # 收集文件信息
        print(f"\n[INFO] 正在收集文件信息...")
        records = []
        for idx, filepath in enumerate(image_files, start=1):
            try:
                info = gather_file_info(filepath, idx, len(image_files))
                records.append(info)
            except Exception as e:
                print(f"[ERROR] 处理失败 {filepath}: {e}")

        # 生成 CSV
        print(f"\n[INFO] 共处理 {len(records)} 个文件")
        write_csv(records, args.output)

        print("[INFO] 处理完成!")
        print("=" * 50)

    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except NotADirectoryError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 发生未知错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()