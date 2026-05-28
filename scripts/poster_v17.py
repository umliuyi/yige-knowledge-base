"""
v17 - 今天早报内容
标题：药品管理法实施条例 明日施行
核心数字：15款国产1类新药获批 / 乐城29个新技术
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920
TOP_H = int(H * 0.20)

def fnt(size):
    for p in ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def t(draw, xy, text, font, fill):
    draw.text(xy, text, font=font, fill=fill)

def make():
    photo = Image.open(r"C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\lecheng_official.jpg").convert("RGB")
    pw, ph = photo.size
    target = W / TOP_H
    pr = pw / ph
    if pr > target:
        nw = int(ph * target)
        photo = photo.crop(((pw - nw) // 2, 0, (pw + nw) // 2, ph))
    else:
        nh = int(pw / target)
        photo = photo.crop((0, (ph - nh) // 2, pw, (ph + nh) // 2))
    photo = photo.resize((W, TOP_H), Image.LANCZOS)

    canvas = Image.new('RGB', (W, H), (255, 255, 255))
    canvas.paste(photo, (0, 0))
    d = ImageDraw.Draw(canvas)

    # 橙色分割线
    d.rectangle([(0, TOP_H), (W, TOP_H + 3)], fill=(230, 80, 40))

    cy = TOP_H + 60

    # Logo
    logo_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        lw, lh = logo.size
        max_w = 180
        if lw > max_w:
            ratio = max_w / lw
            logo = logo.resize((max_w, int(lh * ratio)), Image.LANCZOS)
        canvas.paste(logo, (W - max_w - 55, cy), logo)

    # 日期
    t(d, (55, cy), "2026.05.14", fnt(22), (155, 155, 160))

    # 大标题（不用数字，用关键词）
    y = cy + 85
    t(d, (80, y), "药品管理法", fnt(72), (25, 25, 28))
    t(d, (80, y + 82), "明日正式施行", fnt(72), (230, 80, 40))

    sub = "市场独占期制度落地，进口新药加速进入乐城"
    sbbox = d.textbbox((0, 0), sub, font=fnt(30))
    sw = sbbox[2] - sbbox[0]
    t(d, ((W - sw) // 2, y + 185), sub, fnt(30), (100, 100, 105))

    # 分割线
    ly = y + 250
    d.rectangle([(80, ly), (W - 80, ly + 1)], fill=(218, 218, 220))

    t(d, (80, ly + 25), "精算师视角", fnt(26), (230, 80, 40))

    pts = [
        ("15款国产1类新药", "1-4月密集获批"),
        ("29个乐城生物医学新技术", "已批准，收费体系建立中"),
        ("818号令正式施行", "细胞治疗进入监管时代"),
        ("ADC赛道爆发", "中国进入全面爆发期"),
    ]
    y3 = ly + 65
    for pt in pts:
        if len(pt) == 2:
            t(d, (80, y3), pt[0], fnt(36), (30, 30, 32))
            t(d, (80, y3 + 46), pt[1], fnt(36), (30, 30, 32))
        else:
            t(d, (80, y3), pt[0], fnt(28), (100, 100, 105))
        y3 += 58

    # 底部
    d.rectangle([(80, H - 200), (W - 80, H - 198)], fill=(218, 218, 220))
    t(d, (80, H - 165), "关注我", fnt(44), (25, 25, 28))
    t(d, (80 + 215, H - 165), "用精算师的眼睛", fnt(44), (230, 80, 40))
    t(d, (80, H - 95), "刘一｜精算师聊健康", fnt(22), (120, 120, 125))
    t(d, (80, H - 62), "海南博鳌乐城先行区", fnt(18), (150, 150, 155))

    out = r"C:\Users\Administrator\Downloads\daily_poster_v17.png"
    canvas.save(out, quality=93)
    print(f"Done: {os.path.getsize(out)//1024}KB")

make()