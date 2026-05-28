# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r'C:\Users\Administrator\.openclaw-autoclaw\workspace'
W, H = 1080, 1920

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def make_slide_v6(news_title, news_point, news_data, date="2026年5月14日"):
    """高级感幻灯片 - v6规范"""
    img = Image.new('RGB', (W, H), color=hex2rgb('#0a1628'))
    d = ImageDraw.Draw(img)
    
    # 字体
    try:
        ft1 = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 32)
        ft2 = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 28)
        ft3 = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 24)
        ft_small = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 20)
    except:
        ft1 = ft2 = ft3 = ft_small = ImageFont.load_default()
    
    # 顶部装饰线 - 渐变效果用多线条模拟
    for i in range(3):
        alpha = 255 - i * 60
        d.rectangle([(0, 20+i*2), (W, 26+i*2)], fill=(245, 166, 35, alpha))
    
    # 标签
    d.text((60, 80), '政策', fill='#f5a623', font=ft_small)
    d.text((140, 80), '重要', fill='#e74c3c', font=ft_small)
    
    # 主标题 - 大字体，有重量感
    d.text((60, 130), news_title, fill='white', font=ft1)
    
    # 分隔线
    d.rectangle([(60, 200), (W-60, 202)], fill='#333333')
    
    # 重点信息区 - 带背景色块
    d.rectangle([(40, 230), (W-40, 340)], fill='#1a2a4a')
    d.text((60, 250), '重点', fill='#f5a623', font=ft_small)
    d.text((60, 280), news_point, fill='#e0e0e0', font=ft2)
    
    # 数据区 - 金色强调
    d.text((60, 370), '关键数据', fill='#f5a623', font=ft_small)
    d.text((60, 400), news_data, fill='#ffffff', font=ft3)
    
    # 底部日期
    d.text((W//2, H-80), date, fill='#666666', font=ft_small, anchor='mm')
    
    # 右下角装饰
    d.rectangle([(W-100, H-100), (W-60, H-96)], fill='#333333')
    
    return img

if __name__ == '__main__':
    # 测试1: 药品管理法
    img1 = make_slide_v6(
        '药品管理法实施条例明日施行',
        '市场独占期制度落地，跨国药企对乐城关注度上升',
        '创新药独占期最长6年，罕见病/儿童用药同享'
    )
    img1.save(os.path.join(OUTPUT_DIR, 'daily_v6_test1.png'), 'PNG')
    print('Test1 OK')
    
    # 测试2: ADC赛道
    img2 = make_slide_v6(
        'ADC赛道持续升温',
        '国内ADC进入全面爆发期，下一个超级赛道',
        '多款获批临床，晚期实体瘤患者新希望'
    )
    img2.save(os.path.join(OUTPUT_DIR, 'daily_v6_test2.png'), 'PNG')
    print('Test2 OK')
