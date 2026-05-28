#!/usr/bin/env python3
"""早报视频封面模板 V3 - 首位健康品牌风格"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math

# 竖版尺寸 9:16
WIDTH = 1080
HEIGHT = 1920

# 配色方案（首位健康品牌色）
COLORS = {
    'bg_dark': (10, 22, 40),       # #0A1628 深色背景
    'bg_mid': (26, 52, 70),         # #1A3446 深色调
    'bg_main': (42, 70, 97),         # #2A4661 主色调
    'blue_steel': (82, 106, 143),   # #526A8F 钢蓝
    'blue_light': (163, 177, 200),    # #A3B1C8 浅蓝
    'white': (255, 255, 255),
    'gray_light': (244, 244, 244),  # #F4F4F4
    'gray_blue': (230, 237, 247),    # #E6EDF7
}

def load_logo():
    """加载Logo"""
    logo_path = "C:/Users/Administrator/.openclaw-autoclaw/workspace/logo_main.jpg"
    try:
        logo = Image.open(logo_path).convert('RGBA')
        # 调整Logo大小为宽150px
        w, h = logo.size
        new_w = 150
        new_h = int(h * new_w / w)
        return logo.resize((new_w, new_h), Image.LANCZOS)
    except Exception as e:
        print(f"Logo加载失败: {e}")
        return None

def create_gradient_background(width, height, color1, color2, direction='vertical'):
    """创建渐变背景"""
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    if direction == 'vertical':
        for y in range(height):
            ratio = y / height
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img

def load_font(size, bold=False):
    """加载字体"""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",      # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",   # 黑体
        "C:/Windows/Fonts/simsun.ttc",   # 宋体
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

def add_geometric_decoration(draw, width, height):
    """添加几何装饰元素"""
    # 右上角圆形装饰
    cx, cy = width - 100, 100
    r = 250
    for i in range(20):
        alpha = 150 - i * 7
        color = (42, 70, 97, alpha)
        draw.ellipse([cx-r+i*5, cy-r+i*5, cx+r-i*5, cy+r-i*5], outline=color)
    
    # 左下角圆形装饰
    cx2, cy2 = 100, height - 200
    for i in range(15):
        alpha = 100 - i * 6
        color = (82, 106, 143, alpha)
        draw.ellipse([cx2-r+i*5, cy2-r+i*5, cx2+r-i*5, cy2+r-i*5], outline=color)
    
    # 底部渐变条
    for i in range(50):
        alpha = int(50 + i * 4)
        draw.rectangle([(0, height - 50 + i), (width, height - 50 + i + 1)], 
                       fill=(26, 52, 70))

def create_cover_v3(filename, date_str, news_count=3, title="健康早报", subtitle=""):
    """创建封面"""
    # 渐变背景
    img = create_gradient_background(WIDTH, HEIGHT, 
                                   COLORS['bg_dark'], COLORS['bg_mid'])
    draw = ImageDraw.Draw(img)
    
    # 几何装饰
    add_geometric_decoration(draw, WIDTH, HEIGHT)
    
    # 字体
    font_date = load_font(32)
    font_title = load_font(72, bold=True)
    font_subtitle = load_font(36)
    font_brand = load_font(28)
    font_label = load_font(24)
    
    # 顶部标签区
    # 日期标签背景
    draw.rounded_rectangle([(50, 50), (250, 95)], radius=20, 
                           fill=COLORS['blue_steel'])
    draw.text((75, 60), date_str, font=font_label, fill=COLORS['white'])
    
    # 乐城标签
    draw.rounded_rectangle([(270, 50), (450, 95)], radius=20, 
                           fill=(42, 70, 97))
    draw.text((295, 60), "海南博鳌", font=font_label, fill=COLORS['blue_light'])
    
    # Logo
    logo = load_logo()
    if logo:
        logo_x, logo_y = 50, HEIGHT - 180
        img.paste(logo, (logo_x, logo_y), logo)
    
    # 品牌名
    draw.text((220, HEIGHT - 150), "首位健康", font=font_brand, 
              fill=COLORS['blue_light'])
    draw.text((220, HEIGHT - 115), "HEALTH SCIENCE", font=font_label, 
              fill=COLORS['blue_steel'])
    
    # 中央标题区
    # 标题背景（半透明）
    title_bg_y = 350
    draw.rectangle([(50, title_bg_y), (WIDTH - 50, title_bg_y + 180)], 
                   fill=(0, 0, 0, 50))
    
    # 主标题
    draw.text((80, title_bg_y + 30), title, font=font_title, 
              fill=COLORS['white'])
    
    # 副标题
    if subtitle:
        draw.text((80, title_bg_y + 120), subtitle, font=font_subtitle, 
                  fill=COLORS['blue_light'])
    
    # 期数信息
    period_text = f"第{news_count}条精选"
    draw.text((80, title_bg_y + 200), period_text, font=font_label, 
              fill=COLORS['blue_steel'])
    
    # 底部信息栏
    draw.rectangle([(0, HEIGHT - 100), (WIDTH, HEIGHT)], 
                   fill=(10, 22, 40))
    draw.text((50, HEIGHT - 75), "刘一｜精算师聊健康", font=font_brand, 
              fill=COLORS['white'])
    draw.text((50, HEIGHT - 45), "用精算逻辑管理健康风险", font=font_label, 
              fill=COLORS['blue_steel'])
    
    # 右下角序号
    draw.text((WIDTH - 120, HEIGHT - 80), "01", font=load_font(48), 
              fill=COLORS['blue_steel'])
    
    img.save(filename, quality=95)
    print(f"封面已生成: {filename}")
    return filename

def create_news_page(filename, news_title, news_content, page_num, total):
    """创建内容页"""
    # 渐变背景
    img = create_gradient_background(WIDTH, HEIGHT, 
                                   COLORS['bg_mid'], COLORS['bg_dark'])
    draw = ImageDraw.Draw(img)
    
    # 顶部装饰线
    draw.rectangle([(50, 50), (WIDTH - 50, 55)], fill=COLORS['blue_steel'])
    
    # 页码
    draw.text((50, 80), f"{page_num}/{total}", font=load_font(28), 
              fill=COLORS['blue_steel'])
    
    # 分割线
    draw.rectangle([(50, 140), (WIDTH - 50, 142)], fill=COLORS['blue_steel'])
    
    # 新闻标题
    draw.text((50, 180), news_title, font=load_font(48, bold=True), 
              fill=COLORS['white'])
    
    # 新闻内容（自动换行）
    lines = []
    words = news_content
    max_chars = 20
    while len(words) > max_chars:
        lines.append(words[:max_chars])
        words = words[max_chars:]
    if words:
        lines.append(words)
    
    y = 300
    for line in lines[:8]:  # 最多8行
        draw.text((50, y), line, font=load_font(32), 
                  fill=COLORS['gray_light'])
        y += 55
    
    # 底部
    draw.rectangle([(0, HEIGHT - 100), (WIDTH, HEIGHT)], 
                   fill=(10, 22, 40))
    draw.text((50, HEIGHT - 75), "刘一｜精算师聊健康", font=load_font(28), 
              fill=COLORS['white'])
    draw.text((WIDTH - 150, HEIGHT - 75), f"{page_num}/{total}", 
              font=load_font(28), fill=COLORS['blue_steel'])
    
    img.save(filename, quality=95)
    print(f"内容页已生成: {filename}")
    return filename

# 测试
if __name__ == "__main__":
    output_dir = "C:/Users/Administrator/.openclaw-autoclaw/workspace/covers_v3"
    os.makedirs(output_dir, exist_ok=True)
    
    # 封面
    create_cover_v3(
        os.path.join(output_dir, 'cover_v3_test.png'),
        "2026.05.12",
        news_count=3,
        title="干细胞疗法新突破",
        subtitle="精算师视角·健康日报"
    )
    
    # 内容页示例
    create_news_page(
        os.path.join(output_dir, 'page1_v3_test.png'),
        "麦吉尔大学：可整合血管的胰岛细胞移植新设备",
        "麦吉尔大学团队开发出一种可立即与宿主血管整合的胰岛素分泌细胞移植装置，含预形成人工血管网络，绕过传统移植需先建立血供的难题，同时降低免疫排异风险。",
        page_num=1,
        total=4
    )
    
    print("\n模板测试完成!")
