#!/usr/bin/env python3
"""
乐城早报 v4 - 修复版
"""
from PIL import Image, ImageDraw, ImageFont
import os, subprocess, asyncio, edge_tts
from pathlib import Path

# ============ 配置 ============
SOURCE_FILE = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\日报\2026-05-11-早报-乐城视角.md"
OUTPUT_DIR  = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v3"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1920, 1080
BG      = (6, 8, 20)
ORANGE  = (255, 107, 30)
WHITE   = (255, 255, 255)
GRAY    = (140, 145, 160)

def font(size):
    for p in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

def gradient_bg(img):
    draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(6 * (1-y/H) + 2 * y/H)
        g = int(8 * (1-y/H) + 4 * y/H)
        b = int(20 * (1-y/H) + 12 * y/H)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

def make_slide(title="", subtitle="", body=None, footer=""):
    img = Image.new("RGB", (W, H), BG)
    gradient_bg(img)
    draw = ImageDraw.Draw(img)
    
    # 顶部橙色线
    draw.rectangle([(0,0),(W,4)], fill=ORANGE)
    
    y = 80
    if title:
        draw.text((80, y), title, font=font(52), fill=ORANGE)
        y += 80
    if subtitle:
        draw.text((80, y), subtitle, font=font(26), fill=GRAY)
        y += 50
    if body:
        for line in body:
            draw.text((80, y), line, font=font(24), fill=WHITE)
            y += 45
    if footer:
        draw.text((80, H-60), footer, font=font(18), fill=GRAY)
    
    return img

def parse_source():
    with open(SOURCE_FILE, encoding="utf-8") as f:
        content = f.read()
    
    pages = []
    
    # 封面
    pages.append({
        "title": "乐城视角 · 大健康早报",
        "subtitle": "2026年5月11日",
        "body": [],
        "footer": "刘一 · 精算师聊健康",
        "duration": 5
    })
    
    # 提取新闻一
    idx1 = content.find("新闻一：")
    idx2 = content.find("新闻二：")
    news1 = content[idx1:idx2] if idx1 != -1 and idx2 != -1 else ""
    news2 = content[idx2:] if idx2 != -1 else ""
    
    def extract_news(text):
        if not text:
            return None
        lines = text.split("\n")
        title = ""
        body_lines = []
        capture = False
        for line in lines:
            if "新闻" in line and "：" in line:
                title = line.split("：")[1].strip() if "：" in line else line
                title = title.split("，")[0].strip()
                capture = True
                continue
            if "**热点事件**" in line:
                continue
            if "**对乐城" in line or "**精算视角**" in line:
                capture = False
                continue
            if capture and line.strip() and not line.startswith("---"):
                clean = line.strip().replace("**", "").replace("#", "").strip()
                if clean and len(clean) > 5:
                    body_lines.append(clean[:80])  # 截断长句
        return {"title": title, "body": body_lines[:4]} if title else None
    
    n1 = extract_news(news1)
    if n1:
        n1["footer"] = "刘一 · 精算师聊健康"
        n1["duration"] = 12
        pages.append(n1)
    
    n2 = extract_news(news2)
    if n2:
        n2["footer"] = "刘一 · 精算师聊健康"
        n2["duration"] = 12
        pages.append(n2)
    
    # 结尾
    pages.append({
        "title": "感谢观看",
        "subtitle": "关注我，获取更多乐城医疗资讯",
        "body": [],
        "footer": "刘一 · 精算师聊健康",
        "duration": 5
    })
    
    return pages

async def gen_audio(text, output_path, voice="zh-CN-YunxiNeural"):
    """生成单段配音"""
    try:
        comm = edge_tts.Communicate(text, voice)
        await comm.save(output_path)
        print(f"  配音OK: {output_path}")
        return True
    except Exception as e:
        print(f"  配音失败: {e}")
        return False

async def generate_all_audio(pages):
    """生成所有配音"""
    audio_files = []
    for i, page in enumerate(pages):
        audio_path = os.path.join(OUTPUT_DIR, f"audio_{i:02d}.wav")
        text_parts = []
        if page.get("title"):
            text_parts.append(page["title"])
        if page.get("subtitle"):
            text_parts.append(page["subtitle"])
        if page.get("body"):
            text_parts.extend(page["body"])
        full_text = "，".join(text_parts) if text_parts else "请观看"
        
        if len(full_text) > 5:
            ok = await gen_audio(full_text, audio_path)
            audio_files.append(audio_path if ok else None)
        else:
            audio_files.append(None)
    return audio_files

def build_video(slide_files, audio_files, pages, output):
    """用FFmpeg拼接"""
    ffmpeg = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
    list_file = os.path.join(OUTPUT_DIR, "concat.txt")
    
    with open(list_file, "w", encoding="utf-8") as f:
        for i, slide in enumerate(slide_files):
            dur = pages[i].get("duration", 8)
            f.write(f"file '{slide}'\n")
            f.write(f"duration {dur}\n")
        # 重复最后一张
        f.write(f"file '{slide_files[-1]}'\n")
    
    cmd = [
        ffmpeg, "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-vf", "scale=1920:1080",
        "-r", "25", "-pix_fmt", "yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        output
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("FFmpeg错误:", result.stderr[-300:])
    else:
        print("[OK] Video:", output)

def main():
    print("=== 乐城早报 v4 ===")
    pages = parse_source()
    print(f"解析到 {len(pages)} 页")
    
    slide_files = []
    for i, page in enumerate(pages):
        img = make_slide(
            title=page.get("title", ""),
            subtitle=page.get("subtitle", ""),
            body=page.get("body", []),
            footer=page.get("footer", "")
        )
        path = os.path.join(OUTPUT_DIR, f"slide_{i:02d}.png")
        img.save(path)
        slide_files.append(path)
        print(f"  幻灯片: {path}")
    
    print("生成配音...")
    audio_files = asyncio.run(generate_all_audio(pages))
    
    output = os.path.join(OUTPUT_DIR, "daily_news_20260511_v4.mp4")
    build_video(slide_files, audio_files, pages, output)

if __name__ == "__main__":
    main()
