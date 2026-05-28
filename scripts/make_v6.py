#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V6: 高级感设计 - 玻璃态+发光细胞+多层渐变"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random
import math
import os

W, H = 1080, 1920

def hsl_to_rgb(h, s, l):
    """HSL转RGB"""
    h /= 360
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs(h*6 % 2 - 1))
    m = l - c/2
    if h < 1/6: r,g,b = c,x,0
    elif h < 2/6: r,g,b = x,c,0
    elif h < 3/6: r,g,b = 0,c,x
    elif h < 4/6: r,g,b = 0,x,c
    elif h < 5/6: r,g,b = x,0,c
    else: r,g,b = c,0,x
    return (int((r+m)*255), int((g+m)*255), int((b+m)*255)

def deep_bg():
    """深邃星空背景"""
    # 多层渐变 - 蓝紫到深蓝
    img = Image.new('RGB', (W, H), (5, 8, 20))
    draw = ImageDraw.Draw(img)
    # 底层渐变 - 多种颜色混合
    for y in range(H):
        t = y / H
        # 三段渐变
        if t < 0.4:
            s = t / 0.4
            r = int(5 + (20-5)*s)
            g = int(8 + (15-8)*s)
            b = int(20 + (60-20)*s)
        elif t < 0.7:
            s = (t-0.4)/0.3
            r = int(20 + (15-20)*s)
            g = int(15 + (25-15)*s)
            b = int(60 + (100-60)*s)
        else:
            s = (t-0.7)/0.3
            r = int(15 + (8-15)*s)
            g = int(25 + (15-25)*s)
            b = int(100 + (30-100)*s)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    # 噪点纹理
    for _ in range(3000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(2, 5)
        alpha = random.randint(10, 30)
        draw.ellipse([x,y,x+s,y+s], fill=(100,150,255,alpha))
    return img

def orb(img, cx, cy, r, col, glow_r=80):
    """发光球体 - 核心+光晕+反射"""
    draw = ImageDraw.Draw(img)
    # 外层大光晕
    for i in range(glow_r, r, -2):
        ratio = (glow_r - i) / glow_r
        alpha = int(40 * ratio)
        rr = int(col[0] * (0.3 + 0.7*ratio))
        gg = int(col[1] * (0.3 + 0.7*ratio))
        bb = int(col[2] * (0.3 + 0.7*ratio))
        draw.ellipse([cx-i,cy-i,cx+i,cy+i], fill=(rr,gg,bb))
    # 主体
    for i in range(r, 0, -1):
        ratio = i/r
        rr = int(col[0] * ratio)
        gg = int(col[1] * ratio)
        bb = int(col[2] * ratio)
        draw.ellipse([cx-i,cy-i,cx+i,cy+i], fill=(rr,gg,bb))
    # 高光点
    hi_r = r//3
    hi_x = cx - r//4
    hi_y = cy - r//4
    draw.ellipse([hi_x-hi_r,hi_y-hi_r,hi_x+hi_r,hi_y+hi_r], fill=(200,220,255))
    draw.ellipse([hi_x-hi_r//2,hi_y-hi_r//2,hi_x+hi_r//2,hi_y+hi_r//2], fill=(240,250,255))

def glass_card(img, x, y, w, h, col=(30,40,80), alpha=60):
    """玻璃态卡片"""
    overlay = Image.new('RGBA', (w, h), (*col, alpha))
    # 模糊背景（简化为色块叠加）
    draw = ImageDraw.Draw(overlay)
    # 边框
    draw.rectangle([0,0,w-1,h-1], outline=(100,140,200,100), width=1)
    img.paste(overlay, (x,y), overlay)

def line_connector(draw, x1, y1, x2, y2):
    """发光连接线"""
    steps = int(math.sqrt((x2-x1)**2+(y2-y1)**2)//3)
    for i in range(steps):
        t = i/steps
        x = int(x1*(1-t) + x2*t) + random.randint(-1,1)
        y = int(y1*(1-t) + y2*t) + random.randint(-1,1)
        s = random.randint(1,2)
        draw.ellipse([x-s, y-s, x+s, y+s], fill=(80, 120, 200, 80))

def txt_font(sz):
    for p in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttc"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

def cntr(draw, s, f, y, c):
    bb = draw.textbbox((0,0), s, font=f)
    x = (W-(bb[2]-bb[0]))//2
    draw.text((x,y), s, font=f, fill=c)

def lg():
    try:
        l = Image.open(r"C:\Users\Administrator\.openclaw-autoclaw\workspace\logo_main.jpg").convert("RGBA")
        ratio = l.size[1]/l.size[0]
        l = l.resize((90, int(90*ratio)), Image.LANCZOS)
        return l
    except: return None

def make_cover_v6(title, sub, date_str):
    img = deep_bg()
    d = ImageDraw.Draw(img)
    
    # 中心大发光球 - 细胞感
    orb(img, W//2, H//2-100, 180, (40, 80, 200), glow_r=200)
    orb(img, W//2+250, H//2+200, 120, (60, 120, 220), glow_r=150)
    orb(img, 150, H//2+100, 80, (30, 100, 180), glow_r=100)
    orb(img, W-200, 300, 100, (50, 100, 200), glow_r=120)
    orb(img, W//2-300, H//2+300, 60, (80, 140, 220), glow_r=80)
    
    # 连接线 - 细胞网络感
    for _ in range(8):
        x1 = random.randint(W//4, W*3//4)
        y1 = random.randint(H//4, H*3//4)
        x2 = random.randint(W//4, W*3//4)
        y2 = random.randint(H//4, H*3//4)
        line_connector(d, x1,y1, x2,y2)
    
    # 顶部日期标签 - 玻璃态
    glass_card(img, 50, 50, 180, 50, (20, 40, 100), 80)
    d.text((65, 60), date_str, font=txt_font(22), fill=(150, 180, 220))
    
    # 主标题 - 发光效果（用多层文字叠加模拟）
    tf = txt_font(90)
    # 阴影层
    for ox in [-2,0,2]:
        for oy in [-2,0,2]:
            cntr(d, title[:len(title)//2], tf, 420+oy, (5,10,30))
    cntr(d, title[:len(title)//2], tf, 420, (255,255,255))
    
    if len(title) > 4:
        for ox in [-1,0,1]:
            for oy in [-1,0,1]:
                cntr(d, title[len(title)//2:], tf, 540+oy, (5,10,30))
        cntr(d, title[len(title)//2:], tf, 540, (255,255,255))
    
    # 副标题
    if sub:
        sf = txt_font(32)
        cntr(d, sub, sf, 680, (140,170,210))
    
    # 底部玻璃态信息栏
    glass_card(img, 0, H-150, W, 150, (10,20,50), 100)
    lk = lg()
    if lk:
        img.paste(lk, (50, H-120), lk)
    d.text((160, H-105), "首位健康", font=txt_font(28), fill=(255,255,255))
    d.text((160, H-72), "HEALTH SCIENCE", font=txt_font(16), fill=(80,120,180))
    d.text((50, H-55), "刘一｜精算师聊健康", font=txt_font(20), fill=(120,150,190))
    
    return img

def make_content_v6(title, body, pg, total):
    img = deep_bg()
    d = ImageDraw.Draw(img)
    
    # 小型发光球装饰
    orb(img, W-100, 100, 60, (40, 80, 200), glow_r=80)
    orb(img, 80, H-100, 50, (60, 120, 220), glow_r=70)
    orb(img, W//2, 80, 40, (80, 140, 220), glow_r=60)
    
    # 页码
    d.text((50, 50), f"{pg} / {total}", font=txt_font(24), fill=(80, 130, 220))
    d.rectangle([50,108,W-50,112], fill=(60,100,180))
    
    # 标题
    tf = txt_font(56)
    if len(title) > 14:
        mid = len(title)//2
        for i in range(mid, len(title)):
            if title[i] == ' ':
                t1, t2 = title[:i], title[i+1:]
                break
        else:
            t1, t2 = title[:mid], title[mid:]
    else:
        t1, t2 = title, ""
    for ox,oy in [(-2,-2),(-2,2),(2,-2),(2,2),(0,0)]:
        cntr(d, t1, tf, 240+oy, (5,10,30) if ox!=0 or oy!=0 else (255,255,255))
    if t2:
        for ox,oy in [(-1,-1),(-1,1),(1,-1),(1,1),(0,0)]:
            cntr(d, t2, tf, 340+oy, (5,10,30) if ox!=0 or oy!=0 else (255,255,255))
    
    # 内容
    cf = txt_font(28)
    words = body
    lines = []
    while len(words) > 20:
        cut = 20
        for j in range(20, len(words)):
            if words[j] == ' ':
                cut = j; break
        lines.append(words[:cut]); words = words[cut+1:]
    lines.append(words)
    y = 500
    for line in lines[:5]:
        cntr(d, line, cf, y, (160,180,210))
        y += 50
    
    # 底部栏
    glass_card(img, 0, H-100, W, 100, (10,20,50), 80)
    d.text((50, H-65), "刘一｜精算师聊健康", font=txt_font(24), fill=(255,255,255))
    return img

if __name__ == "__main__":
    out = r"C:\Users\Administrator\.openclaw-autoclaw\media"
    os.makedirs(out, exist_ok=True)
    make_cover_v6("干细胞疗法", "三大新突破 · 2026.05.12", "2026.05.12").save(f"{out}\\v6_cover.png", quality=95)
    print("cover OK")
    make_content_v6("麦吉尔大学：胰岛细胞移植新设备", "绕过传统移植需先建立血供的难题，同时降低免疫排异风险。", 1,3).save(f"{out}\\v6_c1.png", quality=95)
    print("c1 OK")
    make_content_v6("卡罗林斯卡医学院研究新进展", "在多个干细胞系中稳定产生高质量胰岛素分泌细胞。", 2,3).save(f"{out}\\v6_c2.png", quality=95)
    print("c2 OK")
    make_content_v6("Sana UP421：14个月持续存活", "I型糖尿病患者接受移植后细胞仍存活，无需免疫抑制剂。", 3,3).save(f"{out}\\v6_c3.png", quality=95)
    print("c3 OK")
    print("ALL DONE")
