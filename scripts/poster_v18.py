"""
v18 - 内容压缩单行，省空间不重叠
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

    canvas = Image.new('RGB', (W, H), (255, 255, 255))
    canvas.paste(photo, (0, 0))
    d = ImageDraw.Draw(canvas)

    # 橙色分割线
    d.rectangle([(0, TOP_H), (W, TOP_H + 4)], fill=(230, 80, 40))

    cy = TOP_H + 55

    # Logo (小一点，160px)
    logo_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        lw, lh = logo.size
        max_w = 160
        if lw > max_w:
            ratio = max_w / lw
            logo = logo.resize((max_w, int(lh * ratio)), Image.LANCZOS)
        canvas.paste(logo, (W - max_w - 40, cy), logo)

    # 日期（小）
    t(d, (55, cy + 5), "2026.05.14", fnt(20), (155, 155, 160))

    # 大标题（压缩成一行，更大字体居中）
    y = cy + 65
    title = "药品管理法明日正式施行"
    tbbox = d.textbbox((0, 0), title, font=fnt(68))
    tw = tbbox[2] - tbbox[0]
    t(d, ((W - tw) // 2, y), title, fnt(68), (25, 25, 28))

    # 副标题（小一号）
    sub = "市场独占期落地，进口新药加速进乐城"
    sbbox = d.textbbox((0, 0), sub, font=fnt(28))
    sw = sbbox[2] - sbbox[0]
    t(d, ((W - sw) // 2, y + 80), sub, fnt(28), (100, 100, 105))

    # 分割线
    ly = y + 145
    d.rectangle([(80, ly), (W - 80, ly + 1)], fill=(218, 218, 220))

    t(d, (80, ly + 20), "精算师视角", fnt(24), (230, 80, 40))

    # 四个要点，单行，压缩
    pts = [
        "15款国产1类新药密集获批",
        "29个乐城新技术已批准落地",
        "818号令施行，细胞治疗入监管时代",
        "ADC赛道爆发，中国进入全面爆发期",
    ]
    y3 = ly + 60
    lh2 = 50  # 每行高度50px
    for pt in pts:
        t(d, (80, y3), "•  " + pt, fnt(28), (50, 50, 55))
        y3 += lh2

    # 底部
    d.rectangle([(80, H - 175), (W - 80, H - 173)], fill=(218, 218, 220))
    t(d, (80, H - 140), "关注我，用精算师的眼睛看懂大健康", fnt(30), (25, 25, 28))
    t(d, (80, H - 85), "刘一｜精算师聊健康", fnt(20), (120, 120, 125))
    t(d, (80, H - 55), "海南博鳌乐城先行区", fnt(16), (150, 150, 155))

    out = r"C:\Users\Administrator\Downloads\daily_poster_v18.png"
    canvas.save(out, quality=93)
    sz = os.path.getsize(out) // 1024
    print(f"Done: {sz}KB")
    print(f"Content range: {cy} to {H}")
    print(f"Items: title={y}, sub={y+80}, line={ly}, pts={ly+60} to {y3}, bottom={H-175}")

make()