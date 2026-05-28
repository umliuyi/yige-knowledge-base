#!/usr/bin/env python3
"""
视频片段合并器 - Video Segment Merger
按文件名排序读取文件夹内所有 .mp4 文件，合并为单一视频。
支持自动统一分辨率为 1920x1080，输出 H.264 + AAC (MP4)。
"""

import os
import sys
import subprocess
import tempfile
import re
from pathlib import Path
from typing import List, Optional

# ------------------------------------------------------------
# FFmpeg 路径配置
# ------------------------------------------------------------
FFMPEG_BUNDLED = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"


def find_ffmpeg() -> str:
    """查找可用的 FFmpeg 可执行文件路径。"""
    # 1. 优先使用打包的 FFmpeg
    if os.path.isfile(FFMPEG_BUNDLED):
        return FFMPEG_BUNDLED

    # 2. 尝试系统 PATH
    for name in ("ffmpeg", "ffmpeg.exe"):
        try:
            result = subprocess.run(
                [name, "-version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                return name
        except Exception:
            pass

    raise FileNotFoundError(
        "未找到 FFmpeg，请确保已安装 FFmpeg 并将其加入 PATH，"
        "或确认打包路径存在。"
    )


def get_video_info(path: str, ffmpeg: str) -> dict:
    """使用 ffprobe 读取视频基本信息（时长、分辨率）。"""
    cmd = [
        ffmpeg.replace("ffmpeg", "ffprobe"),
        "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        "-show_format",
        path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {}
        import json
        data = json.loads(result.stdout)
        info = {"width": 0, "height": 0, "duration": 0.0}
        for s in data.get("streams", []):
            if s.get("codec_type") == "video":
                info["width"] = int(s.get("width", 0) or 0)
                info["height"] = int(s.get("height", 0) or 0)
                break
        fmt = data.get("format", {})
        info["duration"] = float(fmt.get("duration", 0) or 0)
        return info
    except Exception:
        return {}


def collect_mp4(folder: str) -> List[str]:
    """收集文件夹内所有 .mp4 文件，按文件名排序。"""
    folder_path = Path(folder)
    if not folder_path.is_dir():
        raise ValueError(f"文件夹不存在或不是目录: {folder}")
    mp4_files = sorted(
        [str(p) for p in folder_path.glob("*.mp4")],
        key=lambda x: os.path.basename(x),
    )
    if not mp4_files:
        raise ValueError(f"文件夹内没有找到 .mp4 文件: {folder}")
    return mp4_files


def build_concat_list(files: List[str], tmp_dir: str) -> str:
    """生成 FFmpeg concat 所需的文件列表（分离版）。"""
    lines = []
    for f in files:
        safe = f.replace("\\", "\\\\").replace(":", "\\:")  # 转义路径特殊字符
        lines.append(f"file '{safe}'")
    list_path = os.path.join(tmp_dir, "concat_list.txt")
    with open(list_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return list_path


def merge_videos(
    input_folder: str,
    output_path: str,
    target_width: int = 1920,
    target_height: int = 1080,
    crf: int = 23,
    preset: str = "medium",
) -> None:
    """
    核心合并函数。

    参数:
        input_folder: 包含 .mp4 文件的文件夹路径
        output_path: 输出文件路径
        target_width / target_height: 目标分辨率（默认 1920x1080）
        crf: H.264 质量参数（0-51，越小质量越高，默认 23）
        preset: H.264 编码速度（默认 medium）
    """
    ffmpeg = find_ffmpeg()
    print(f"[FFmpeg] 使用: {ffmpeg}")

    # 1. 收集文件
    files = collect_mp4(input_folder)
    total = len(files)
    print(f"[输入] 共找到 {total} 个 .mp4 文件：")
    for i, f in enumerate(files, 1):
        print(f"  [{i}/{total}] {os.path.basename(f)}")

    # 2. 探测总时长（用于进度提示）
    total_duration = 0.0
    print("\n[探测] 正在分析各片段信息...")
    for i, f in enumerate(files, 1):
        info = get_video_info(f, ffmpeg)
        dur = info.get("duration", 0)
        w = info.get("width", 0)
        h = info.get("height", 0)
        total_duration += dur
        status = "OK"
        if w == 0 or h == 0:
            status = "⚠ 分辨率未知"
        elif w != target_width or h != target_height:
            status = f"→ 将缩放至 {target_width}x{target_height}"
        print(f"  [{i}/{total}] {os.path.basename(f)} | {w}x{h} | {dur:.1f}s | {status}")
    print(f"[探测] 总时长约 {total_duration:.1f}s ({total_duration/60:.1f}min)\n")

    # 3. 创建 concat 文件列表
    with tempfile.TemporaryDirectory(prefix="merge_videos_") as tmp_dir:
        list_path = build_concat_list(files, tmp_dir)

        # 4. 构建 FFmpeg 命令
        # -vf scale: 统一分辨率
        # -c:v libx264: H.264 视频编码
        # -c:a aac: AAC 音频编码
        # -crf: 质量
        # -preset: 编码速度
        # -movflags +faststart: 支持网络播放
        cmd = [
            ffmpeg,
            "-y",                     # 覆盖输出文件
            "-f", "concat",
            "-safe", "0",
            "-i", list_path,
            "-vf", (
                f"scale={target_width}:{target_height}"
                f":force_original_aspect_ratio=decrease"
                f",pad={target_width}:{target_height}"
                f":(ow-iw)/2:(oh-ih)/2"
                f",setsar=1"
            ),
            "-c:v", "libx264",
            "-preset", preset,
            "-crf", str(crf),
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            "-progress", "pipe:1",   # 输出进度到 stdout
            "-stats_period", "1",     # 每秒更新一次进度
            output_path,
        ]

        print(f"[合并] 开始合并 {total} 个片段 → {output_path}")
        print(f"[编码] 分辨率: {target_width}x{target_height} | CRF: {crf} | Preset: {preset}\n")

        # 5. 执行 FFmpeg，实时打印进度
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        current_file_idx = 0
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
            # FFmpeg concat 模式进度格式示例:
            # frame=1234
            # fps=...
            # out_time_us=1234567
            # speed=...
            # progress=...
            if line.startswith("out_time_us=") or line.startswith("out_time_ms="):
                # 解析时间
                try:
                    us = int(line.split("=")[1])
                    elapsed_sec = us / 1_000_000
                    pct = min(100, elapsed_sec / total_duration * 100) if total_duration > 0 else 0
                    mins = int(elapsed_sec // 60)
                    secs = int(elapsed_sec % 60)
                    bar = "█" * int(pct // 2) + "░" * (50 - int(pct // 2))
                    print(
                        f"\r[进度] [{bar}] {pct:5.1f}% | {mins:02d}:{secs:02d} / "
                        f"{int(total_duration//60):02d}:{int(total_duration%60):02d}  ",
                        end="", flush=True
                    )
                except Exception:
                    pass
            elif line.startswith("progress="):
                # 某个文件处理完成时 progress=end
                pass  # 在 out_time_us 里已处理
            elif "Error" in line or "Invalid" in line:
                print(f"\n[FFmpeg 警告] {line}")

        process.wait()

        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg 执行失败，返回码: {process.returncode}")

        print(f"\n\n[完成] ✅ 视频已保存至: {output_path}")
        if os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"[完成] 文件大小: {size_mb:.1f} MB")


# ------------------------------------------------------------
# 命令行入口
# ------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="视频片段合并器 - 合并文件夹内所有 .mp4 为单一视频",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python merge_videos.py -i ./clips -o ./output.mp4
  python merge_videos.py -i ./clips -o ./output.mp4 -w 1280 -h 720 -crf 20
        """,
    )
    parser.add_argument("-i", "--input", required=True, help="包含 .mp4 文件的文件夹路径")
    parser.add_argument("-o", "--output", required=True, help="输出文件路径（.mp4）")
    parser.add_argument("-w", "--width", type=int, default=1920, help="目标宽度（默认 1920）")
    parser.add_argument("-h", "--height", type=int, default=1080, help="目标高度（默认 1080）")
    parser.add_argument("-crf", type=int, default=23, help="H.264 CRF 质量（0-51，越小越高，默认 23）")
    parser.add_argument("-p", "--preset", default="medium",
                        choices=["ultrafast", "superfast", "veryfast", "faster", "fast",
                                  "medium", "slow", "slower", "veryslow"],
                        help="H.264 编码速度（默认 medium）")

    args = parser.parse_args()

    try:
        merge_videos(
            input_folder=args.input,
            output_path=args.output,
            target_width=args.width,
            target_height=args.height,
            crf=args.crf,
            preset=args.preset,
        )
    except FileNotFoundError as e:
        print(f"[错误] {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"[错误] {e}", file=sys.stderr)
        sys.exit(2)
    except RuntimeError as e:
        print(f"[错误] {e}", file=sys.stderr)
        sys.exit(3)
    except KeyboardInterrupt:
        print("\n[中断] 用户取消合并。", file=sys.stderr)
        sys.exit(4)
