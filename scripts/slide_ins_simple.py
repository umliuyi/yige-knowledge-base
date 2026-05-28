#!/usr/bin/env python3
"""Ins风幻灯片"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\media"
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080

BG = (250, 248, 245)
CARD = (255, 255, 255)
ORANGE = (255, 107, 82)
TEAL = (82, 194, 194)
GRAY = (120, 120, 130)
DARK = (40, 42, 55)
LGRAY = (235, 235, 240)

def F(size):
    for p in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

def make_cover(title, subtitle, date_str):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # 顶部橙色条
    draw.rectangle([(0, 0), (W, 8)], fill=ORANGE)
    # 左侧白色卡片
    draw.rectangle([(0, 0), (600, H)], fill=CARD)

    # 日期
    draw.text((60, 40), date_str, font=F(24), fill=GRAY)

    # 左侧竖线装饰
    draw.rectangle([(50, 100), (55, 500)], fill=ORANGE)

    # 主标题
    draw.text((70, 120), title, font=F(90), fill=DARK)

    # 副标题
    draw.text((70, 240), subtitle, font=F(36), fill=TEAL)

    # 右侧装饰圆1
    draw.ellipse([(1100, 80), (1400, 380)], outline=ORANGE, width=4)
    # 装饰圆2
    draw.ellipse([(1150, 130), (1350, 330)], outline=TEAL, width=3)
    # 装饰圆3
    draw.ellipse([(1200, 180), (1300, 280)], fill=ORANGE)
    # 小装饰
    draw.ellipse([(1500, 300), (1600, 400)], fill=LGRAY)
    draw.ellipse([(1450, 500), (1550, 600)], fill=TEAL)
    draw.ellipse([(1350, 700), (1450, 800)], fill=ORANGE)
    # 右下角
    draw.ellipse([(W-200, H-250), (W, H-50)], fill=LGRAY)
    draw.ellipse([(W-300, H-150), (W-100, H+50)], fill=ORANGE)

    # 底部白色区
    draw.rectangle([(0, H-120), (W, H)], fill=CARD)
    draw.rectangle([(0, H-124), (W, H-120)], fill=ORANGE)

    # 账号
    draw.text((60, H-90), "刘一 | 精算师聊健康", font=F(32), fill=DARK)

    path = os.path.join(OUT, "design_ins_cover.png")
    img.save(path, quality=95)
    print("Cover:", path)
    return path

def make_news(num, total, tag, title, points):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # 顶部白底
    draw.rectangle([(0, 0), (W, 80)], fill=CARD)
    draw.rectangle([(0, 78), (W, 82)], fill=ORANGE)

    # 大编号背景
    draw.text((30, 5), f"0{num}", font=F(60), fill=LGRAY)

    f_tag = F(24)
    draw.text((180, 24), f"[{num}/{total}]", font=f_tag, fill=ORANGE)
    draw.text((320, 24), tag, font=f_tag, fill=GRAY)

    # 左侧白卡
    draw.rectangle([(0, 82), (920, H)], fill=CARD)

    # 标题
    draw.text((60, 130), title, font=F(56), fill=DARK)
    draw.rectangle([(60, 220), (300, 224)], fill=ORANGE)

    # 要点
    y = 270
    for pt in points:
        pt = pt.strip()
        if not pt:
            continue
        if pt.startswith("•") or pt.startswith("-"):
            draw.ellipse([(60, y+8), (78, y+26)], fill=TEAL)
            draw.text((100, y), pt[1:].strip(), font=F(30), fill=DARK)
        else:
            draw.text((100, y), pt, font=F(30), fill=GRAY)
        y += 68
        if y > H - 180:
            break

    # 右侧大编号
    draw.text((700, H//2 - 150), f"0{num}", font=F(280), fill=LGRAY)

    # 右侧装饰圆
    draw.ellipse([(1100, 150), (1300, 350)], outline=ORANGE, width=4)
    draw.ellipse([(1400, 300), (1600, 500)], outline=TEAL, width=3)
    draw.ellipse([(1500, 600), (1700, 800)], fill=LGRAY)
    draw.ellipse([(1200, 700), (1400, 900)], fill=ORANGE)
    draw.ellipse([(1650, 150), (1750, 250)], fill=TEAL)

    # 底部
    draw.rectangle([(0, H-4), (W, H)], fill=ORANGE)
    draw.rectangle([(0, H-10), (W//4, H-4)], fill=TEAL)

    path = os.path.join(OUT, f"design_ins_news{num}.png")
    img.save(path, quality=95)
    print("News:", path)
    return path

def make_data(big_num, unit, desc, tag):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (W, 80)], fill=CARD)
    draw.rectangle([(0, 78), (W, 82)], fill=TEAL)
    draw.text((60, 24), tag, font=F(26), fill=GRAY)

    # 大数字
    f_num = F(240)
    bbox = draw.textbbox((0, 0), big_num, font=f_num)
    nw = bbox[2] - bbox[0]
    draw.text(((W - nw)//2, 150), big_num, font=f_num, fill=DARK)

    f_unit = F(100)
    draw.text(((W - nw)//2 + nw + 10, 280), unit, font=f_unit, fill=ORANGE)

    f_desc = F(36)
    bbox2 = draw.textbbox((0, 0), desc, font=f_desc)
    dw = bbox2[2] - bbox2[0]
    draw.text(((W - dw)//2, 440), desc, font=f_desc, fill=GRAY)

    draw.rectangle([(W//2 - 60, 510), (W//2 + 60, 514)], fill=TEAL)

    # 四角装饰
    draw.ellipse([(50, 50), (150, 150)], fill=LGRAY)
    draw.ellipse([(W-200, 50), (W-100, 150)], fill=ORANGE)
    draw.ellipse([(50, H-200), (150, H-100)], fill=TEAL)
    draw.ellipse([(W-200, H-200), (W-100, H-100)], fill=LGRAY)

    draw.rectangle([(0, H-6), (W, H)], fill=DARK)

    path = os.path.join(OUT, "design_ins_data.png")
    img.save(path, quality=95)
    print("Data:", path)
    return path

if __name__ == "__main__":
    make_cover("大健康早报", "CAR-T · 基因编辑 · AI医疗 · 患者故事", "2026.05.11")
    make_news(1, 5, "CAR-T · 血液癌",
        "强化版CAR-T：完全缓解率翻倍",
        ["• 德国团队新型制剂，干细胞记忆T细胞提高10倍",
         "• 11名难治性患者：5人完全缓解，1人部分缓解",
         "• 副作用更低，无需高强度预处理"])
    make_data("480", "万+", "2023年中国新增癌症患者/年", "关键数据")
