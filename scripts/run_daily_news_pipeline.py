"""
早报视频全自动流水线 - 一键生成
触发路径: 调研龙虾生成MD → 生成幻灯片 → TTS配音 → FFmpeg合成视频

用法: python run_daily_news_pipeline.py
"""
import subprocess
import os
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")
WORKSPACE = r"C:\Users\Administrator\.openclaw-autoclaw\workspace"
SCRIPTS_DIR = os.path.join(WORKSPACE, "scripts")
OUTPUT_BASE = r"C:\Users\Administrator\Downloads\videos\daily_news"
DAILY_NEWS_DIR = os.path.join(OUTPUT_BASE, TODAY)

# 1. 生成幻灯片
print(f"[1/3] 生成幻灯片: {TODAY}")
slide_cmd = [
    "python",
    os.path.join(SCRIPTS_DIR, "daily_news_slides.py"),
    "--date", TODAY,
    "--output", DAILY_NEWS_DIR
]
result = subprocess.run(slide_cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"幻灯片生成失败: {result.stderr}")
else:
    print(f"幻灯片生成完成")

# 2. TTS配音 + 合成视频
print(f"[2/3] 配音 + 合成视频")
video_cmd = [
    "python",
    os.path.join(SCRIPTS_DIR, "assemble_daily_news.py"),
    "--date", TODAY,
    "--slides-dir", DAILY_NEWS_DIR,
    "--output-dir", OUTPUT_BASE
]
result = subprocess.run(video_cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"视频合成失败: {result.stderr}")
else:
    print(f"视频合成完成")

# 3. 输出结果
output_video = os.path.join(OUTPUT_BASE, f"daily_news_{TODAY}.mp4")
if os.path.exists(output_video):
    size = os.path.getsize(output_video) // 1024
    print(f"[OK] 视频已生成: {output_video} ({size}KB)")
else:
    print(f"[WARN] 视频文件未找到: {output_video}")
