"""
v19 - 舒展排版，留白更多，阅读感受好
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920
TOP_H = int(H * 0.20)  # 384px

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

    # 照片底部加柔和渐变（柔和过渡到白色）
    fade = Image.new('RGBA', (W, 80), (255, 255, 255, 0))
    for y in range(80):
        alpha = int(255 * y / 80)
        for x in range(W):
            fade.putpixel((x, y), (255, 255, 255, alpha))
    photo_rgba = photo.convert('RGBA')
    photo_rgba.paste(fade, (0, TOP_H - 80))
    white = Image.new('RGB', (W, H), (255, 255, 255))
    white.paste(photo_rgba, (0, 0))

    canvas = white
    d = ImageDraw.Draw(canvas)

    # Logo在白色区右上（content_y位置）
    logo_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        lw, lh = logo.size
        max_w = 160
        if lw > max_w:
            ratio = max_w / lw
            logo = logo.resize((max_w, int(lh * ratio)), Image.LANCZOS)
        canvas.paste(logo, (W - max_w - 40, TOP_H + 30), logo)

    # 日期在左上（白色区）
    t(d, (55, TOP_H + 35), "2026.05.14", fnt(20), (160, 160, 165))

    # 主标题（大字，居中，留白）
    y = TOP_H + 90
    title = "药品管理法明日正式施行"
    tbbox = d.textbbox((0, 0), title, font=fnt(76))
    tw = tbbox[2] - tbbox[0]
    t(d, ((W - tw) // 2, y), title, fnt(76), (20, 20, 25))

    # 副标题（居中，分隔清晰）
    sub = "市场独占期落地，进口新药加速进乐城"
    sbbox = d.textbbox((0, 0), sub, font=fnt(30))
    sw = sbbox[2] - sbbox[0]
    t(d, ((W - sw) // 2, y + 105), sub, fnt(30), (110, 110, 115))

    # 分割线（细线）
    ly = y + 175
    d.rectangle([(80, ly), (W - 80, ly + 1)], fill=(210, 210, 215))

    # 精算师视角标签
    t(d, (80, ly + 20), "精算师视角", fnt(24), (220, 75, 35))

    # 四个要点，卡片式布局
    pts = [
        ("15款", "国产1类新药密集获批"),
        ("29个", "乐城新技术已批准落地"),
        ("818号令", "细胞治疗进入监管时代"),
        ("ADC赛道", "中国进入全面爆发期"),
    ]
    y3 = ly + 70
    lh2 = 90  # 每个要点占90px

    for i, (num, desc) in enumerate(pts):
        # 序号点
        dot_x = 80
        t(d, (dot_x, y3), f"0{i+1}", fnt(36), (220, 75, 35))
        # 数字大字
        nbbox = d.textbbox((0, 0), num, font=fnt(40))
        t(d, (130, y3), num, fnt(40), (25, 25, 30))
        # 描述
        t(d, (130 + nbbox[2] - nbbox[0] + 10, y3 + 5), desc, fnt(30), (80, 80, 85))
        y3 += lh2

    # 底部（签名区）
    d.rectangle([(80, H - 175), (W - 80, H - 173)], fill=(210, 210, 215))
    t(d, (80, H - 140), "关注我，用精算师的眼睛看懂大健康", fnt(32), (20, 20, 25))
    t(d, (80, H - 85), "刘一｜精算师聊健康", fnt(20), (130, 130, 135))
    t(d, (80, H - 55), "海南博鳌乐城先行区", fnt(16), (160, 160, 165))

    out = r"C:\Users\Administrator\Downloads\daily_poster_v19.png"
    canvas.save(out, quality=93)
    sz = os.path.getsize(out) // 1024
    print(f"Done: {sz}KB")

make()