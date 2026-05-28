"""
图片信息读取脚本
读取指定图片，输出分辨率、文件大小、格式信息
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("错误：需要安装 Pillow 库")
    print("请运行: pip install Pillow")
    sys.exit(1)


def get_image_info(image_path: str) -> dict:
    """读取图片信息"""
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {image_path}")

    # 获取文件大小
    file_size = path.stat().st_size

    # 读取图片信息
    with Image.open(image_path) as img:
        info = {
            "文件路径": str(path.absolute()),
            "文件名": path.name,
            "格式": img.format,
            "分辨率": f"{img.width} x {img.height}",
            "宽度": img.width,
            "高度": img.height,
            "文件大小": file_size,
            "文件大小(可读)": format_file_size(file_size),
            "颜色模式": img.mode,
        }

        # 尝试获取 DPI 信息
        if hasattr(img, 'info') and 'dpi' in img.info:
            dpi = img.info['dpi']
            if isinstance(dpi, tuple):
                info["DPI"] = f"{dpi[0]:.0f} x {dpi[1]:.0f}"
            else:
                info["DPI"] = str(dpi)

    return info


def format_file_size(size: int) -> str:
    """将字节数转换为可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def print_image_info(image_path: str):
    """打印图片信息"""
    print(f"\n{'='*50}")
    print(f"图片信息: {image_path}")
    print(f"{'='*50}")

    try:
        info = get_image_info(image_path)
        print(f"\n📁 文件名: {info['文件名']}")
        print(f"📂 格式: {info['格式']}")
        print(f"📐 分辨率: {info['分辨率']} (宽 x 高)")
        print(f"🎨 颜色模式: {info['颜色模式']}")
        print(f"📊 文件大小: {info['文件大小(可读)']} ({info['文件大小']} 字节)")

        if 'DPI' in info:
            print(f"🖨️ DPI: {info['DPI']}")

        print(f"\n完整路径: {info['文件路径']}")
        print(f"{'='*50}\n")

    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 无法读取图片: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # 测试图片路径
        test_image = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\test_image.png"

        if os.path.exists(test_image):
            print(f"未提供图片路径，使用测试图片: {test_image}")
            print_image_info(test_image)
        else:
            print("用法: python test_coding_lobster.py <图片路径>")
            print(f"\n测试: python test_coding_lobster.py {test_image}")
            print("\n请提供要读取的图片路径作为参数")
            sys.exit(1)
    else:
        image_path = sys.argv[1]
        print_image_info(image_path)