#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V7 明亮简洁风 - 白底+品牌蓝+科技感图形"""
from PIL import Image, ImageDraw, ImageFont
import os
import math

W, H = 1080, 1920

# 品牌蓝白配色
COLORS = {
    'primary': (26, 52, 100),     # 深蓝
    'accent': (37, 99, 178),    # 品牌蓝
    'light': (96, 165, 250),  # 亮蓝
    'glow': (191, 219, 255),  # 浅蓝发光
    'dark': (10, 22, 40),    # 深色点缀
    'white': (255, 255, 255),
    'gray': (100, 100, 110),
    'light_bg': (240, 245, 250),  # 浅灰白背景
}

def bright_bg():
    """明亮渐变背景"""
    img = Image.new('RGB', (W, H), (240, 245, 250))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(240 - 20*t)
        g = int(245 - 20*t)
        b = int(250 - 30*t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    return img

def abstract_shape(d, cx, cy, sc=1.0):
    """抽象几何装饰 - 简洁线条圆"""
    # 圆形线条装饰
    r = int(80 * sc)
    # 外圆
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(37, 99, 178), width=2)
    # 内圆
    r2 = int(50 * sc)
    d.ellipse([cx-r2, cy-r2, cx+r2, cy+r2], outline=(96, 165, 250), width=1)
    # 中心点
    d.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(37, 99, 178))
    # 放射线
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        ex = int(cx + r * math.cos(rad))
        ey = int(cy + r * math.sin(rad))
        d.line([cx, cy, ex, ey], fill=(200, 220, 240), width=1)

def molecular_nodes(d, cx, cy, sc=1.0):
    """分子节点装饰 - 简洁点线"""
    # 中心节点
    r = int(12 * sc)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(37, 99, 178))
    # 周围节点
    nodes = [
        (cx, cy - int(100*sc)),
        (cx + int(87*sc), cy - int(50*sc)),
        (cx + int(87*sc), cy + int(50*sc)),
        (cx, cy + int(100*sc)),
        (cx - int(87*sc), cy + int(50*sc)),
        (cx - int(87*sc), cy - int(50*sc)),
    ]
    for nx, ny in nodes:
        nr = int(6 * sc)
        d.ellipse([nx-nr, ny-nr, nx+nr, ny+nr], fill=(96, 165, 250))
        # 连接线
        d.line([cx, cy, nx, ny], fill=(191, 219, 255), width=1)

def txt_font(sz):
    for p in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc"]:
        try:
            return ImageFont.truetype(p, sz)
        except:
            pass
    for p in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttc"]:
        try:
            return ImageFont.truetype(p, sz)
        except:
            pass
    return ImageFont.load_default()

def cntr(draw, s, f, y, c):
    bb = draw.textbbox((0, 0), s, font=f)
    x = (W - (bb[2] - bb[0])) // 2
    draw.text((x, y), s, font=f, fill=c)

def logo_img():
    try:
        l = Image.open(r"C:\Users\Administrator\.openclaw-autoclaw\workspace\logo_main.jpg").convert("RGBA")
        ratio = l.size[1] / l.size[0]
        l = l.resize((80, int(80 * ratio)), Image.LANCZOS)
        return l
    except:
        return None

def make_cover(title, sub, date_str):
    img = bright_bg()
    d = ImageDraw.Draw(img)
    # 顶部蓝色条
    d.rectangle([0, 0, W, 8], fill=(37, 99, 178))
    # 抽象几何装饰 - 左上
    abstract_shape(d, 150, 200, 1.2)
    # 右上装饰
    d.ellipse([W-200, 80, W-80, 200], outline=(37, 99, 178), width=2)
    d.ellipse([W-170, 110, W-110, 170], outline=(96, 165, 250), width=1)
    # 底部装饰
    d.ellipse([50, H-200, 170, H-80], outline=(37, 99, 178), width=2)
    # 日期标签
    d.rectangle([50, 40, 220, 95], fill=(37, 99, 178))
    d.text((70, 55), date_str, font=txt_font(22), fill=(255, 255, 255))
    # 主标题 - 深蓝大字
    tf = txt_font(80)
    if len(title) > 6:
        mid = len(title) // 2
        for i in range(mid, len(title)):
            if title[i] == ' ':
                l1 = title[:i]
                l2 = title[i+1:]
                break
        else:
            l1 = title[:mid]
            l2 = title[mid:]
    else:
        l1 = title
        l2 = ""
    # 深蓝阴影层
    cntr(d, l1, tf, 350, (200, 215, 235))
    if l2:
        cntr(d, l2, tf, 460, (200, 215, 235))
    # 副标题
    if sub:
        cntr(d, sub, txt_font(28), 600, (100, 100, 120))
    # 底部蓝色条
    d.rectangle([0, H-120, W, H-116], fill=(37, 99, 178))
    d.rectangle([0, H-116, W, H], fill=(240, 245, 250))
    lk = logo_img()
    if lk:
        img.paste(lk, (50, H-100), lk)
    d.text((150, H-95), "首位健康", font=txt_font(26), fill=(37, 99, 178))
    d.text((50, H-58), "刘一｜精算师聊健康", font=txt_font(18), fill=(100, 100, 120))
    return img

def make_content(title, body, pg, total):
    img = bright_bg()
    d = ImageDraw.Draw(img)
    # 顶部蓝条
    d.rectangle([0, 0, W, 6], fill=(37, 99, 178))
    # 页码
    d.text((50, 40), f"{pg} / {total}", font=txt_font(24), fill=(37, 99, 178))
    d.rectangle([50, 95, W-50, 99], fill=(200, 220, 240))
    # 分子装饰 - 右上角
    molecular_nodes(d, W-120, 180, 0.8)
    # 标题
    tf = txt_font(52)
    if len(title) > 14:
        mid = len(title) // 2
        for i in range(mid, len(title)):
            if title[i] == ' ':
                l1 = title[:i]
                l2 = title[i+1:]
                break
        else:
            l1 = title[:mid]
            l2 = title[mid:]
    else:
        l1 = title
        l2 = ""
    cntr(d, l1, tf, 200, (26, 52, 100))
    if l2:
        cntr(d, l2, tf, 275, (26, 52, 100))
    # 内容
    cf = txt_font(26)
    words = body
    lines = []
    while len(words) > 22:
        cut = 22
        for j in range(22, len(words)):
            if words[j] == ' ':
                cut = j
                break
        lines.append(words[:cut])
        words = words[cut+1:]
    lines.append(words)
    y = 420
    for line in lines[:5]:
        cntr(d, line, cf, y, (80, 80, 100))
        y += 46
    # 底部
    d.rectangle([0, H-80, W, H-76], fill=(37, 99, 178))
    d.rectangle([0, H-76, W, H], fill=(240, 245, 250))
    d.text((50, H-55), "刘一｜精算师聊健康", font=txt_font(20), fill=(37, 99, 178))
    return img

if __name__ == "__main__":
    out = r"C:\Users\Administrator\.openclaw-autoclaw\media"
    os.makedirs(out, exist_ok=True)
    make_cover("干细胞疗法", "三大新突破 · 2026.05.12", "2026.05.12").save(f"{out}\\v7_cover.png", quality=95)
    print("cover OK")
    make_content("麦吉尔大学：胰岛细胞移植新设备", "绕过传统移植需先建立血供的难题，同时降低免疫排异风险。", 1, 3).save(f"{out}\\v7_c1.png", quality=95)
    print("c1 OK")
    make_content("卡罗林斯卡医学院研究新进展", "在多个干细胞系中稳定产生高质量胰岛素分泌细胞。", 2, 3).save(f"{out}\\v7_c2.png", quality=95)
    print("c2 OK")
    make_content("Sana UP421：14个月持续存活", "I型糖尿病患者接受移植后细胞仍存活，无需免疫抑制剂。", 3, 3).save(f"{out}\\v7_c3.png", quality=95)
    print("c3 OK")
    print("ALL DONE")
