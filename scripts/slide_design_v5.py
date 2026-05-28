#!/usr/bin/env python3
"""v5设计 - 专业媒体风格，层次丰富"""
from PIL import Image, ImageDraw, ImageFont
import os, math, random

OUT = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\media"
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080

# 配色
BG = (12, 18, 38)
CARD1 = (20, 35, 75)
CARD2 = (25, 45, 90)
ACCENT = (255, 87, 34)
CYAN = (0, 200, 220)
TEAL = (0, 180, 160)
WHITE = (255, 255, 255)
GRAY = (160, 170, 200)
LIGHT = (200, 210, 240)

def font(size):
    for p in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

def gradient(draw, w, h, c1, c2, vertical=True):
    for i in range(h if vertical else w):
        r = int(c1[0]*(1-i/h) + c2[0]*i/h)
        g = int(c1[1]*(1-i/h) + c2[1]*i/h)
        b = int(c1[2]*(1-i/h) + c2[2]*i/h)
        if vertical:
            draw.line([(0,i),(w,i)], fill=(r,g,b))
        else:
            draw.line([(i,0),(i,h)], fill=(r,g,b))

def make_cover_v5(title, subtitle, date_str):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient(draw, W, H, (15,25,60), (5,10,30))

    # 左上角大色块
    draw.rectangle([(0,0),(700,H)], fill=CARD1)
    draw.rectangle([(0,0),(700,H)], fill=(0,0,0))
    draw.rectangle([(0,0),(700,H)], fill=CARD1)
    # 透明度叠加
    for y in range(H):
        for x in range(700):
            draw.point((x,y), fill=(20+x//10, 30+y//20, 65+x//15))

    # 顶部横条
    draw.rectangle([(0,0),(W,6)], fill=ACCENT)
    draw.rectangle([(0,6),(W,90)], fill=CARD2)

    # 日期
    draw.text((60, 28), date_str, font=font(26), fill=LIGHT)

    # 右下角装饰圆
    draw.ellipse([(W-350, H-450), (W+50, H-50)], outline=TEAL, width=3)
    draw.ellipse([(W-280, H-380), (W+20, H-80)], outline=ACCENT, width=2)
    draw.ellipse([(W-200, H-300), (W+50, H-50)], outline=CYAN, width=2)

    # 左色块内大标题
    draw.rectangle([(50,0),(55,H)], fill=ACCENT)  # 竖线装饰
    f_title = font(80)
    draw.text((80, 150), title, font=f_title, fill=WHITE)

    # 副标题带色块底
    draw.rectangle([(80, 270),(580, 330)], fill=(ACCENT[0]//3, ACCENT[1]//3, ACCENT[2]//3))
    draw.text((90, 275), subtitle, font=font(34), fill=ACCENT)

    # 右下角主标题
    f_main = font(120)
    bbox = draw.textbbox((0,0), title, font=f_main)
    tw = bbox[2]-bbox[0]
    draw.text(((W+tw)//2 - tw + 80, H//2-50), title, font=f_main, fill=WHITE)

    # 底部
    draw.rectangle([(0,H-80),(W,H)], fill=CARD2)
    draw.rectangle([(0,H-80),(W//3,H)], fill=ACCENT)
    draw.text((60, H-58), "刘一 | 精算师聊健康", font=font(32), fill=WHITE)
    draw.rectangle([(0,H-4),(W,H)], fill=TEAL)

    path = os.path.join(OUT, "design_v5_cover.png")
    img.save(path, quality=95)
    print(f"v5 Cover: {path}")
    return path

def make_news_v5(num, total, tag, title, points):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient(draw, W, H, (12,20,50), (8,12,35))

    # 顶部标签栏
    draw.rectangle([(0,0),(W,80)], fill=CARD2)
    draw.rectangle([(0,78),(W,82)], fill=ACCENT)

    # 编号大标签
    f_num_big = font(72)
    draw.text((40, 5), f"0{num}", font=f_num_big, fill=(30,50,90))

    draw.text((180, 24), f"[{num}/{total}]", font=font(26), fill=ACCENT)
    draw.text((300, 24), tag, font=font(26), fill=LIGHT)

    # 左侧大色块
    draw.rectangle([(0,82),(500,H)], fill=CARD1)
    # 渐变
    for x in range(500):
        r = int(25*(1-x/500) + 20)
        g = int(50*(1-x/500) + 35)
        b = int(90*(1-x/500) + 65)
        draw.line([(x,82),(x,H)], fill=(r,g,b))

    # 标题
    draw.rectangle([(30, 120),(40, 400)], fill=ACCENT)  # 竖线
    f_title = font(58)
    draw.text((60, 120), title, font=f_title, fill=WHITE)

    # 分隔
    draw.rectangle([(60, 220),(460, 224)], fill=ACCENT)

    # 要点
    f_pt = font(30)
    y = 260
    for pt in points:
        pt = pt.strip()
        if not pt:
            continue
        if pt.startswith("•") or pt.startswith("-"):
            draw.rectangle([(60, y+6),(76, y+22)], fill=ACCENT)
            draw.text((95, y), pt[1:].strip(), font=f_pt, fill=WHITE)
        else:
            draw.text((95, y), pt, font=f_pt, fill=GRAY)
        y += 65
        if y > H - 180:
            break

    # 右侧装饰
    draw.ellipse([(W-300, 200),(W-50, 450)], outline=TEAL, width=3)
    draw.ellipse([(W-230, 270),(W-80, 420)], outline=ACCENT, width=2)

    # 大数字背景
    f_bg = font(300)
    draw.text((900, H//2-100), f"0{num}", font=f_bg, fill=(20,35,60))

    # 右侧要点补充
    f_side = font(26)
    draw.text((W-280, 500), "关键数据", font=f_side, fill=CYAN)
    draw.rectangle([(W-280, 535),(W-100, 538)], fill=CYAN)

    # 底部
    draw.rectangle([(0,H-4),(W,H)], fill=ACCENT)
    draw.rectangle([(0,H-10),(W//4,H-4)], fill=CYAN)

    path = os.path.join(OUT, f"design_v5_news{num}.png")
    img.save(path, quality=95)
    print(f"v5 News {num}: {path}")
    return path

def make_data_v5(big_num, unit, desc):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient(draw, W, H, (15,25,65), (5,10,30))

    draw.rectangle([(0,0),(W,80)], fill=CARD2)
    draw.rectangle([(0,78),(W,82)], fill=CYAN)
    draw.text((60, 24), "关键数据", font=font(26), fill=CYAN)

    # 中央大数字
    f_num = font(260)
    bbox = draw.textbbox((0,0), big_num, font=f_num)
    nw = bbox[2]-bbox[0]
    draw.text(((W-nw)//2, 150), big_num, font=f_num, fill=WHITE)

    f_unit = font(100)
    ux = ((W-nw)//2 + nw + 15)
    draw.text((ux, 300), unit, font=f_unit, fill=ACCENT)

    f_desc = font(40)
    bbox2 = draw.textbbox((0,0), desc, font=f_desc)
    dw = bbox2[2]-bbox2[0]
    draw.text(((W-dw)//2, 450), desc, font=f_desc, fill=GRAY)

    # 上下装饰线
    draw.rectangle([(W//2-80, 530),(W//2+80, 535)], fill=ACCENT)

    # 四个角装饰
    corners = [(0,0),(W-80,0),(0,H-80),(W-80,H-80)]
    for cx2, cy2 in corners:
        draw.ellipse([(cx2,cy2),(cx2+80,cy2+80)], outline=TEAL, width=2)

    draw.rectangle([(0,H-6),(W,H)], fill=ACCENT)

    path = os.path.join(OUT, "design_v5_data.png")
    img.save(path, quality=95)
    print(f"v5 Data: {path}")
    return path

if __name__ == "__main__":
    make_cover_v5("大健康早报", "CAR-T · 基因编辑 · AI医疗 · 患者故事", "2026年5月11日 星期日")
    make_news_v5(1, 5, "CAR-T · 血液癌",
        "强化版CAR-T：完全缓解率翻倍",
        ["• 德国团队新型制剂，干细胞记忆T细胞提高10倍",
         "• 11名难治性患者：5人完全缓解，1人部分缓解",
         "• 副作用更低，无需高强度预处理"])
    make_data_v5("480", "万+", "2023年中国新增癌症患者/年")
