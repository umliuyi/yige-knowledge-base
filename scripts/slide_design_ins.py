#!/usr/bin/env python3
"""Ins风幻灯片 - 明亮、干净、现代感"""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\media"
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080

# Ins风配色 - 莫兰迪色系+高饱和点缀
BG = (250, 248, 245)       # 米白
CARD = (255, 255, 255)     # 纯白
ORANGE = (255, 107, 82)     # 珊瑚橙（品牌色）
TEAL = (82, 194, 194)       # 青绿
GRAY = (120, 120, 130)      # 中灰
DARK = (40, 42, 55)         # 深蓝灰
LIGHT_GRAY = (235, 235, 240) # 浅灰

def font(size, bold=False):
    for p in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

def draw_gradient_rect(draw, x, y, w, h, c1, c2, horizontal=False):
    """矩形渐变"""
    for i in range(w if horizontal else h):
        r = int(c1[0]*(1-i/(h if not horizontal else w)) + int(c2[0]*i/(h if not horizontal else w))
        g = int(c1[1]*(1-i/(h if not horizontal else w)) + int(c2[1]*i/(h if not horizontal else w))
        b = int(c1[2]*(1-i/(h if not horizontal else w)) + int(c2[2]*i/(h if not horizontal else w))
        if horizontal:
            draw.line([(x+i, y),(x+i, y+h)], fill=(r,g,b))
        else:
            draw.line([(x, y+i),(x+w, y+i)], fill=(r,g,b))

def make_cover_ins(title, subtitle, date_str):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # 顶部装饰条 - 珊瑚橙渐变
    draw.rectangle([(0,0),(W,8)], fill=ORANGE)
    # 左侧大色块
    draw.rectangle([(0,8),(600,H)], fill=CARD)
    draw_gradient_rect(draw, 0, 8, 600, H-8, (255,255,255), (245,248,252))

    # 日期 - 浅灰色
    draw.text((60, 40), date_str, font=font(24), fill=GRAY)

    # 左侧标题区
    draw.rectangle([(50,100),(55,500)], fill=ORANGE)  # 竖线装饰
    f_title = font(90)
    draw.text((70, 120), title, font=f_title, fill=DARK)

    # 副标题
    f_sub = font(38)
    draw.text((70, 240), subtitle, font=f_sub, fill=TEAL)

    # 右侧装饰 - 几何圆形
    draw.ellipse([(1100, 100),(1400, 400)], outline=ORANGE, width=4)
    draw.ellipse([(1150, 150),(1350, 350)], outline=TEAL, width=3)
    draw.ellipse([(1200, 200),(1300, 300)], fill=ORANGE)
    draw.ellipse([(1500, 300),(1600, 400)], fill=LIGHT_GRAY)
    draw.ellipse([(1450, 500),(1550, 600)], fill=TEAL)
    draw.ellipse([(1350, 700),(1450, 800)], fill=ORANGE)
    draw.ellipse([(W-200, H-250),(W, H-50)], fill=LIGHT_GRAY)
    draw.ellipse([(W-300, H-150),(W-100, H+50)], fill=ORANGE)

    # 底部色块
    draw.rectangle([(0,H-120),(W,H)], fill=CARD)
    draw.rectangle([(0,H-124),(W,H-120)], fill=ORANGE)
    # 账号
    draw.text((60, H-90), "刘一 | 精算师聊健康", font=font(32), fill=DARK)
    # 右侧装饰线
    draw.rectangle([(W-200, H-90),(W-195, H-40)], fill=TEAL)

    path = os.path.join(OUT, "design_ins_cover.png")
    img.save(path, quality=95)
    print(f"Ins Cover: {path}")
    return path

def make_news_ins(num, total, tag, title, points):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # 顶部标签栏 - 白底
    draw.rectangle([(0,0),(W,80)], fill=CARD)
    draw.rectangle([(0,78),(W,82)], fill=ORANGE)

    # 编号大标签
    f_num = font(60)
    draw.text((40, 8), f"0{num}", font=f_num, fill=LIGHT_GRAY)

    f_tag = font(24)
    draw.text((180, 24), f"[{num}/{total}]", font=f_tag, fill=ORANGE)
    draw.text((320, 24), tag, font=f_tag, fill=GRAY)

    # 左侧内容区 - 白底卡片
    draw.rectangle([(0,82),(900,H)], fill=CARD)

    # 标题
    f_title = font(56)
    draw.text((60, 130), title, font=f_title, fill=DARK)

    # 分隔线
    draw.rectangle([(60,220),(300,224)], fill=ORANGE)

    # 要点
    f_pt = font(30)
    y = 270
    for pt in points:
        pt = pt.strip()
        if not pt:
            continue
        if pt.startswith("•") or pt.startswith("-"):
            draw.ellipse([(60, y+8),(78, y+26)], fill=TEAL)
            draw.text((100, y), pt[1:].strip(), font=f_pt, fill=DARK)
        else:
            draw.text((100, y), pt, font=f_pt, fill=GRAY)
        y += 68
        if y > H - 180:
            break

    # 右侧大数字背景
    f_bg = font(280)
    draw.text((700, H//2-150), f"0{num}", font=f_bg, fill=LIGHT_GRAY)

    # 右侧装饰
    draw.ellipse([(1100, 150),(1300, 350)], outline=ORANGE, width=4)
    draw.ellipse([(1400, 300),(1600, 500)], outline=TEAL, width=3)
    draw.ellipse([(1500, 600),(1700, 800)], fill=LIGHT_GRAY)
    draw.ellipse([(1200, 700),(1400, 900)], fill=ORANGE)
    # 小装饰
    draw.ellipse([(1650, 150),(1750, 250)], fill=TEAL)

    # 底部
    draw.rectangle([(0,H-4),(W,H)], fill=ORANGE)
    draw.rectangle([(0,H-10),(W//4,H-4)], fill=TEAL)

    path = os.path.join(OUT, f"design_ins_news{num}.png")
    img.save(path, quality=95)
    print(f"Ins News {num}: {path}")
    return path

def make_data_ins(big_num, unit, desc, tag):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0,0),(W,80)], fill=CARD)
    draw.rectangle([(0,78),(W,82)], fill=TEAL)
    draw.text((60, 24), tag, font=font(26), fill=GRAY)

    # 中央数字
    f_num = font(240)
    bbox = draw.textbbox((0,0), big_num, font=f_num)
    nw = bbox[2]-bbox[0]
    draw.text(((W-nw)//2, 150), big_num, font=f_num, fill=DARK)

    f_unit = font(100)
    draw.text(((W-nw)//2 + nw + 10, 280), unit, font=f_unit, fill=ORANGE)

    f_desc = font(36)
    bbox2 = draw.textbbox((0,0), desc, font=f_desc)
    dw = bbox2[2]-bbox2[0]
    draw.text(((W-dw)//2, 440), desc, font=f_desc, fill=GRAY)

    # 装饰线
    draw.rectangle([(W//2-60, 510),(W//2+60, 514)], fill=TEAL)

    # 四角装饰
    draw.ellipse([(50,50),(150,150)], fill=LIGHT_GRAY)
    draw.ellipse([(W-200,50),(W-100,150)], fill=ORANGE)
    draw.ellipse([(50,H-200),(150,H-100)], fill=TEAL)
    draw.ellipse([(W-200,H-200),(W-100,H-100)], fill=LIGHT_GRAY)

    draw.rectangle([(0,H-6),(W,H)], fill=DARK)

    path = os.path.join(OUT, "design_ins_data.png")
    img.save(path, quality=95)
    print(f"Ins Data: {path}")
    return path

if __name__ == "__main__":
    make_cover_ins(
        "大健康早报",
        "CAR-T · 基因编辑 · AI医疗 · 患者故事",
        "2026.05.11"
    )
    make_news_ins(1, 5, "CAR-T · 血液癌",
        "强化版CAR-T：完全缓解率翻倍",
        ["• 德国团队新型制剂，干细胞记忆T细胞提高10倍",
         "• 11名难治性患者：5人完全缓解，1人部分缓解",
         "• 副作用更低，无需高强度预处理"])
    make_data_ins("480", "万+", "2023年中国新增癌症患者/年", "关键数据")
