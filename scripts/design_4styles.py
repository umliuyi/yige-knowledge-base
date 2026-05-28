#!/usr/bin/env python3
"""4种完全不同的设计方向"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\media"
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080

def F(size):
    for p in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

# =========================
# 风格A: 极简杂志风
# =========================
def style_a():
    img = Image.new("RGB", (W, H), (255,255,255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0,0),(W,6)], fill=(255,87,34))
    draw.text((80, 80), "大健康早报", font=F(80), fill=(30,30,30))
    draw.rectangle([(80,200),(200,206)], fill=(255,87,34))
    draw.text((80, 240), "CAR-T · 基因编辑 · AI医疗", font=F(36), fill=(150,150,160))
    draw.text((80, 350), "2026.05.11", font=F(28), fill=(180,180,190))
    # 右侧大量留白+小圆点
    for i in range(8):
        draw.ellipse([(1500+i*40, 200+i*30),(1520+i*40, 220+i*30)], fill=(255,87,34))
    draw.rectangle([(0,H-6),(W,H)], fill=(255,87,34))
    draw.text((80, H-80), "刘一 | 精算师聊健康", font=F(30), fill=(80,80,90))
    path = os.path.join(OUT, "A_minimal.png")
    img.save(path, quality=95)
    return path

# =========================
# 风格B: 暗色数据仪表盘
# =========================
def style_b():
    img = Image.new("RGB", (W, H), (10,12,20))
    draw = ImageDraw.Draw(img)
    # 顶部
    draw.rectangle([(0,0),(W,80)], fill=(20,25,45))
    draw.rectangle([(0,78),(W,82)], fill=(0,200,220))
    draw.text((60, 24), "大健康早报  DAILY BRIEF", font=F(28), fill=(0,200,220))
    # 左侧大数据
    draw.rectangle([(0,82),(600,H)], fill=(15,20,38))
    f_big = F(180)
    draw.text((40, 200), "480", font=f_big, fill=(255,255,255))
    f_unit = F(60)
    draw.text((40, 400), "万+", font=f_unit, fill=(0,200,220))
    f_desc = F(32)
    draw.text((40, 500), "2023年中国新增癌症患者/年", font=f_desc, fill=(120,140,170))
    # 分隔线
    draw.rectangle([(620,82),(625,H)], fill=(0,200,220))
    # 右侧要点
    draw.text((660, 130), "强化版CAR-T", font=F(52), fill=(255,255,255))
    draw.rectangle([(660,220),(860,224)], fill=(255,87,34))
    y = 270
    for pt in ["• 德国团队新型制剂", "• 11名患者5人完全缓解", "• 副作用更低"]:
        draw.ellipse([(660,y+8),(680,y+26)], fill=(255,87,34))
        draw.text((700, y), pt, font=F(30), fill=(200,210,220))
        y += 65
    # 底部
    draw.rectangle([(0,H-6),(W,H)], fill=(0,200,220))
    draw.text((60, H-80), "刘一 | 精算师聊健康", font=F(30), fill=(100,120,150))
    path = os.path.join(OUT, "B_dashboard.png")
    img.save(path, quality=95)
    return path

# =========================
# 风格C: 新拟态(Neumorphism)
# =========================
def style_c():
    img = Image.new("RGB", (W, H), (220,225,230))
    draw = ImageDraw.Draw(img)
    # 新拟态背景渐变
    for y in range(H):
        r = int(220*(1-y/H) + 235*y/H)
        g = int(225*(1-y/H) + 230*y/H)
        b = int(230*(1-y/H) + 235*y/H)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    # 软阴影卡片
    draw.rounded_rectangle([(60,60),(W-60,H-60)], radius=40, fill=(235,240,245))
    # 顶部标签
    draw.rounded_rectangle([(100,100),(400,160)], radius=20, fill=(255,87,34))
    draw.text((120, 112), "CAR-T · 血液癌", font=F(30), fill=(255,255,255))
    # 主标题
    f_title = F(72)
    draw.text((100, 220), "强化版CAR-T", font=f_title, fill=(40,50,70))
    draw.text((100, 310), "完全缓解率翻倍", font=F(50), fill=(80,90,110))
    # 数据展示
    draw.rounded_rectangle([(100,430),(350,550)], radius=30, fill=(255,255,255))
    draw.rounded_rectangle([(105,435),(345,545)], radius=28, fill=(235,240,245))
    f_num = F(80)
    draw.text((120, 445), "5/11", font=f_num, fill=(255,87,34))
    f_sub = F(22)
    draw.text((120, 525), "完全缓解", font=f_sub, fill=(100,110,130))
    # 右侧要点
    pts = ["干细胞记忆T细胞↑10倍", "副作用显著降低", "无需高强度预处理"]
    y = 440
    for pt in pts:
        draw.rounded_rectangle([(400,y),(850,y+55)], radius=25, fill=(255,255,255))
        draw.rounded_rectangle([(405,y+5),(845,y+50)], radius=23, fill=(235,240,245))
        draw.ellipse([(420, y+18),(440, y+38)], fill=(0,200,220))
        draw.text((460, y+15), pt, font=F(24), fill=(60,70,90))
        y += 70
    # 底部
    draw.text((100, H-120), "刘一 | 精算师聊健康", font=F(28), fill=(100,110,130))
    path = os.path.join(OUT, "C_neumorphic.png")
    img.save(path, quality=95)
    return path

# =========================
# 风格D: 孟菲斯风格
# =========================
def style_d():
    img = Image.new("RGB", (W, H), (255,248,245))
    draw = ImageDraw.Draw(img)
    # 彩色几何图案背景
    colors = [(255,87,34),(0,200,220),(255,200,100),(180,100,200),(100,200,150)]
    for i in range(20):
        x = (i * 200) % (W - 100)
        y = (i * 150) % (H - 100)
        c = colors[i % len(colors)]
        if i % 4 == 0:
            draw.rectangle([(x,y),(x+80,y+80)], outline=c, width=3)
        elif i % 4 == 1:
            draw.ellipse([(x,y),(x+100,y+100)], outline=c, width=3)
        elif i % 4 == 2:
            draw.polygon([(x+50,y),(x+100,y+80),(x,y+80)], outline=c, width=3)
        else:
            draw.rectangle([(x,y),(x+60,y+60)], fill=c)
    # 半透明白色遮罩
    overlay = Image.new("RGB", (W, H), (255,248,245))
    overlay.putalpha(180)
    img.paste(overlay, (0, 0))
    # 内容白卡
    draw.rectangle([(60,60),(W-60,H-60)], fill=(255,255,255))
    draw.rectangle([(60,60),(W-60,66)], fill=(255,87,34))
    draw.text((100, 100), "大健康早报", font=F(70), fill=(40,42,55))
    draw.rectangle([(100,200),(300,206)], fill=(0,200,220))
    draw.text((100, 240), "CAR-T · 基因编辑 · AI医疗 · 患者故事", font=F(30), fill=(120,130,150))
    # 三个彩色信息卡
    cards = [
        ("480万+", "新增癌症患者/年", (255,87,34)),
        ("5/11", "完全缓解", (0,200,220)),
        ("10x", "T细胞提高", (180,100,200)),
    ]
    x = 100
    for num, label, col in cards:
        draw.rectangle([(x,320),(x+220,500)], fill=(255,255,255))
        draw.rectangle([(x,320),(x+8,500)], fill=col)
        f_num = F(60)
        draw.text((x+20, 340), num, font=f_num, fill=(40,42,55))
        f_lb = F(24)
        draw.text((x+20, 440), label, font=f_lb, fill=(120,130,150))
        x += 260
    draw.text((100, H-120), "刘一 | 精算师聊健康", font=F(28), fill=(100,110,130))
    path = os.path.join(OUT, "D_memphis.png")
    img.save(path, quality=95)
    return path

if __name__ == "__main__":
    print("A(极简杂志):", style_a())
    print("B(数据仪表盘):", style_b())
    print("C(新拟态):", style_c())
    print("D(孟菲斯):", style_d())
