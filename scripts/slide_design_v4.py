#!/usr/bin/env python3
"""v4设计 - 专业、明亮、数据感"""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\media"
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080

# 配色：专业医疗/金融风格
BG_TOP = (20, 40, 80)     # 深蓝顶
BG_BOT = (10, 20, 50)     # 蓝底（不做黑）
ACCENT = (255, 87, 34)      # 品牌橙
CYAN = (0, 200, 220)        # 青色
WHITE = (255, 255, 255)
GRAY = (180, 190, 210)
DARK_TEXT = (20, 25, 45)
CARD_BG = (30, 50, 90)

def font(size):
    for p in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

def gradient(draw, w, h):
    for y in range(h):
        r = int(BG_TOP[0]*(1-y/h) + BG_BOT[0]*y/h)
        g = int(BG_TOP[1]*(1-y/h) + BG_BOT[1]*y/h)
        b = int(BG_TOP[2]*(1-y/h) + BG_BOT[2]*y/h)
        draw.line([(0,y),(w,y)], fill=(r,g,b))

def make_cover_v4(title, subtitle, date_str):
    img = Image.new("RGB", (W, H), BG_BOT)
    draw = ImageDraw.Draw(img)
    gradient(draw, W, H)

    # 顶部标签条
    draw.rectangle([(0,0),(W,80)], fill=CARD_BG)
    draw.rectangle([(0,78),(W,82)], fill=ACCENT)

    # 日期
    draw.text((60, 28), date_str, font=font(28), fill=GRAY)

    # 右上角装饰 - 渐变圆
    for r in [120, 90, 60]:
        alpha_color = (ACCENT[0], ACCENT[1]//4, ACCENT[2]//4)
        draw.ellipse([(W-r-80, -20), (W+20, r+80)], outline=ACCENT, width=2)
    draw.ellipse([(W-220, 0), (W-80, 140)], fill=(40,60,100))

    # 左下角大标题 - 居中偏上
    # 标题上方装饰线
    draw.rectangle([(60, 200), (300, 205)], fill=ACCENT)
    
    f_title = font(110)
    draw.text((60, 230), title, font=f_title, fill=WHITE)
    
    # 副标题
    f_sub = font(44)
    draw.text((60, 370), subtitle, font=f_sub, fill=CYAN)
    
    # 底部装饰
    draw.rectangle([(0, H-100), (W, H-96)], fill=CARD_BG)
    draw.rectangle([(0, H-4), (W, H)], fill=ACCENT)
    
    # 底部账号
    f_acc = font(36)
    draw.text((60, H-80), "刘一 | 精算师聊健康", font=f_acc, fill=WHITE)

    path = os.path.join(OUT, "design_v4_cover.png")
    img.save(path, quality=95)
    print(f"Cover: {path}")
    return path

def make_news_v4(num, total, tag, title, points):
    img = Image.new("RGB", (W, H), BG_BOT)
    draw = ImageDraw.Draw(img)
    gradient(draw, W, H)

    # 顶部标签
    draw.rectangle([(0,0),(W,80)], fill=CARD_BG)
    draw.rectangle([(0,78),(W,82)], fill=ACCENT)
    
    f_tag = font(24)
    draw.text((60, 28), f"[{num}/{total}]", font=f_tag, fill=ACCENT)
    draw.text((160, 28), tag, font=f_tag, fill=GRAY)

    # 左侧色块装饰
    draw.rectangle([(0, 82), (12, H)], fill=ACCENT)

    # 主标题 - 左对齐，不贴顶
    f_title = font(64)
    draw.text((60, 140), title, font=f_title, fill=WHITE)
    draw.rectangle([(60, 230), (500, 234)], fill=ACCENT)

    # 要点 - 大字间距，清晰可读
    f_pt = font(36)
    y = 280
    for pt in points:
        pt = pt.strip()
        if not pt:
            continue
        if pt.startswith("•") or pt.startswith("-"):
            # 橙色方块
            draw.rectangle([(60, y+8), (76, y+24)], fill=ACCENT)
            draw.text((95, y), pt[1:].strip(), font=f_pt, fill=WHITE)
        else:
            draw.text((95, y), pt, font=f_pt, fill=GRAY)
        y += 70
        if y > H - 160:
            break

    # 右侧大数据展示
    f_big = font(180)
    # 数字阴影
    draw.text((W-480, H//2-80), str(num), font=f_big, fill=(30,50,80))
    draw.text((W-478, H//2-80), str(num), font=f_big, fill=ACCENT)

    f_frac = font(48)
    draw.text((W-480, H//2+100), f"/{total}", font=f_frac, fill=GRAY)

    # 底部
    draw.rectangle([(0, H-4), (W, H)], fill=CARD_BG)
    draw.rectangle([(0, H-8), (W//3, H-4)], fill=CYAN)

    path = os.path.join(OUT, f"design_v4_news{num}.png")
    img.save(path, quality=95)
    print(f"News {num}: {path}")
    return path

def make_data_v4(big_num, unit, desc, tag):
    img = Image.new("RGB", (W, H), BG_BOT)
    draw = ImageDraw.Draw(img)
    gradient(draw, W, H)

    draw.rectangle([(0,0),(W,80)], fill=CARD_BG)
    draw.rectangle([(0,78),(W,82)], fill=CYAN)
    
    f_tag = font(24)
    draw.text((60, 28), tag, font=f_tag, fill=GRAY)

    # 居中大数字
    f_num = font(220)
    num_w = draw.textbbox((0,0), big_num, font=f_num)[2]
    draw.text(((W-num_w)//2, 200), big_num, font=f_num, fill=WHITE)
    
    f_unit = font(80)
    unit_x = (W-num_w)//2 + num_w + 10
    draw.text((unit_x, 340), unit, font=f_unit, fill=ACCENT)

    f_desc = font(36)
    bbox = draw.textbbox((0,0), desc, font=f_desc)
    dw = bbox[2]-bbox[0]
    draw.text(((W-dw)//2, 500), desc, font=f_desc, fill=GRAY)

    # 装饰线
    draw.rectangle([(W//2-100, 600), (W//2+100, 605)], fill=CYAN)

    draw.rectangle([(0, H-4), (W, H)], fill=ACCENT)

    path = os.path.join(OUT, "design_v4_data.png")
    img.save(path, quality=95)
    print(f"Data: {path}")
    return path

if __name__ == "__main__":
    make_cover_v4(
        "大健康早报",
        "CAR-T · 基因编辑 · AI医疗",
        "2026年5月11日 星期日"
    )
    make_news_v4(1, 5, "CAR-T · 血液癌",
        "强化版CAR-T：完全缓解率翻倍",
        ["• 德国团队新型制剂，干细胞记忆T细胞提高10倍",
         "• 11名难治性患者：5人完全缓解，1人部分缓解",
         "• 副作用更低，无需高强度预处理"])
    make_data_v4("480", "万", "2023年中国新增癌症患者/年", "患者故事")
