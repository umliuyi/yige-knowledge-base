#!/usr/bin/env python3
"""生成完整早报视频幻灯片 - V4模板"""

from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = 1080
HEIGHT = 1920

LEFT_MARGIN = 80
RIGHT_SAFE = WIDTH - 150
BOTTOM_SAFE = HEIGHT - 380

COLORS = {
    'bg_dark': (10, 22, 40),
    'white': (255, 255, 255),
    'gray_light': (200, 200, 200),
    'gray': (150, 150, 150),
    'accent': (82, 106, 143),
}

def load_font(size, bold=False):
    for path in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

def load_logo():
    try:
        logo = Image.open("C:/Users/Administrator/.openclaw-autoclaw/workspace/logo_main.jpg").convert('RGBA')
        w, h = logo.size
        new_h = int(120 * h / w)
        logo = logo.resize((120, new_h), Image.LANCZOS)
        return logo
    except:
        return None

def center_text(draw, text, font, y, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (WIDTH - w) // 2
    draw.text((x, y), text, font=font, fill=color)

def create_slides():
    output_dir = "C:/Users/Administrator/.openclaw-autoclaw/workspace/covers_v4"
    os.makedirs(output_dir, exist_ok=True)
    
    news = [
        {
            "title": "麦吉尔大学：可整合血管的胰岛细胞移植新设备",
            "content": "麦吉尔大学团队开发出一种可立即与宿主血管整合的胰岛素分泌细胞移植装置，绕过传统移植需先建立血供的难题，同时降低免疫排异风险。"
        },
        {
            "title": "瑞典卡罗林斯卡医学院：干细胞培育胰岛素细胞新进展",
            "content": "研究团队在多个干细胞系中稳定产生高质量胰岛素分泌细胞，移植后逆转糖尿病并维持血糖调控数月，为临床转化提供支撑。"
        },
        {
            "title": "Sana Biotechnology UP421：基因编辑β细胞疗法14个月持续存活",
            "content": "Ⅰ型糖尿病患者接受UP421移植后14个月，细胞仍存活并持续产生胰岛素，全程无需免疫抑制剂。这一结果证明无排异β细胞疗法路径可行。"
        }
    ]
    
    slides = []
    
    # ===== 封面 =====
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS['bg_dark'])
    draw = ImageDraw.Draw(img)
    
    logo = load_logo()
    if logo:
        img.paste(logo, (LEFT_MARGIN, 40), logo)
    
    draw.text((WIDTH - 200, 50), "2026.05.12", font=load_font(28), fill=COLORS['gray'])
    
    title_font = load_font(72, bold=True)
    center_text(draw, "干细胞疗法", title_font, 450, COLORS['white'])
    center_text(draw, "三大新突破", title_font, 550, COLORS['white'])
    
    sub_font = load_font(36)
    center_text(draw, "精算师视角 每日健康资讯", sub_font, 700, COLORS['gray'])
    
    draw.rectangle([(LEFT_MARGIN, 1400), (WIDTH - RIGHT_SAFE, 1405)], fill=COLORS['accent'])
    draw.text((LEFT_MARGIN, 1430), "首位健康", font=load_font(32), fill=COLORS['white'])
    draw.text((LEFT_MARGIN, 1470), "刘一｜精算师聊健康", font=load_font(24), fill=COLORS['gray'])
    
    slide_path = output_dir + "/slide_00_cover.png"
    img.save(slide_path, quality=95)
    slides.append(slide_path)
    print("封面已生成")
    
    # ===== 内容页 =====
    for i, n in enumerate(news):
        img = Image.new('RGB', (WIDTH, HEIGHT), COLORS['bg_dark'])
        draw = ImageDraw.Draw(img)
        
        draw.text((LEFT_MARGIN, 50), f"{i+1} / {len(news)}", font=load_font(24), fill=COLORS['accent'])
        draw.rectangle([(LEFT_MARGIN, 120), (WIDTH - RIGHT_SAFE, 125)], fill=COLORS['accent'])
        
        title_font = load_font(48, bold=True)
        words = n["title"]
        if len(words) > 16:
            mid = len(words) // 2
            for j in range(mid, len(words)):
                if words[j] == ' ':
                    line1 = words[:j]
                    line2 = words[j+1:]
                    break
            else:
                line1 = words[:mid]
                line2 = words[mid:]
        else:
            line1 = words
            line2 = ""
        
        center_text(draw, line1, title_font, 250, COLORS['white'])
        if line2:
            center_text(draw, line2, title_font, 330, COLORS['white'])
        
        content_font = load_font(28)
        content = n["content"]
        lines = []
        max_chars = 16
        while len(content) > max_chars:
            for j in range(max_chars, len(content)):
                if content[j] == ' ':
                    lines.append(content[:j])
                    content = content[j+1:]
                    break
            else:
                lines.append(content[:max_chars])
                content = content[max_chars:]
        lines.append(content)
        
        y = 500
        for line in lines[:6]:
            center_text(draw, line, content_font, y, COLORS['gray_light'])
            y += 50
        
        draw.rectangle([(LEFT_MARGIN, 1400), (WIDTH - RIGHT_SAFE, 1405)], fill=COLORS['accent'])
        draw.text((LEFT_MARGIN, 1430), "刘一｜精算师聊健康", font=load_font(24), fill=COLORS['white'])
        
        slide_path = output_dir + f"/slide_{i+1:02d}_content.png"
        img.save(slide_path, quality=95)
        slides.append(slide_path)
        print(f"内容页{i+1}已生成")
    
    # ===== 结尾页 =====
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS['bg_dark'])
    draw = ImageDraw.Draw(img)
    
    title_font = load_font(64, bold=True)
    center_text(draw, "关注我", title_font, 600, COLORS['white'])
    center_text(draw, "用精算逻辑管理健康风险", load_font(36), 720, COLORS['gray'])
    
    draw.rectangle([(LEFT_MARGIN, 1300), (WIDTH - RIGHT_SAFE, 1305)], fill=COLORS['accent'])
    draw.text((LEFT_MARGIN, 1330), "首位健康", font=load_font(32), fill=COLORS['white'])
    draw.text((LEFT_MARGIN, 1370), "HEALTH SCIENCE", font=load_font(20), fill=COLORS['accent'])
    draw.text((LEFT_MARGIN, 1420), "刘一｜精算师聊健康", font=load_font(24), fill=COLORS['gray'])
    
    slide_path = output_dir + "/slide_99_end.png"
    img.save(slide_path, quality=95)
    slides.append(slide_path)
    print("结尾页已生成")
    
    return slides

if __name__ == "__main__":
    slides = create_slides()
    print(f"\n共 {len(slides)} 张幻灯片")
