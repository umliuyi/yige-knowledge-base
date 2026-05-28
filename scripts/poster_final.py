from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920

def fnt(size):
    for p in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def txt(draw, xy, text, font, fill):
    draw.text(xy, text, font=font, fill=fill)

def make():
    photo = Image.open(r"C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\lecheng_official.jpg").convert("RGB")
    pw, ph = photo.size
    target = 9.0 / 16.0
    ratio = pw / ph
    if ratio > target:
        nw = int(ph * target)
        photo = photo.crop(((pw - nw) // 2, 0, (pw + nw) // 2, ph))
    else:
        nh = int(pw / target)
        photo = photo.crop((0, (ph - nh) // 2, pw, (ph + nh) // 2))
    photo = photo.resize((W, H), Image.LANCZOS)

    # White block from 30% downward (no dark overlay on image)
    white_top = int(H * 0.30)
    white_h = H - white_top
    white_block = Image.new("RGBA", (W, white_h), (255, 255, 255, 245))
    photo.paste(white_block, (0, white_top), white_block)

    d = ImageDraw.Draw(photo)

    # Orange line at white block top
    d.rectangle([(0, white_top - 3), (W, white_top)], fill=(230, 80, 40))

    content_y = white_top + 65

    # Logo (180px wide, top-right of white block)
    logo_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        lw, lh = logo.size
        max_w = 180
        if lw > max_w:
            r = max_w / lw
            logo = logo.resize((max_w, int(lh * r), Image.LANCZOS)
        photo.paste(logo, (W - max_w - 55, content_y), logo)

    # Date (top-left of white block)
    txt(d, (55, content_y), "2026.05.14", fnt(22), (155, 155, 160))

    # Big number
    y = content_y + 90
    nbbox = d.textbbox((0, 0), "480", font=fnt(240))
    nw = nbbox[2] - nbbox[0]
    cx = (W - nw) // 2
    txt(d, (cx, y), "480", fnt(240), (25, 25, 28))

    ubbox = d.textbbox((0, 0), "万", font=fnt(80))
    uw = ubbox[2] - ubbox[0]
    txt(d, (cx + nw + 5, y + 55), "万", fnt(80), (80, 80, 85))

    sub = "中国人每年新发癌症"
    sbbox = d.textbbox((0, 0), sub, font=fnt(34))
    sw = sbbox[2] - sbbox[0]
    txt(d, ((W - sw) // 2, y + 270), sub, fnt(34), (100, 100, 105))

    # Divider
    ly = y + 340
    d.rectangle([(80, ly), (W - 80, ly + 1)], fill=(218, 218, 220))

    txt(d, (80, ly + 30), "精算师视角", fnt(26), (230, 80, 40))

    pts = [
        ("其中不到30%", "能用上新药"),
        ("原因一：海外新药国内未批",),
        ("原因二：普通家庭无力承担",),
        ("结果：等不起，也用不起",),
    ]
    y3 = ly + 75
    for pt in pts:
        if len(pt) == 2:
            txt(d, (80, y3), pt[0], fnt(36), (30, 30, 32))
            txt(d, (80, y3 + 46), pt[1], fnt(36), (30, 30, 32))
        else:
            txt(d, (80, y3), pt[0], fnt(28), (100, 100, 105))
        y3 += 58

    # Bottom
    d.rectangle([(80, H - 200), (W - 80, H - 198)], fill=(218, 218, 220))
    txt(d, (80, H - 165), "健康的人", fnt(44), (25, 25, 28))
    txt(d, (80 + 315, H - 165), "不算账", fnt(44), (230, 80, 40))
    txt(d, (80, H - 95), "刘一｜精算师聊健康", fnt(22), (120, 120, 125))
    txt(d, (80, H - 62), "海南博鳌乐城先行区", fnt(18), (150, 150, 155))

    out = r"C:\Users\Administrator\Downloads\daily_poster_final.png"
    photo.save(out, quality=93)
    print(f"Done: {os.path.getsize(out) // 1024}KB")

make()
