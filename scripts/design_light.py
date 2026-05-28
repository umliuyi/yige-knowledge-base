#!/usr/bin/env python3
"""最通透的竖屏设计 - 留白即正义"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\media"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920

WHITE = (255,255,255)
OFFWHITE = (252,252,255)
ORANGE = (255,107,82)
TEAL = (0,200,220)
GRAY = (160,165,175)
DARK = (35,38,48)

def F(size):
    for p in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

# =========================
# L1: 封面
# =========================
def l1():
    img = Image.new("RGB", (W,H), WHITE)
    draw = ImageDraw.Draw(img)
    # 顶部一根细线
    draw.rectangle([(80, 80),(W-80, 84)], fill=ORANGE)
    # 日期
    draw.text((80, 120), "2026.05.11", font=F(28), fill=GRAY)
    # 大标题 - 上半屏呼吸
    draw.text((80, 280), "大健康", font=F(96), fill=DARK)
    draw.text((80, 390), "早报", font=F(96), fill=ORANGE)
    # 副标题 - 居中偏下
    draw.text((80, 550), "CAR-T · 基因编辑 · AI医疗 · 患者故事", font=F(32), fill=GRAY)
    # 底部
    draw.rectangle([(80, H-160),(W-80, H-156)], fill=ORANGE)
    draw.text((80, H-120), "刘一 | 精算师聊健康", font=F(36), fill=DARK)
    path = os.path.join(OUT, "L1.png")
    img.save(path, quality=95)
    return path

# =========================
# L2: 标签页
# =========================
def l2():
    img = Image.new("RGB", (W,H), OFFWHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(80, 80),(W-80, 84)], fill=ORANGE)
    # 标签
    draw.rounded_rectangle([(80, 140),(340, 200)], radius=12, fill=DARK)
    draw.text((100, 155), "CAR-T · 血液癌", font=F(28), fill=WHITE)
    # 标题大字
    draw.text((80, 340), "强化版CAR-T", font=F(88), fill=DARK)
    draw.text((80, 450), "完全缓解率翻倍", font=F(64), fill=GRAY)
    # 底部
    draw.rectangle([(80, H-160),(W-80, H-156)], fill=ORANGE)
    draw.text((80, H-120), "刘一 | 精算师聊健康", font=F(36), fill=DARK)
    path = os.path.join(OUT, "L2.png")
    img.save(path, quality=95)
    return path

# =========================
# L3: 大数字冲击页
# =========================
def l3():
    img = Image.new("RGB", (W,H), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(80, 80),(W-80, 84)], fill=ORANGE)
    # 超大数字
    draw.text((80, 200), "480", font=F(220), fill=DARK)
    draw.text((80, 460), "万+", font=F(80), fill=ORANGE)
    draw.rectangle([(80, 560),(280, 566)], fill=GRAY)
    draw.text((80, 600), "2023年中国新增癌症患者/年", font=F(32), fill=GRAY)
    # 底部
    draw.rectangle([(80, H-160),(W-80, H-156)], fill=ORANGE)
    draw.text((80, H-120), "刘一 | 精算师聊健康", font=F(36), fill=DARK)
    path = os.path.join(OUT, "L3.png")
    img.save(path, quality=95)
    return path

# =========================
# L4: 要点页
# =========================
def l4():
    img = Image.new("RGB", (W,H), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(80, 80),(W-80, 84)], fill=ORANGE)
    draw.rounded_rectangle([(80, 140),(300, 200)], radius=12, fill=TEAL)
    draw.text((100, 155), "完全缓解", font=F(28), fill=WHITE)
    # 要点
    y = 300
    for pt in ["德国团队新型制剂", "干细胞记忆T细胞提高10倍", "5/11患者完全缓解", "副作用显著低于常规CAR-T"]:
        draw.text((80, y), pt, font=F(44), fill=DARK)
        y += 90
    draw.rectangle([(80, H-160),(W-80, H-156)], fill=ORANGE)
    draw.text((80, H-120), "刘一 | 精算师聊健康", font=F(36), fill=DARK)
    path = os.path.join(OUT, "L4.png")
    img.save(path, quality=95)
    return path

# =========================
# L5: 结尾关注页
# =========================
def l5():
    img = Image.new("RGB", (W,H), WHITE)
    draw = ImageDraw.Draw(img)
    # 全屏居中大字
    draw.text((80, 400), "关注我", font=F(120), fill=DARK)
    draw.rectangle([(80, 560),(300, 568)], fill=ORANGE)
    draw.text((80, 620), "刘一 | 精算师聊健康", font=F(52), fill=ORANGE)
    draw.text((80, 720), "每天早8:30", font=F(32), fill=GRAY)
    draw.text((80, 780), "大健康资讯早知道", font=F(32), fill=GRAY)
    draw.rectangle([(80, H-160),(W-80, H-156)], fill=ORANGE)
    path = os.path.join(OUT, "L5.png")
    img.save(path, quality=95)
    return path

if __name__ == "__main__":
    print("L1:", l1())
    print("L2:", l2())
    print("L3:", l3())
    print("L4:", l4())
    print("L5:", l5())
