#!/usr/bin/env python3
"""4种抖音竖屏风格（9:16）"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\media"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920  # 竖屏9:16

def F(size):
    for p in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

ORANGE = (255,107,82)
TEAL = (0,200,220)
GRAY = (120,130,150)
DARK = (25,28,40)
WHITE = (255,255,255)
LGRAY = (240,242,248)
BG = (250,248,245)

# =========================
# A: 极简杂志风（竖屏）
# =========================
def style_a():
    img = Image.new("RGB", (W,H), WHITE)
    draw = ImageDraw.Draw(img)
    # 顶部橙色条
    draw.rectangle([(0,0),(W,6)], fill=ORANGE)
    # 顶部标题
    draw.rectangle([(0,0),(W,120)], fill=(250,252,255))
    draw.text((60,30), "大健康早报", font=F(56), fill=DARK)
    draw.rectangle([(60,110),(280,114)], fill=ORANGE)
    draw.text((60,135), "2026.05.11", font=F(28), fill=GRAY)
    # 装饰右侧
    for i in range(6):
        draw.ellipse([(800+i*30, 200+i*40),(830+i*30, 230+i*40)], fill=ORANGE)
    # 主要内容
    draw.text((60,300), "强化版CAR-T", font=F(72), fill=DARK)
    draw.rectangle([(60,420),(300,424)], fill=TEAL)
    draw.text((60,450), "完全缓解率翻倍", font=F(48), fill=GRAY)
    # 三个数据卡
    cards = [("480万+", "年新增患者"), ("5/11", "完全缓解"), ("10x", "T细胞↑")]
    x = 60
    for num, label in cards:
        draw.rectangle([(x,560),(x+280,700)], fill=(250,252,255))
        draw.rectangle([(x,556),(x+8,700)], fill=ORANGE)
        draw.text((x+20, 570), num, font=F(52), fill=DARK)
        draw.text((x+20, 640), label, font=F(22), fill=GRAY)
        x += 310
    # 底部账号
    draw.rectangle([(0,H-100),(W,H)], fill=DARK)
    draw.text((60, H-70), "刘一 | 精算师聊健康", font=F(32), fill=WHITE)
    draw.rectangle([(0,H-6),(W,H)], fill=ORANGE)
    path = os.path.join(OUT, "VA_minimal.png")
    img.save(path, quality=95)
    return path

# =========================
# B: 暗色数据流（竖屏）
# =========================
def style_b():
    img = Image.new("RGB", (W,H), DARK)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0,0),(W,6)], fill=TEAL)
    draw.rectangle([(0,0),(W,120)], fill=(20,25,45))
    draw.text((60,30), "大健康早报", font=F(52), fill=TEAL)
    draw.text((60,110), "2026.05.11", font=F(24), fill=GRAY)
    # 大数字
    f_big = F(160)
    draw.text((60, 180), "480", font=f_big, fill=WHITE)
    f_unit = F(60)
    draw.text((60, 370), "万+", font=f_unit, fill=ORANGE)
    f_desc = F(32)
    draw.text((60, 450), "2023年中国新增癌症患者/年", font=f_desc, fill=GRAY)
    # 要点
    draw.rectangle([(0,520),(W,524)], fill=(30,40,60))
    y = 570
    for pt in ["德国团队新型制剂", "11名患者5人完全缓解", "副作用显著低于常规CAR-T"]:
        draw.ellipse([(60, y+10),(80, y+30)], fill=ORANGE)
        draw.text((100, y), pt, font=F(32), fill=WHITE)
        y += 80
    # 底部
    draw.rectangle([(0,H-100),(W,H)], fill=(20,25,45))
    draw.rectangle([(0,H-6),(W,H)], fill=TEAL)
    draw.text((60, H-70), "刘一 | 精算师聊健康", font=F(30), fill=GRAY)
    path = os.path.join(OUT, "VB_dark.png")
    img.save(path, quality=95)
    return path

# =========================
# C: 软卡片（竖屏）
# =========================
def style_c():
    img = Image.new("RGB", (W,H), (240,242,248))
    draw = ImageDraw.Draw(img)
    # 顶部
    draw.rectangle([(0,0),(W,6)], fill=ORANGE)
    draw.rectangle([(0,0),(W,130)], fill=WHITE)
    draw.rounded_rectangle([(50,25),(350,105)], radius=20, fill=ORANGE)
    draw.text((70, 40), "CAR-T · 血液癌", font=F(30), fill=WHITE)
    draw.text((60,120), "大健康早报  2026.05.11", font=F(26), fill=GRAY)
    # 主标题
    draw.rounded_rectangle([(50,180),(W-50,340)], radius=30, fill=WHITE)
    draw.text((80, 200), "强化版CAR-T", font=F(60), fill=DARK)
    draw.text((80, 280), "完全缓解率翻倍", font=F(40), fill=ORANGE)
    # 数据卡
    cards = [("480万+", "新增患者/年"), ("5/11", "完全缓解"), ("10x", "T细胞提升")]
    colors = [ORANGE, TEAL, (180,100,200)]
    y = 400
    for (num, lbl), col in zip(cards, colors):
        draw.rounded_rectangle([(50,y),(W-50,y+150)], radius=25, fill=WHITE)
        draw.rounded_rectangle([(50,y),(W-50,y+8)], radius=4, fill=col)
        draw.text((80, y+25), num, font=F(56), fill=DARK)
        draw.text((80, y+100), lbl, font=F(24), fill=GRAY)
        y += 175
    # 底部
    draw.rounded_rectangle([(0,H-100),(W,H)], radius=0, fill=WHITE)
    draw.rectangle([(0,H-6),(W,H)], fill=ORANGE)
    draw.text((60, H-70), "刘一 | 精算师聊健康", font=F(28), fill=GRAY)
    path = os.path.join(OUT, "VC_soft.png")
    img.save(path, quality=95)
    return path

# =========================
# D: 全屏大字（竖屏抖音风）
# =========================
def style_d():
    img = Image.new("RGB", (W,H), DARK)
    draw = ImageDraw.Draw(img)
    # 顶部渐变
    for y in range(400):
        r = int(30*(1-y/400) + 10*y/400)
        g = int(35*(1-y/400) + 15*y/400)
        b = int(60*(1-y/400) + 30*y/400)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    draw.rectangle([(0,0),(W,6)], fill=ORANGE)
    # 标签
    draw.rounded_rectangle([(50,50),(300,100)], radius=15, fill=ORANGE)
    draw.text((70, 60), "CAR-T · 血液癌", font=F(26), fill=WHITE)
    draw.text((50,130), "大健康早报", font=F(42), fill=GRAY)
    draw.text((50,180), "2026.05.11", font=F(26), fill=(80,90,110))
    # 主标题大字
    f_title = F(100)
    draw.text((50, 300), "强化版", font=f_title, fill=WHITE)
    draw.text((50, 420), "CAR-T", font=f_title, fill=ORANGE)
    # 核心数据
    draw.rounded_rectangle([(50,580),(W-50,720)], radius=25, fill=(20,25,45))
    f_num = F(80)
    draw.text((80, 595), "5/11", font=f_num, fill=ORANGE)
    f_sub = F(28)
    draw.text((80, 680), "完全缓解率，远超常规CAR-T", font=f_sub, fill=GRAY)
    # 要点
    y = 800
    for pt in ["干细胞记忆T细胞↑10倍", "副作用显著低于常规疗法", "无需高强度预处理"]:
        draw.ellipse([(50, y+12),(70, y+32)], fill=TEAL)
        draw.text((90, y), pt, font=F(34), fill=WHITE)
        y += 85
    # 底部
    draw.rectangle([(0,H-120),(W,H)], fill=(15,18,30))
    draw.rectangle([(0,H-6),(W,H)], fill=ORANGE)
    draw.text((60, H-90), "刘一 | 精算师聊健康", font=F(30), fill=GRAY)
    path = os.path.join(OUT, "VD_bigtext.png")
    img.save(path, quality=95)
    return path

if __name__ == "__main__":
    print("A(极简):", style_a())
    print("B(暗色流):", style_b())
    print("C(软卡):", style_c())
    print("D(大字):", style_d())
