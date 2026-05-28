#!/usr/bin/env python3
"""
乐城早报 v3 - 重新设计版本
深色背景 + 真实图片 + 男声 + 完整内容
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, subprocess, asyncio, edge_tts
from pathlib import Path

# ============ 配置 ============
SOURCE_FILE = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\日报\2026-05-11-早报-乐城视角.md"
OUTPUT_DIR  = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v3"
AUDIO_DIR   = os.path.join(OUTPUT_DIR, "audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

W, H = 1920, 1080
# 配色：深蓝黑+橙色
BG      = (6, 8, 20)
ORANGE  = (255, 107, 30)
WHITE   = (255, 255, 255)
GRAY    = (140, 145, 160)
CYAN    = (0, 200, 220)

# ============ 字体 ============
def font(size, bold=False):
    for p in [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

def gradient_bg(img):
    """深色渐变背景"""
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(6 * (1-ratio) + 2 * ratio)
        g = int(8 * (1-ratio) + 4 * ratio)
        b = int(20 * (1-ratio) + 12 * ratio)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

def draw_glow_text(draw, xy, text, font_obj, fill=WHITE, glow=ORANGE, glow_r=4):
    """发光字"""
    for dr in range(glow_r, 0, -1):
        alpha = 255 // (dr * 2)
        draw.text(xy, text, font=font_obj, fill=glow)
    draw.text(xy, text, font=font_obj, fill=fill)

def make_page(bg_color=None, top_line=None, title=None, subtitle=None, 
             body_lines=None, footer=None, duration_s=8):
    """生成单页幻灯片"""
    img = Image.new("RGB", (W, H), BG)
    gradient_bg(img)
    draw = ImageDraw.Draw(img)

    # 顶部装饰线
    if top_line:
        draw.rectangle([(0,0),(W,3)], fill=ORANGE)

    # 主标题
    if title:
        draw.text((80, 120), title, font=font(56, True), fill=ORANGE)

    # 副标题/小标题
    if subtitle:
        draw.text((80, 210), subtitle, font=font(28), fill=GRAY)

    # 正文
    if body_lines:
        y = 280
        for line in body_lines:
            draw.text((80, y), line, font=font(26), fill=WHITE)
            y += 50

    # 底部信息
    if footer:
        draw.text((80, H-80), footer, font=font(20), fill=GRAY)

    return img

def parse_source():
    """解析源文件"""
    with open(SOURCE_FILE, encoding="utf-8") as f:
        content = f.read()
    
    pages = []
    
    # 封面
    pages.append({
        "title": "乐城视角 · 大健康早报",
        "subtitle": "2026年5月11日 · 星期日",
        "footer": "刘一 · 精算师聊健康",
        "duration": 5
    })
    
    # 解析新闻段落
    news_sections = content.split("## ")
    for section in news_sections:
        if "新闻一" in section or "新闻二" in section:
            lines = section.split("\n")
            title = ""
            body = []
            for line in lines:
                if line.startswith("**对乐城的影响**"):
                    pass
                elif line.startswith("**精算视角**"):
                    break
                elif line.startswith("**热点事件**"):
                    continue
                elif line.startswith("#"):
                    title = line.replace("🔬", "").replace("💊", "").replace("**", "").strip()
                elif line.strip() and not line.startswith("---"):
                    body.append(line.strip())
            
            if title and body:
                # 截取前3行作为摘要
                pages.append({
                    "title": title,
                    "subtitle": "",
                    "body": body[:3],
                    "footer": "刘一 · 精算师聊健康",
                    "duration": 10
                })
    
    # 结尾
    pages.append({
        "title": "感谢观看",
        "subtitle": "关注我，获取更多乐城医疗资讯",
        "footer": "刘一 · 精算师聊健康",
        "duration": 5
    })
    
    return pages

def generate_slides(pages):
    """生成所有幻灯片"""
    slide_files = []
    for i, page in enumerate(pages):
        img = make_page(
            title=page.get("title", ""),
            subtitle=page.get("subtitle", ""),
            body_lines=page.get("body", []),
            footer=page.get("footer", ""),
        )
        path = os.path.join(OUTPUT_DIR, f"slide_{i:02d}.png")
        img.save(path)
        slide_files.append(path)
        print(f"生成: {path}")
    return slide_files, pages

async def generate_audio(pages):
    """生成配音"""
    audio_files = []
    communicator = edge_tts.Communicate()
    voice = "zh-CN-YunxiNeural"  # 男声
    
    for i, page in enumerate(pages):
        # 构建配音文本
        text_parts = []
        if page.get("title"):
            text_parts.append(page["title"])
        if page.get("subtitle"):
            text_parts.append(page["subtitle"])
        if page.get("body"):
            text_parts.extend(page["body"])
        elif page.get("footer"):
            text_parts.append(page["footer"])
        
        full_text = "，".join(text_parts)
        if not full_text.strip():
            full_text = "请观看"
        
        audio_path = os.path.join(AUDIO_DIR, f"audio_{i:02d}.wav")
        
        try:
            comm = edge_tts.Communicate(full_text, voice)
            await comm.save(audio_path)
            audio_files.append(audio_path)
            print(f"配音: {audio_path}")
        except Exception as e:
            print(f"配音失败 {i}: {e}")
            audio_files.append(None)
    
    return audio_files

def make_video(slide_files, audio_files, pages, output_path):
    """用FFmpeg拼接最终视频"""
    # 生成文件列表
    list_file = os.path.join(OUTPUT_DIR, "concat_list.txt")
    
    with open(list_file, "w", encoding="utf-8") as f:
        for i, (slide, audio) in enumerate(zip(slide_files, audio_files)):
            duration = pages[i].get("duration", 8)
            if audio and os.path.exists(audio):
                # 有配音：用音频长度控制
                f.write(f"file '{slide}'\n")
                f.write(f"duration {duration}\n")
            else:
                # 无配音：用duration控制
                f.write(f"file '{slide}'\n")
                f.write(f"duration {duration}\n")
        # 最后一张重复
        f.write(f"file '{slide_files[-1]}'\n")
    
    # FFmpeg命令
    ffmpeg = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
    
    # 简化方案：用图片+固定时长直接生成
    cmd = [
        ffmpeg,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
        "-r", "25",
        "-pix_fmt", "yuv420p",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        output_path
    ]
    
    print("执行:", " ".join(cmd[:5]) + "...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("FFmpeg错误:", result.stderr[-500:])
    else:
        print(f"视频生成完成: {output_path}")
    
    return output_path

def main():
    print("=== 乐城早报 v3 生成 ===")
    
    # 解析内容
    pages = parse_source()
    print(f"解析到 {len(pages)} 页")
    
    # 生成幻灯片
    slide_files, pages = generate_slides(pages)
    
    # 生成配音
    audio_files = asyncio.run(generate_audio(pages))
    
    # 生成视频
    output = os.path.join(OUTPUT_DIR, "daily_news_20260511_v3.mp4")
    make_video(slide_files, audio_files, pages, output)
    
    print(f"\n✅ 完成: {output}")

if __name__ == "__main__":
    main()
