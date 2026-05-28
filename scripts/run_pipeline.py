#!/usr/bin/env python3
"""
早报视频全自动流水线 v2
从调研龙虾的MD文件 → 生成幻灯片 → TTS配音 → FFmpeg合成视频

用法: python run_pipeline.py [日期]
日期默认今天，格式 YYYY-MM-DD
"""
import subprocess, os, re, sys
from datetime import datetime

TODAY = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
WORKSPACE = r"C:\Users\Administrator\.openclaw-autoclaw\workspace"
SCRIPTS_DIR = os.path.join(WORKSPACE, "scripts")
OUTPUT_DIR = r"C:\Users\Administrator\Downloads\videos\daily_news"
SOURCE_MD = os.path.join(WORKSPACE, "lobster-team", "research", "daily", f"{TODAY}.md")

# 如果今天的MD不存在，找最近的一天
if not os.path.exists(SOURCE_MD):
    daily_dir = os.path.join(WORKSPACE, "lobster-team", "research", "daily")
    files = sorted([f for f in os.listdir(daily_dir) if f.endswith(".md")], reverse=True)
    if files:
        SOURCE_MD = os.path.join(daily_dir, files[0])
        print(f"[INFO] 今天的MD不存在，使用最新: {files[0]}")
    else:
        print(f"[ERROR] 没有找到任何早报MD文件")
        sys.exit(1)

print(f"[INFO] 源文件: {SOURCE_MD}")

# ========== Step 1: 改写 slides 脚本的 SOURCE_FILE ==========
slides_script = os.path.join(SCRIPTS_DIR, "daily_news_slides.py")
with open(slides_script, "r", encoding="utf-8") as f:
    content = f.read()

# 替换 SOURCE_FILE
old_source = re.search(r'SOURCE_FILE\s*=\s*r"[^\"]+\"', content)
if old_source:
    content = content.replace(old_source.group(), f'SOURCE_FILE = r"{SOURCE_MD}"')
    with open(slides_script, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[1/4] 已更新 slides 源文件 -> {os.path.basename(SOURCE_MD)}")
else:
    print(f"[WARN] 未找到 SOURCE_FILE 替换点")

# ========== Step 2: 生成幻灯片 ==========
print(f"[2/4] 生成幻灯片...")
os.makedirs(OUTPUT_DIR, exist_ok=True)
result = subprocess.run(
    ["python", slides_script],
    capture_output=True, text=True,
    cwd=SCRIPTS_DIR,
    env={**os.environ, "PYTHONIOENCODING": "utf-8"}
)
if result.returncode != 0:
    print(f"[ERROR] 幻灯片失败:\n{result.stderr[-500:]}")
else:
    print(f"[OK] 幻灯片生成完成")

# ========== Step 3: TTS配音 + FFmpeg合成 ==========
print(f"[3/4] TTS配音 + 视频合成...")
video_script = os.path.join(SCRIPTS_DIR, "assemble_daily_news.py")
result = subprocess.run(
    ["python", video_script],
    capture_output=True, text=True,
    cwd=SCRIPTS_DIR,
    env={**os.environ, "PYTHONIOENCODING": "utf-8"}
)
if result.returncode != 0:
    print(f"[ERROR] 视频合成失败:\n{result.stderr[-500:]}")
else:
    print(f"[OK] 视频合成完成")

# ========== Step 4: 找输出文件 ==========
print(f"[4/4] 检查输出...")
for fname in os.listdir(OUTPUT_DIR):
    if TODAY.replace("-", "") in fname and fname.endswith(".mp4"):
        fpath = os.path.join(OUTPUT_DIR, fname)
        size = os.path.getsize(fpath) // 1024
        print(f"[OK] 视频: {fname} ({size}KB)")
        break
else:
    # 找最新的mp4
    mp4s = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".mp4")]
    if mp4s:
        latest = max(mp4s, key=lambda f: os.path.getmtime(os.path.join(OUTPUT_DIR, f)))
        fpath = os.path.join(OUTPUT_DIR, latest)
        size = os.path.getsize(fpath) // 1024
        print(f"[OK] 视频: {latest} ({size}KB)")
    else:
        print(f"[WARN] 未找到mp4文件，检查以下目录: {OUTPUT_DIR}")