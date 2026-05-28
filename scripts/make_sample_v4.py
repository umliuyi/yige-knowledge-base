#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""早报幻灯片生成器"""
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"C:\Users\Administrator\.openclaw-autoclaw\workspace"
FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
WIDTH, HEIGHT = 1080, 1920

def hex2rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_slide(title, subtitle=None, date="2026年5月14日", bg_color='#0a1628', accent='#f5a623'):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype(FONT_PATH, 72)
        font_sub = ImageFont.truetype(FONT_PATH, 36)
        font_date = ImageFont.truetype(FONT_PATH, 28)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_date = font_title
    
    # 顶部橙色线
    draw.rectangle([(0, 0), (WIDTH, 6)], fill=accent)
    
    # 主标题
    draw.text((WIDTH//2, HEIGHT//3), title, fill='white', font=font_title, anchor='mm')
    
    # 副标题
    if subtitle:
        draw.text((WIDTH//2, HEIGHT//2 + 60), subtitle, fill='#4a90d9', font=font_sub, anchor='mm')
    
    # 日期
    draw.text((WIDTH//2, HEIGHT - 150), date, fill='#666666', font=font_date, anchor='mm')
    
    # 底部装饰线
    draw.rectangle([(WIDTH//2-80, HEIGHT-80), (WIDTH//2+80, HEIGHT-76)], fill='#333333')
    
    return img

if __name__ == '__main__':
    # 测试封面
    img1 = create_slide("今日早报", "乐城医疗动态 | 权益卡资讯")
    img1.save(os.path.join(OUTPUT_DIR, "daily_cover_v5.png"), 'PNG')
    print("封面OK")
    
    # 测试要点页
    img2 = create_slide(
        "药品管理法实施条例明日施行",
        "市场独占期制度落地，跨国药企对乐城关注度上升",
        bg_color='#1a2a4a', accent='#e74c3c'
    )
    img2.save(os.path.join(OUTPUT_DIR, "daily_p2_v5.png"), 'PNG')
    print("第二页OK")
