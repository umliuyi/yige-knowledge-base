"""
v15 - 极简可靠版：照片裁切填满1/5，白色区紧贴照片底部
不用复杂渐变，简单直接
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920
PH = int(H * 0.20)  # 384px

def fnt(size):
    for p in ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def t(draw, xy, text, font, fill):
    draw.text(xy, text, font=font, fill=fill)

def make():
    # 1. 照片：裁切9:16，让宽度填满，高度384px
    photo = Image.open(r"C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\lecheng_official.jpg").convert("RGB")
    pw, ph = photo.size
    # 9:16 = 1080:1920，高度方向1/5对应384px，宽度需1080px
    # 如果照片太宽，切左右；太窄切上下
    target_ratio = W / PH  # 1080/384 = 2.8125
    pr = pw / ph
    if pr > target_ratio:
        # 太宽，切左右
        nw = int(ph * target_ratio)
        photo = photo.crop(((pw - nw) // 2, 0, (pw + nw) // 2, ph))
    else:
        # 太窄，切上下
        nh = int(pw / target_ratio)
        photo = photo.crop((0, (ph - nh) // 2, pw, (ph + nh) // 2))
    photo = photo.resize((W, PH), Image.LANCZOS)

    # 2. 白底
    canvas = Image.new('RGB', (W, H), (255, 255, 255))
    canvas.paste(photo, (0, 0))

    d = ImageDraw.Draw(canvas)

    # 3. 橙色分割线（紧贴1/5边界）
    d.rectangle([(0, PH), (W, PH + 3)], fill=(230, 80, 40))

    # 4. 内容起点（紧贴分割线）
    cy = PH + 60

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

    # 大数字
    y = cy + 90
    nbbox = d.textbbox((0, 0), "480", font=fnt(240))
    nw = nbbox[2] - nbbox[0]
    cx = (W - nw) // 2
    t(d, (cx, y), "480", fnt(240), (25, 25, 28))

    ubbox = d.textbbox((0, 0), "万", font=fnt(80))
    t(d, (cx + nw + 5, y + 55), "万", fnt(80), (80, 80, 85))

    sub = "中国人每年新发癌症"
    sbbox = d.textbbox((0, 0), sub, font=fnt(34))
    sw = sbbox[2] - sbbox[0]
    t(d, ((W - sw) // 2, y + 265), sub, fnt(34), (100, 100, 105))

    # 分割线
    ly = y + 330
    d.rectangle([(80, ly), (W - 80, ly + 1)], fill=(218, 218, 220))

    t(d, (80, ly + 25), "精算师视角", fnt(26), (230, 80, 40))

    pts = [
        ("其中不到30%", "能用上新药"),
        ("原因一：海外新药国内未批",),
        ("原因二：普通家庭无力承担",),
        ("结果：等不起，也用不起",),
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
    t(d, (80, H - 165), "健康的人", fnt(44), (25, 25, 28))
    t(d, (80 + 315, H - 165), "不算账", fnt(44), (230, 80, 40))
    t(d, (80, H - 95), "刘一｜精算师聊健康", fnt(22), (120, 120, 125))
    t(d, (80, H - 62), "海南博鳌乐城先行区", fnt(18), (150, 150, 155))

    out = r"C:\Users\Administrator\Downloads\daily_poster_v15.png"
    canvas.save(out, quality=93)
    print(f"Done: {os.path.getsize(out)//1024}KB")

make()