from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920

def fnt(size):
    for p in ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def t(draw, xy, text, font, fill):
    draw.text(xy, text, font=font, fill=fill)

def make():
    photo = Image.open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\lecheng_official.jpg').convert('RGB')
    pw, ph = photo.size
    photo_h = int(H * 0.20)
    photo_w = int(photo_h * pw / ph)
    photo_resized = photo.resize((photo_w, photo_h), Image.LANCZOS)

    white = Image.new('RGB', (W, H), (250, 250, 248))
    x_offset = 0
    white.paste(photo_resized, (x_offset, 0))

    d = ImageDraw.Draw(white)
    d.rectangle([(0, photo_h-2), (W, photo_h+2)], fill=(230, 80, 40))

    cy = photo_h + 60

    # logo加大到180px
    logo_path = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png'
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        lw, lh = logo.size
        max_w = 180
        if lw > max_w:
            ratio = max_w / lw
            new_h = int(lh * ratio)
            logo = logo.resize((max_w, new_h), Image.LANCZOS)
        logo_x = W - max_w - 55
        logo_y = cy - 5
        white.paste(logo, (logo_x, logo_y), logo)

    t(d, (55, cy), '2026.05.14', fnt(22), (155, 155, 160))

    y = cy + 100
    nbbox = d.textbbox((0, 0), '480', font=fnt(240))
    nw = nbbox[2] - nbbox[0]
    cx = (W - nw) // 2
    t(d, (cx, y), '480', fnt(240), (25, 25, 28))
    ubbox = d.textbbox((0, 0), '万', font=fnt(80))
    uw = ubbox[2] - ubbox[0]
    t(d, (cx + nw + 5, y + 60), '万', fnt(80), (80, 80, 85))

    sub = '中国人每年新发癌症'
    sbbox = d.textbbox((0, 0), sub, font=fnt(34))
    sw = sbbox[2] - sbbox[0]
    t(d, ((W - sw) // 2, y + 275), sub, fnt(34), (100, 100, 105))

    ly = y + 350
    d.rectangle([(80, ly), (W - 80, ly + 1)], fill=(218, 218, 220))
    t(d, (80, ly + 30), '精算师视角', fnt(26), (230, 80, 40))

    pts = [
        ('其中不到30%', '能用上新药'),
        ('原因一：海外新药国内未批',),
        ('原因二：普通家庭无力承担',),
        ('结果：等不起，也用不起',),
    ]
    y3 = ly + 75
    for pt in pts:
        if len(pt) == 2:
            t(d, (80, y3), pt[0], fnt(36), (30, 30, 32))
            t(d, (80, y3 + 46), pt[1], fnt(36), (30, 30, 32))
        else:
            t(d, (80, y3), pt[0], fnt(28), (100, 100, 105))
        y3 += 58

    d.rectangle([(80, H - 200), (W - 80, H - 198)], fill=(218, 218, 220))
    t(d, (80, H - 165), '健康的人', fnt(44), (25, 25, 28))
    t(d, (80 + 315, H - 165), '不算账', fnt(44), (230, 80, 40))
    t(d, (80, H - 95), '刘一｜精算师聊健康', fnt(22), (120, 120, 125))
    t(d, (80, H - 62), '海南博鳌乐城先行区', fnt(18), (150, 150, 155))

    white.save(r'C:\Users\Administrator\Downloads\daily_A_final2.png', quality=93)
    sz = os.path.getsize(r'C:\Users\Administrator\Downloads\daily_A_final2.png') // 1024
    print(f'Done: {sz}KB')

make()
