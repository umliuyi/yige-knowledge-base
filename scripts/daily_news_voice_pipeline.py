# -*- coding: utf-8 -*-
# 早报视频流水线: edge-tts云扬(zh-CN-YunyangNeural) + PIL幻灯片 + FFmpeg合并
# 输出: C:\Users\Administrator\.openclaw-autoclaw\media\daily_news_voice_test.mp4
#
import asyncio
import os
import re
import sys
import subprocess
import shutil

os.environ["PYTHONIOENCODING"] = "utf-8"

import edge_tts
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

WS        = r"C:\Users\Administrator\.openclaw-autoclaw\workspace"
MEDIA_DIR = r"C:\Users\Administrator\.openclaw-autoclaw\media"
SLIDES_DIR = os.path.join(WS, "temp_slides")
os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(SLIDES_DIR, exist_ok=True)

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1920, 1080

BG     = (8,   8,  18)
ORANGE = (255, 87,  34)
CYAN   = (0,  188, 212)
WHITE  = (255, 255, 255)
GRAY   = (160, 160, 170)

VOICE       = "zh-CN-YunyangNeural"
TTS_RATE    = "+0%"
TTS_PITCH   = "+0Hz"

AUTHOR_NAME = "刘一"
AUTHOR_TAG  = "精算师聊健康"


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def gradient_bg(img, draw):
    w, h = img.size
    top, bot = (12, 12, 30), (4, 4, 12)
    for y in range(h):
        r = int(top[0]*(1-y/h) + bot[0]*y/h)
        g = int(top[1]*(1-y/h) + bot[1]*y/h)
        b = int(top[2]*(1-y/h) + bot[2]*y/h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def add_left_bar(draw, color=ORANGE, width=6):
    draw.rectangle([(0, 0), (width, H)], fill=color)


def add_bottom_line(draw, color=CYAN):
    draw.rectangle([(0, H-5), (W, H)], fill=color)


def add_top_bar(draw, color=ORANGE):
    draw.rectangle([(0, 0), (W, 8)], fill=color)


def add_page_num(draw, num, total):
    txt = f"{num}/{total}"
    draw.text((W-100, H-70), txt, font=font(22), fill=GRAY)


def make_cover(date_str, tagline, total):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient_bg(img, draw)
    add_top_bar(draw)
    draw.text((80, 60), date_str, font=font(32), fill=GRAY)
    f_title = font(96, bold=True)
    title = "大健康早报"
    bbox = draw.textbbox((0, 0), title, font=f_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw)//2, H//2 - 160), title, font=f_title, fill=WHITE)
    f_sub = font(44)
    bbox2 = draw.textbbox((0, 0), tagline, font=f_sub)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W - sw)//2, H//2 - 40), tagline, font=f_sub, fill=GRAY)
    f_acc = font(36)
    acc = f"{AUTHOR_NAME} | {AUTHOR_TAG}"
    abbox = draw.textbbox((0, 0), acc, font=f_acc)
    aw = abbox[2] - abbox[0]
    draw.text(((W - aw)//2, H - 130), acc, font=f_acc, fill=ORANGE)
    add_bottom_line(draw)
    path = os.path.join(SLIDES_DIR, "00_cover.png")
    img.save(path, "PNG")
    print(f"  [封面] saved")
    return path, "封面"


def make_news_slide(num, total, tag, title, points):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient_bg(img, draw)
    add_left_bar(draw, ORANGE, 6)
    draw.text((80, 55), f"[{num}/{total}] {tag}", font=font(26), fill=ORANGE)
    draw.text((80, 110), title, font=font(58, bold=True), fill=WHITE)
    draw.rectangle([(80, 200), (W - 80, 204)], fill=ORANGE)
    f_pt = font(36)
    y = 240
    for line in points:
        line = line.strip()
        if not line:
            continue
        if line.startswith("•"):
            draw.ellipse([(85, y+10), (100, y+25)], fill=ORANGE)
            draw.text((115, y), line[1:].strip(), font=f_pt, fill=WHITE)
        else:
            draw.text((100, y), line, font=f_pt, fill=GRAY)
        y += 65
        if y > H - 120:
            break
    add_page_num(draw, num, total)
    add_bottom_line(draw)
    slug = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "", title)[:8]
    path = os.path.join(SLIDES_DIR, f"0{num}_{slug}.png")
    img.save(path, "PNG")
    print(f"  [新闻{num}] {title[:20]}")
    return path, title


def make_closing():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient_bg(img, draw)
    f_main = font(90, bold=True)
    t1 = "关注我"
    bbox = draw.textbbox((0, 0), t1, font=f_main)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw)//2, H//2 - 100), t1, font=f_main, fill=WHITE)
    f_sub = font(52)
    t2 = f"{AUTHOR_NAME} | {AUTHOR_TAG}"
    bbox2 = draw.textbbox((0, 0), t2, font=f_sub)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W - sw)//2, H//2), t2, font=f_sub, fill=ORANGE)
    f_date = font(30)
    t3 = "每早8:30 | 大健康资讯早知道"
    bbox3 = draw.textbbox((0, 0), t3, font=f_date)
    sw3 = bbox3[2] - bbox3[0]
    draw.text(((W - sw3)//2, H//2 + 80), t3, font=f_date, fill=GRAY)
    add_bottom_line(draw)
    path = os.path.join(SLIDES_DIR, "99_closing.png")
    img.save(path, "PNG")
    print(f"  [结尾] 关注我")
    return path, "结尾"


def parse_lecheng_daily():
    """读取乐城早报，提取最多5条新闻（有实质内容，非'今日无更新'）"""
    daily_dir = os.path.join(WS, "lobster-team", "research", "daily")
    md_path = os.path.join(daily_dir, "2026-05-13.md")
    if not os.path.exists(md_path):
        files = sorted(os.listdir(daily_dir), reverse=True)
        md_path = os.path.join(daily_dir, files[0])

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    news_items = []

    # Strategy: find the LATEST date block (most recent section), then extract
    # hospital entries from ALL date blocks (prioritize today's entries)
    # Split by ## date headers
    date_blocks = re.split(r"\n(?=## \d{4}-)", content)

    for block in date_blocks:
        if not block.strip():
            continue
        lines = block.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            m = re.match(r"^\*\*(.+?)\*\*[：:]\s*(.+)$", line)
            if not m:
                continue
            hospital = m.group(1).strip()
            rest = m.group(2).strip()
            # Skip purely "今日无更新" entries (but don't skip if there's additional content)
            if rest == "今日无更新" or rest == "今日无更新。":
                continue
            # Skip duplicates by hospital name
            if any(h == hospital for h, c in news_items):
                continue
            if rest and len(rest) > 3:
                news_items.append((hospital, rest))
            if len(news_items) >= 5:
                break
        if len(news_items) >= 5:
            break

    # Fallback: if still nothing, use general health news
    if not news_items:
        news_items = [
            ("乐城动态", "博鳌乐城持续引进国际最新药械，打造跨境医疗新高地"),
            ("新药进展", "多个生物医学新技术项目在乐城落地，惠及患者"),
            ("医疗服务", "乐城各大医院提供国际前沿治疗方案"),
            ("健康资讯", "乐城创新疗法为患者带来新希望"),
            ("行业观察", "大健康行业迎来快速发展期"),
        ]

    return news_items, md_path


async def generate_tts(text, output_path, voice=VOICE, rate=TTS_RATE, pitch=TTS_PITCH):
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await communicate.save(output_path)
        size = os.path.getsize(output_path)
        print(f"  TTS OK: {os.path.basename(output_path)} ({size:,} bytes)")
        return True
    except Exception as e:
        print(f"  TTS error: {e}")
        return False


async def generate_all_tts(scripts):
    audio_files = []
    for i, text in enumerate(scripts):
        out = os.path.join(SLIDES_DIR, f"audio_{i:02d}.mp3")
        ok = await generate_tts(text, out)
        if not ok or not (os.path.exists(out) and os.path.getsize(out) > 500):
            # Create a silence fallback
            await generate_tts(" ", out)
        audio_files.append(out)
        await asyncio.sleep(0.3)
    return audio_files


def run_ffmpeg(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(f"    FFmpeg error: {r.stderr[-300:]}")
        return False
    return True


def make_clip(png_path, clip_path, duration):
    cmd = [
        FFMPEG, "-loop", "1", "-i", png_path,
        "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
        "-t", str(duration), "-r", "24", "-y", clip_path
    ]
    ok = run_ffmpeg(cmd)
    if ok:
        sz = os.path.getsize(clip_path)
        print(f"    clip OK: {os.path.basename(clip_path)} ({sz:,} bytes, {duration}s)")
    return ok


def estimate_duration(text):
    chinese_chars = len(re.findall(r"[\u4e00-\u9fa5]", text))
    return max(4, min(15, int(chinese_chars / 4.5)))


def concat_videos(clip_list, list_path, output_path):
    with open(list_path, "w", encoding="utf-8") as f:
        for cf in clip_list:
            f.write(f"file '{cf}'\n")
    cmd = [
        FFMPEG, "-f", "concat", "-safe", "0",
        "-i", list_path,
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac", "-y", output_path
    ]
    ok = run_ffmpeg(cmd)
    if ok:
        print(f"    concat OK: {os.path.getsize(output_path):,} bytes")
    return ok


def merge_audio_video(video_path, audio_path, output_path):
    cmd = [
        FFMPEG, "-i", video_path, "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac",
        "-shortest", "-y", output_path
    ]
    ok = run_ffmpeg(cmd)
    if ok:
        print(f"    merged OK: {os.path.getsize(output_path):,} bytes")
    return ok


async def run_pipeline():
    print("=" * 60)
    print("  早报视频流水线 | edge-tts 云扬(zh-CN-YunyangNeural)")
    print("=" * 60)

    print("\n[1/5] 解析乐城早报...")
    news_items, md_path = parse_lecheng_daily()
    print(f"  来源: {os.path.basename(md_path)}")
    print(f"  新闻: {len(news_items)} 条")
    for h, c in news_items[:3]:
        print(f"    - {h}: {c[:40]}")

    print("\n[2/5] 加载分镜脚本...")
    storyboard_path = os.path.join(WS, "scripts", "storyboard_generator.py")
    if os.path.exists(storyboard_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("storyboard", storyboard_path)
        sb = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sb)
        # Pad to 5 items for storyboard
        padded = list(news_items)
        while len(padded) < 5:
            padded.append((f"健康要点{len(padded)+1}", "持续关注乐城创新疗法与大健康行业最新动态"))
        storyboard_news = [(f"{h}:{c[:30]}", c, "资讯") for h, c in padded[:5]]
        shots = sb.generate_storyboard(
            storyboard_news,
            "大健康早报 · 乐城动态",
            "用精算师的视角，看懂健康行业"
        )
        print(f"  分镜: {len(shots)} 个镜头")
    else:
        print("  分镜脚本未找到，跳过")
        shots = []

    print("\n[3/5] 生成幻灯片 (7页: 封面+5条新闻+结尾)...")
    # Always 7 pages: cover + 5 news + closing
    total = 7  # 封面+5新闻+结尾固定为7页
    slide_paths = []
    slide_labels = []
    scripts = []

    # Page 1: 封面
    p, l = make_cover("2026年05月13日", "用精算师的视角，看懂健康行业", total)
    slide_paths.append(p); slide_labels.append(l)
    scripts.append("欢迎收看今日大健康早报，2026年05月13日，乐城健康资讯早知道。")

    # Pages 2-6: 新闻（循环补齐确保5条）
    for i in range(5):
        hospital, content = news_items[i % len(news_items)] if news_items else (f"健康要点{i+1}", "持续关注乐城创新疗法与大健康行业最新动态")
        num = i + 1
        title_short = f"{hospital}最新动态"
        pts = [content[:80] if content else "持续关注乐城创新疗法进展", "更多详情请关注乐城动态"]
        p, l = make_news_slide(num, total, "乐城动态", title_short, pts)
        slide_paths.append(p); slide_labels.append(l)
        scripts.append(f"第{num}条，{title_short}。{content if content else '持续关注大健康行业最新动态'}。")

    # Page 7: 结尾
    p, l = make_closing()
    slide_paths.append(p); slide_labels.append(l)
    scripts.append("关注我，每天早八点半，帮你算清楚大健康这笔账。刘一，精算师聊健康。")

    print(f"  共 {len(slide_paths)} 页 (封面+5条新闻+结尾)")

    print(f"\n[4/5] TTS配音 | voice={VOICE} rate={TTS_RATE} pitch={TTS_PITCH}...")
    audio_files = await generate_all_tts(scripts)
    valid_audios = [af for af in audio_files if os.path.exists(af) and os.path.getsize(af) > 500]
    print(f"  音频: {len(valid_audios)}/{len(audio_files)} 有效")

    print("\n[5/5] 生成视频片段...")
    clip_files = []
    for i, (png, label) in enumerate(zip(slide_paths, slide_labels)):
        script_text = scripts[i] if i < len(scripts) else ""
        dur = estimate_duration(script_text)
        clip = os.path.join(SLIDES_DIR, f"clip_{i:02d}.mp4")
        print(f"  [{i+1}/{len(slide_paths)}] {label[:25]} ({dur}s)")
        ok = make_clip(png, clip, dur)
        if ok:
            clip_files.append(clip)

    if not clip_files:
        print("ERROR: 没有生成任何视频片段!")
        return None

    print("\n[6/6] 合并视频...")
    video_only = os.path.join(SLIDES_DIR, "video_only.mp4")
    concat_videos(clip_files, os.path.join(SLIDES_DIR, "clips.txt"), video_only)

    audio_concat_path = os.path.join(SLIDES_DIR, "audio_concat.mp3")
    audio_valid = [af for af in audio_files if os.path.exists(af) and os.path.getsize(af) > 500]
    has_audio = False
    if audio_valid:
        concat_audio_list = os.path.join(SLIDES_DIR, "audio_concat_list.txt")
        with open(concat_audio_list, "w", encoding="utf-8") as f:
            for af in audio_valid:
                f.write(f"file '{af}'\n")
        cmd = [
            FFMPEG, "-f", "concat", "-safe", "0",
            "-i", concat_audio_list,
            "-c:a", "libmp3lame", "-q:a", "2", "-y", audio_concat_path
        ]
        has_audio = run_ffmpeg(cmd)
        if has_audio:
            print(f"  音频合并 OK: {os.path.getsize(audio_concat_path):,} bytes")

    output_path = os.path.join(MEDIA_DIR, "daily_news_voice_test.mp4")
    if has_audio:
        merge_ok = merge_audio_video(video_only, audio_concat_path, output_path)
    else:
        if os.path.exists(video_only):
            shutil.copy(video_only, output_path)
            merge_ok = True
        else:
            merge_ok = False

    if merge_ok and os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"\n{'=' * 60}")
        print(f"  完成!")
        print(f"  输出: {output_path}")
        print(f"  大小: {size_mb:.1f} MB")
        print(f"  页面: {len(slide_paths)} 页 (封面+5新闻+结尾)")
        print(f"  配音: {VOICE} | rate={TTS_RATE} | pitch={TTS_PITCH}")
        print(f"  分镜: {len(shots)} 个镜头")
        print(f"{'=' * 60}")
        return output_path
    else:
        print("ERROR: 视频生成失败!")
        return None


if __name__ == "__main__":
    result = asyncio.run(run_pipeline())
    sys.exit(0 if result else 1)