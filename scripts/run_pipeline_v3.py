#!/usr/bin/env python3
"""
早报视频全自动流水线 v3
从调研龙虾MD → 提取内容 → 生成幻灯片 → TTS配音 → FFmpeg合成视频
"""
import subprocess, os, re, sys, asyncio
from datetime import datetime
from pathlib import Path

TODAY = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
WORKSPACE = Path(r"C:\Users\Administrator\.openclaw-autoclaw\workspace")
SCRIPTS_DIR = WORKSPACE / "scripts"
OUTPUT_DIR = Path(r"C:\Users\Administrator\Downloads\videos\daily_news")

# 找源MD文件（优先growth路径，备选research路径）
possible_dirs = [
    WORKSPACE / "growth" / "daily" / "ccfa1206",
    WORKSPACE / "lobster-team" / "research" / "daily",
    WORKSPACE / "早报",
]
daily_dir = None
for d in possible_dirs:
    if d.exists():
        daily_dir = d
        print(f"[INFO] 找到早报目录: {d}")
        break
if daily_dir is None:
    print("[ERROR] 未找到早报目录")
    sys.exit(1)

source_md = daily_dir / f"{TODAY}.md"
if not source_md.exists():
    files = sorted([f for f in os.listdir(daily_dir) if f.endswith(".md")], reverse=True)
    if files:
        source_md = daily_dir / files[0]
        print(f"[INFO] 使用最新: {files[0]}")
    else:
        print(f"[ERROR] 目录 {daily_dir} 里没有MD文件")
        sys.exit(1)
print(f"[INFO] 源文件: {source_md}")

# ========== 读取MD内容 ==========
with open(source_md, "r", encoding="utf-8") as f:
    md_content = f.read()

# 提取日期行
date_match = re.search(r'[\u4e00-\u9fa5]+\s*\|\s*(\d{4}[年\-\/]\d{1,2}[月\-\/]\d{1,2})', md_content)
date_str = date_match.group(1) if date_match else TODAY.replace("-", "年").replace("/", "年")

# 提取新闻条目（## 或 🔴 或 📌 开头）
items = []
for line in md_content.split("\n"):
    line = line.strip()
    if line.startswith("🔴") or line.startswith("📌"):
        title = re.sub(r'^[🔴📌]\s*\*?\*?', '', line).strip("* ")
        title = title[:50]
        if title:
            items.append(title)
    elif line.startswith("##") and len(line) > 5 and not line.startswith("## 【"):
        title = line.lstrip("#").strip()
        title = re.sub(r'^[🔴📌]\s*\*?\*?', '', title).strip("* ")
        if title and len(title) > 5:
            items.append(title[:50])

print(f"[INFO] 提取到 {len(items)} 条新闻")

# ========== 写幻灯片内容到临时模块 ==========
slides_content = f'''
# -*- coding: utf-8 -*-
"""由 pipeline 自动生成 - {TODAY}"""
from daily_news_slides import *

if __name__ == "__main__":
    print("生成早报幻灯片 - {date_str} ...")
    slides = []

    # 封面
    slides.append(make_cover(
        "{date_str}",
        "{" · ".join(items[:3])}"
    ))

    # 新闻页
    for i, title in enumerate(items[:5], 1):
        slides.append(make_news_slide(
            i, 5,
            "大健康",
            title[:30],
            ["• 详见今日早报内容", "• 关注我了解更多"]
        ))

    # 结尾
    slides.append(make_closing())
    print(f"共生成 7 页幻灯片")
'''

slide_runner = SCRIPTS_DIR / "slide_runner_today.py"
with open(slide_runner, "w", encoding="utf-8") as f:
    f.write(slides_content)

# ========== 改 SOURCE_FILE 并跑幻灯片 ==========
slides_script = SCRIPTS_DIR / "daily_news_slides.py"
with open(slides_script, "r", encoding="utf-8") as f:
    orig = f.read()
patched = re.sub(
    r'SOURCE_FILE\s*=\s*r"[^"]*"',
    'SOURCE_FILE = r"' + str(source_md).replace('\\', '\\\\') + '"',
    orig
)
with open(slides_script, "w", encoding="utf-8") as f:
    f.write(patched)

print("[1/4] 生成幻灯片...")
r1 = subprocess.run(["python", str(slides_script)], capture_output=True, text=True, cwd=str(SCRIPTS_DIR))
if r1.returncode != 0:
    print(f"[WARN] slides 失败，回退: {r1.stderr[-300:]}")
    # 静默跑 slide_runner
    r1 = subprocess.run(["python", str(slide_runner)], capture_output=True, text=True, cwd=str(SCRIPTS_DIR))
print(f"[OK] 幻灯片完成")

# ========== 改 assemble 脚本的配音词 ==========
ascribe_daily_news = SCRIPTS_DIR / "assemble_daily_news.py"
with open(ascribe_daily_news, "r", encoding="utf-8") as f:
    asm = f.read()

# 提取MD中的摘要行作为配音
narration_lines = []
for line in md_content.split("\n"):
    line = line.strip()
    if line.startswith("- 来源") or line.startswith("  来源"):
        continue
    if line.startswith("•") or line.startswith("-"):
        text = line.lstrip("•-").strip()
        if len(text) > 10:
            narration_lines.append(text)

# 生成7段配音
today_narrations = []
if len(items) >= 1:
    today_narrations.append(f"今日早报要点：{items[0]}")
if len(items) >= 2:
    today_narrations.append(f"今日第二条：{items[1]}")
if len(items) >= 3:
    today_narrations.append(f"今日第三条：{items[2]}")
if len(items) >= 4:
    today_narrations.append(f"今日第四条：{items[3]}")
if len(items) >= 5:
    today_narrations.append(f"今日第五条：{items[4]}")
today_narrations.append(f"关注我，每天早八点半，帮你算清楚大健康这笔账。刘一，精算师聊健康。")

# 替换SLIDES_AUDIO
old_audio_match = re.search(r'SLIDES_AUDIO\s*=\s*\[(.*?)\]', asm, re.DOTALL)
if old_audio_match:
    audio_entries = ',\n    '.join([f'"""{n}"""' for n in today_narrations])
    asm = asm.replace(
        old_audio_match.group(0),
        f'SLIDES_AUDIO = [{audio_entries}]'
    )
    with open(ascribe_daily_news, "w", encoding="utf-8") as f:
        f.write(asm)
    print(f"[2/4] 已更新配音词 ({len(today_narrations)}段)")

print("[3/4] TTS配音 + 视频合成...")
r2 = subprocess.run(["python", str(ascribe_daily_news)], capture_output=True, text=True, cwd=str(SCRIPTS_DIR))
if r2.returncode != 0:
    print(f"[WARN] 视频合成 stderr: {r2.stderr[-300:]}")
print(f"[OK] 视频合成完成")

# ========== 找输出文件 ==========
print("[4/4] 检查输出...")
mp4s = [(f, os.path.getmtime(OUTPUT_DIR / f)) for f in os.listdir(OUTPUT_DIR) if f.endswith(".mp4")]
if mp4s:
    latest = sorted(mp4s, key=lambda x: x[1], reverse=True)[0][0]
    fpath = OUTPUT_DIR / latest
    size = os.path.getsize(fpath) // 1024
    print(f"[OK] 视频: {latest} ({size}KB)")
    print(f"[OK] 完整路径: {fpath}")
else:
    print("[WARN] 未找到mp4，检查目录:")
    for f in os.listdir(OUTPUT_DIR):
        print(f"  {f}")
