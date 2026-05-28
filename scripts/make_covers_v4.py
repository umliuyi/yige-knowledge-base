#!/usr/bin/env python3
"""
早报视频封面模板 V4 - 设计哲学优化版
约束：避开短视频按钮区域（右侧120px，底部300px）
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 竖版尺寸 9:16
WIDTH = 1080
HEIGHT = 1920

# 安全区域（避开按钮）
RIGHT_SAFE = WIDTH - 150  # 右侧留150px
BOTTOM_SAFE = HEIGHT - 380  # 底部留380px
LEFT_MARGIN = 80
RIGHT_MARGIN = 150

# 配色方案（首位健康品牌色）
COLORS = {
    'bg_dark': (10, 22, 40),
    'bg_mid': (26, 52, 70),
    'white': (255, 255, 255),
    'gray_light': (200, 200, 200),
    'gray': (150, 150, 150),
    'accent': (82, 106, 143),  # 钢蓝
}

def load_font(size, bold=False):
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

def load_logo():
    logo_path = "C:/Users/Administrator/.openclaw-autoclaw/workspace/logo_main.jpg"
    try:
        logo = Image.open(logo_path).convert('RGBA')
        w, h = logo.size
        new_w = 120
        new_h = int(h * new_w / w)
        return logo.resize((new_w, new_h), Image.LANCZOS)
    except:
        return None

def draw_safe_background(img):
    """画背景：上方安全，内容集中在中下"""
    draw = ImageDraw.Draw(img)
    # 渐变效果用色块代替
    draw.rectangle([(0, 0), (WIDTH, HEIGHT)], fill=COLORS['bg_dark'])
    # 中间区域稍微亮一点
    draw.rectangle([(0, 300), (WIDTH, 600)], fill=(15, 28, 50))

def create_cover_v4(filename, date_str, title, subtitle, page_num=1):
    """
    封面设计原则：
    1. 内容放在中间区域（避开右侧按钮）
    2. 底部留白给标题（避开底部标题区）
    3. 文字要少、要大、要居中
    """
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS['bg_dark'])
    draw = ImageDraw.Draw(img)
    
    # ===== 顶部：Logo + 日期（80px高，不超过安全区）=====
    logo = load_logo()
    if logo:
        img.paste(logo, (LEFT_MARGIN, 40), logo)
    
    # 日期标签
    date_text = date_str
    draw.text((WIDTH - 200, 50), date_text, font=load_font(28), fill=COLORS['gray'])
    
    # ===== 中间：核心信息区（300-1200px，最安全区域）=====
    center_y = 450
    
    # 标题：超大字号，居中
    title_font = load_font(80, bold=True)
    # 计算标题位置（居中）
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    title_x = (WIDTH - title_width) // 2
    draw.text((title_x, center_y), title, font=title_font, fill=COLORS['white'])
    
    # 副标题
    sub_font = load_font(36)
    if subtitle:
        bbox2 = draw.textbbox((0, 0), subtitle, font=sub_font)
        sub_width = bbox2[2] - bbox2[0]
        sub_x = (WIDTH - sub_width) // 2
        draw.text((sub_x, center_y + 120), subtitle, font=sub_font, fill=COLORS['gray'])
    
    # ===== 底部：品牌信息（在380px安全线以上）=====
    # 在安全线内（HEIGHT-380以上）
    brand_y = HEIGHT - 450
    
    # 分隔线
    draw.rectangle([(LEFT_MARGIN, brand_y), (WIDTH - RIGHT_MARGIN, brand_y + 2)], 
                   fill=COLORS['accent'])
    
    # 品牌名
    draw.text((LEFT_MARGIN, brand_y + 30), "首位健康", font=load_font(32), 
              fill=COLORS['white'])
    draw.text((LEFT_MARGIN, brand_y + 70), "HEALTH SCIENCE", font=load_font(20), 
              fill=COLORS['accent'])
    
    # 人设
    draw.text((LEFT_MARGIN, brand_y + 120), "刘一｜精算师聊健康", font=load_font(24), 
              fill=COLORS['gray'])
    draw.text((LEFT_MARGIN, brand_y + 155), "用精算逻辑管理健康风险", font=load_font(18), 
              fill=COLORS['gray'])
    
    img.save(filename, quality=95)
    print(f"封面V4已生成: {filename}")
    return filename

def create_page_v4(filename, news_title, news_content, page_num, total):
    """
    内容页设计原则：
    1. 标题区域固定（上方）
    2. 内容区域居中（避开按钮）
    3. 每页只放一条新闻
    4. 文字少、大、清晰
    """
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS['bg_dark'])
    draw = ImageDraw.Draw(img)
    
    # ===== 顶部：页码 + 标题 =====
    # 页码
    page_text = f"{page_num} / {total}"
    draw.text((LEFT_MARGIN, 50), page_text, font=load_font(24), 
              fill=COLORS['accent'])
    
    # 标题区背景
    draw.rectangle([(LEFT_MARGIN, 120), (WIDTH - RIGHT_MARGIN, 130)], 
                   fill=COLORS['accent'])
    
    # ===== 中间：新闻标题（超大，居中）=====
    # 标题：超大字号
    title_font = load_font(52, bold=True)
    # 标题最多2行
    words = news_title
    if len(words) > 20:
        # 找中间空格换行
        mid = len(words) // 2
        for i in range(mid, len(words)):
            if words[i] == ' ':
                line1 = words[:i]
                line2 = words[i+1:]
                break
        else:
            line1 = words[:mid]
            line2 = words[mid:]
    else:
        line1 = words
        line2 = ""
    
    # 居中显示
    bbox = draw.textbbox((0, 0), line1, font=title_font)
    line1_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - line1_width)//2, 250), line1, font=title_font, fill=COLORS['white'])
    
    if line2:
        bbox2 = draw.textbbox((0, 0), line2, font=title_font)
        line2_width = bbox2[2] - bbox2[0]
        draw.text(((WIDTH - line2_width)//2, 330), line2, font=title_font, fill=COLORS['white'])
    
    # ===== 内容区域：简短的关键信息 =====
    content_y = 500
    
    # 内容用较小字号，居中
    content_font = load_font(32)
    
    # 内容分段显示（每行16字）
    max_chars_per_line = 18
    lines = []
    words = news_content
    while len(words) > max_chars_per_line:
        # 找空格截断
        cut = max_chars_per_line
        for i in range(max_chars_per_line, len(words)):
            if words[i] == ' ':
                cut = i
                break
        lines.append(words[:cut])
        words = words[cut+1:]
    lines.append(words)
    
    y = content_y
    for line in lines[:6]:  # 最多6行
        bbox = draw.textbbox((0, 0), line, font=content_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((WIDTH - line_width)//2, y), line, font=content_font, 
                  fill=COLORS['gray_light'])
        y += 55
    
    # ===== 底部：品牌（在安全线以上）=====
    brand_y = HEIGHT - 450
    
    draw.rectangle([(LEFT_MARGIN, brand_y), (WIDTH - RIGHT_MARGIN, brand_y + 2)], 
                   fill=COLORS['accent'])
    
    draw.text((LEFT_MARGIN, brand_y + 30), "刘一｜精算师聊健康", font=load_font(24), 
              fill=COLORS['white'])
    
    img.save(filename, quality=95)
    print(f"内容页V4已生成: {filename}")
    return filename

# 测试
if __name__ == "__main__":
    output_dir = "C:/Users/Administrator/.openclaw-autoclaw/workspace/covers_v4"
    os.makedirs(output_dir, exist_ok=True)
    
    # 封面
    create_cover_v4(
        f"{output_dir}/cover_v4.png",
        "2026.05.12",
        "干细胞疗法新突破",
        "精算师视角 · 每日健康资讯"
    )
    
    # 内容页
    create_page_v4(
        f"{output_dir}/page1_v4.png",
        "麦吉尔大学：可整合血管的胰岛细胞移植新设备",
        "麦吉尔大学团队开发出一种可立即与宿主血管整合的胰岛素分泌细胞移植装置，含预形成人工血管网络，绕过传统移植需先建立血供的难题，同时降低免疫排异风险。",
        1, 3
    )
    
    print("V4模板完成!")
