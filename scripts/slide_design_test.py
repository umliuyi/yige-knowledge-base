#!/usr/bin/env python3
"""升级版幻灯片 v3 - 纯PIL几何装饰"""
from PIL import Image, ImageDraw, ImageFont
import os, re, math

OUT = r"C:\Users\Administrator\Downloads\videos\slides_design"
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080

BG = (8, 8, 18)
ORANGE = (255, 87, 34)
CYAN = (0, 188, 212)
WHITE = (255, 255, 255)
GRAY = (140, 140, 155)
DARK = (15, 15, 30)

def font(size):
    for p in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

def gradient(draw, w, h):
    for y in range(h):
        r = int(8*(1-y/h) + 4*y/h)
        g = int(8*(1-y/h) + 4*y/h)
        b = int(18*(1-y/h) + 12*y/h)
        draw.line([(0,y),(w,y)], fill=(r,g,b))

def hex_polygon(draw, cx, cy, r, color, width=2):
    pts = [(cx + int(r*math.cos(math.pi*2*i/6)),
            cy + int(r*math.sin(math.pi*2*i/6))) for i in range(6)]
    draw.polygon(pts, outline=color, width=width)

def circle_pattern(draw, cx, cy, r, color):
    for i in range(3):
        ri = r * (1 - i*0.28)
        draw.ellipse([(cx-ri, cy-ri), (cx+ri, cy+ri)], outline=color, width=1)

def make_cover_v3(title, subtitle, date_str):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient(draw, W, H)

    draw.rectangle([(0,0),(W,8)], fill=ORANGE)
    draw.text((60, 45), date_str, font=font(28), fill=GRAY)

    # 右下角同心圆装饰
    circle_pattern(draw, 1550, 800, 180, ORANGE)
    circle_pattern(draw, 1550, 800, 120, CYAN)
    circle_pattern(draw, 1550, 800, 60, ORANGE)

    # 左上角大标题装饰字
    f_huge = font(280)
    draw.text((30, H//2-130), "早", font=f_huge, fill=(14,14,26))

    f_title = font(96)
    bbox = draw.textbbox((0,0), title, font=f_title)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H//2-130), title, font=f_title, fill=WHITE)

    f_sub = font(40)
    bbox2 = draw.textbbox((0,0), subtitle, font=f_sub)
    sw = bbox2[2]-bbox2[0]
    draw.text(((W-sw)//2, H//2+10), subtitle, font=f_sub, fill=GRAY)

    f_acc = font(36)
    acc = "刘一 | 精算师聊健康"
    abbox = draw.textbbox((0,0), acc, font=f_acc)
    aw = abbox[2]-abbox[0]
    draw.text(((W-aw)//2, H-130), acc, font=f_acc, fill=ORANGE)
    draw.rectangle([(0,H-5),(W,H)], fill=CYAN)

    path = os.path.join(OUT, "v3_cover.png")
    img.save(path, quality=95)
    print(f"Cover: {path}")
    return path

def make_news_v3(num, total, tag, title, points, accent_color=None):
    accent = accent_color or ORANGE
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient(draw, W, H)

    draw.rectangle([(0,0),(W,6)], fill=accent)
    draw.rectangle([(0,6),(W,70)], fill=DARK)

    f_tag = font(24)
    draw.text((50, 22), f"[{num}/{total}]", font=f_tag, fill=accent)
    draw.text((150, 22), tag, font=f_tag, fill=WHITE)

    f_title = font(56)
    draw.text((50, 100), title, font=f_title, fill=WHITE)
    draw.rectangle([(50,190),(W-50,194)], fill=accent)

    # 左侧大号半透明数字
    f_big = font(220)
    draw.text((20, H//2-90), str(num), font=f_big, fill=(18,18,28))

    f_pt = font(32)
    y = 220
    for pt in points:
        pt = pt.strip()
        if not pt:
            continue
        if pt.startswith("•") or pt.startswith("-"):
            draw.ellipse([(55, y+9),(72, y+26)], fill=accent)
            draw.text((90, y), pt[1:].strip(), font=f_pt, fill=WHITE)
        else:
            draw.text((90, y), pt, font=f_pt, fill=GRAY)
        y += 68
        if y > H - 130:
            break

    # 右侧六边形装饰
    hex_positions = [(1560,260),(1700,420),(1520,580),(1660,720),(1780,320)]
    for hx, hy in hex_positions:
        hex_polygon(draw, hx, hy, 50, accent, width=2)
        draw.ellipse([(hx-4,hy-4),(hx+4,hy+4)], fill=accent)

    draw.rectangle([(0,H-5),(W,H)], fill=CYAN)
    draw.text((W-120, H-70), f"{num}/{total}", font=font(22), fill=GRAY)

    slug = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "", title)[:4]
    path = os.path.join(OUT, f"v3_{num}_{slug}.png")
    img.save(path, quality=95)
    print(f"News {num}: {path}")
    return path

def make_data_slide_v3(num, total, big_num, big_unit, sub_text, tag):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient(draw, W, H)

    draw.rectangle([(0,0),(W,6)], fill=ORANGE)
    draw.rectangle([(0,6),(W,70)], fill=DARK)
    f_tag = font(24)
    draw.text((50, 22), f"[{num}/{total}]", font=f_tag, fill=ORANGE)
    draw.text((150, 22), tag, font=f_tag, fill=WHITE)

    # 大数字
    f_num = font(200)
    draw.text((W//2 - 350, H//2-180), big_num, font=f_num, fill=ORANGE)
    f_unit = font(52)
    draw.text((W//2 + 280, H//2-60), big_unit, font=f_unit, fill=WHITE)

    # 说明
    f_sub = font(36)
    bbox = draw.textbbox((0,0), sub_text, font=f_sub)
    sw = bbox[2]-bbox[0]
    draw.text(((W-sw)//2, H//2+60), sub_text, font=f_sub, fill=GRAY)

    # 周围六边形装饰
    hex_positions = [(400,300),(600,700),(1300,250),(1500,600),(1700,850)]
    for hx, hy in hex_positions:
        hex_polygon(draw, hx, hy, 40, CYAN, width=1)
        draw.ellipse([(hx-3,hy-3),(hx+3,hy+3)], fill=CYAN)

    draw.rectangle([(0,H-5),(W,H)], fill=ORANGE)
    draw.text((W-120, H-70), f"{num}/{total}", font=font(22), fill=GRAY)

    path = os.path.join(OUT, f"v3_{num}_data.png")
    img.save(path, quality=95)
    print(f"Data {num}: {path}")
    return path

if __name__ == "__main__":
    print("Generating v3 slides...")
    make_cover_v3("大健康早报", "CAR-T · 基因编辑 · AI医疗", "2026年5月11日")
    make_news_v3(1, 5, "CAR-T · 血液癌", "强化版CAR-T：完全缓解率翻倍",
        ["• 德国团队新型制剂，干细胞记忆T细胞提高10倍",
         "• 11名难治性患者：5人完全缓解，1人部分缓解",
         "• 副作用更低，无需高强度预处理"], ORANGE)
    make_news_v3(2, 5, "基因技术", "基因碎纸机Cas12a2精准灭杀癌细胞",
        ["• 犹他大学《自然》发表：识别RNA后触发细胞自毁",
         "• KRAS肺癌：疗效媲美顺铂，健康细胞零损伤",
         "• HPV小鼠：清除90%以上感染细胞"], CYAN)
    make_data_slide_v3(3, 5, "480", "万", "2023年中国新增癌症患者/年", "患者故事")
    print("Done!")
