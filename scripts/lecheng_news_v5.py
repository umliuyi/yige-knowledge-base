#!/usr/bin/env python3
"""
乐城早报 v5 - 正确流程：每段视频+音频单独生成，再拼接
"""
from PIL import Image, ImageDraw, ImageFont
import os, subprocess, asyncio, edge_tts
from pathlib import Path

SOURCE_FILE = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\日报\2026-05-11-早报-乐城视角.md"
OUTPUT_DIR = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v3"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1920, 1080
BG = (6, 8, 20); ORANGE = (255,107,30); WHITE = (255,255,255); GRAY = (140,145,160)

def font(size):
    for p in ["C:/Windows/Fonts/msyh.ttc","C:/Windows/Fonts/simhei.ttf"]:
        try: return ImageFont.truetype(p, size)
        except: continue
    return ImageFont.load_default()

def gradient_bg(img):
    draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(6*(1-y/H)+2*y/H); g = int(8*(1-y/H)+4*y/H); b = int(20*(1-y/H)+12*y/H)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

def make_slide(title="", subtitle="", body=None, footer=""):
    img = Image.new("RGB", (W,H), BG)
    gradient_bg(img)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0,0),(W,4)], fill=ORANGE)
    y = 80
    if title: draw.text((80,y), title, font=font(52), fill=ORANGE); y += 90
    if subtitle: draw.text((80,y), subtitle, font=font(26), fill=GRAY); y += 55
    if body:
        for line in body:
            draw.text((80,y), line, font=font(24), fill=WHITE); y += 48
    if footer: draw.text((80,H-60), footer, font=font(18), fill=GRAY)
    return img

def parse_source():
    with open(SOURCE_FILE, encoding="utf-8") as f: content = f.read()
    pages = []
    pages.append({"title":"乐城视角 · 大健康早报","subtitle":"2026年5月11日","body":[],"footer":"刘一 · 精算师聊健康","duration":6})
    idx1 = content.find("新闻一："); idx2 = content.find("新闻二：")
    for start, end in [(idx1, idx2), (idx2, len(content))]:
        if start == -1: continue
        section = content[start:end]
        lines = section.split("\n")
        title = ""; body = []; capture = False
        for line in lines:
            if "新闻" in line and "：" in line:
                title = line.split("：")[1].split("，")[0].split("（")[0].strip()
                capture = True; continue
            if "**" in line: capture = False; continue
            if line.startswith("---"): continue
            if capture and line.strip():
                clean = line.strip().replace("**","").strip()
                if clean: body.append(clean[:90])
        if title:
            pages.append({"title":title,"subtitle":"","body":body[:4],"footer":"刘一 · 精算师聊健康","duration":12})
    pages.append({"title":"感谢观看","subtitle":"关注我，获取更多乐城医疗资讯","body":[],"footer":"刘一 · 精算师聊健康","duration":6})
    return pages

async def gen_audio(text, output, voice="zh-CN-YunxiNeural"):
    try:
        comm = edge_tts.Communicate(text, voice)
        await comm.save(output)
        return True
    except: return False

async def generate_audio_files(pages):
    results = []
    for i, page in enumerate(pages):
        parts = [page.get("title",""), page.get("subtitle","")]
        parts.extend(page.get("body",[]))
        text = "，".join([p for p in parts if p]) if parts else "请观看"
        out = os.path.join(OUTPUT_DIR, f"seg_audio_{i}.wav")
        ok = await gen_audio(text, out) if len(text)>5 else False
        results.append(out if ok else None)
        print(f"  Audio {i}: {'OK' if ok else 'SKIP'}")
    return results

def make_segment(slide_path, audio_path, duration, output):
    """用FFmpeg把图片+音频合并成一个视频片段"""
    ffmpeg = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
    if audio_path and os.path.exists(audio_path):
        cmd = [
            ffmpeg, "-y",
            "-loop", "1", "-i", slide_path,
            "-i", audio_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-pix_fmt", "yuv420p", "-r", "25",
            "-t", str(duration),
            "-vf", "scale=1920:1080",
            "-c:a", "aac", "-b:a", "128k",
            "-shortest", output
        ]
    else:
        cmd = [
            ffmpeg, "-y",
            "-loop", "1", "-i", slide_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-pix_fmt", "yuv420p", "-r", "25",
            "-t", str(duration),
            "-vf", "scale=1920:1080",
            output
        ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0

def concatenate_segments(segment_files, output):
    """把所有片段拼接成一个视频"""
    ffmpeg = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
    list_file = os.path.join(OUTPUT_DIR, "segments.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for seg in segment_files:
            if seg and os.path.exists(seg):
                f.write(f"file '{seg}'\n")
    if len(segment_files) <= 1:
        print("No segments to concatenate"); return False
    cmd = [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", list_file,
           "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "aac", output]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("Concat错误:", r.stderr[-400:])
        return False
    return True

def main():
    print("=== Lecheng Daily News v5 ===")
    pages = parse_source()
    print(f"Pages: {len(pages)}")
    
    # 1. 生成幻灯片
    slide_files = []
    for i, page in enumerate(pages):
        img = make_slide(page.get("title",""), page.get("subtitle",""), page.get("body",[]), page.get("footer",""))
        p = os.path.join(OUTPUT_DIR, f"slide_{i}.png")
        img.save(p); slide_files.append(p)
        print(f"  Slide {i} OK")
    
    # 2. 生成配音
    print("Generating audio...")
    audio_files = asyncio.run(generate_audio_files(pages))
    
    # 3. 每段生成视频片段
    segment_files = []
    for i, page in enumerate(pages):
        seg = os.path.join(OUTPUT_DIR, f"seg_{i}.mp4")
        ok = make_segment(slide_files[i], audio_files[i], page["duration"], seg)
        if ok:
            segment_files.append(seg)
            print(f"  Segment {i} OK ({os.path.getsize(seg)//1024}KB)")
        else:
            segment_files.append(None)
    
    # 4. 拼接
    output = os.path.join(OUTPUT_DIR, "daily_news_20260511_v5.mp4")
    concatenate_segments(segment_files, output)
    if os.path.exists(output):
        print(f"Done: {output} ({os.path.getsize(output)//1024}KB)")

if __name__ == "__main__":
    main()
