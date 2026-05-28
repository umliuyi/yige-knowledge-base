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
    tr = 9.0 / 16.0
    pr = pw / ph
    if pr > tr:
        nw = int(ph * tr)
        photo = photo.crop(((pw - nw) // 2, 0, (pw + nw) // 2, ph))
    else:
        nh = int(pw / tr)
        photo = photo.crop((0, (ph - nh) // 2, pw, (ph + nh) // 2))
    photo = photo.resize((W, H), Image.LANCZOS)

    # 全幅暗化
    d = ImageDraw.Draw(photo)
    for y in range(H):
        if y < int(H * 0.30):
            continue
        rat = (y - H * 0.30) / (H * 0.70)
        alpha = int(200 * rat)
        for x in range(W):
            r2, g, b = photo.getpixel((x, y))
            photo.putpixel((x, y), (
                max(0, r2 - alpha),
                max(0, g - alpha),
                max(0, b - alpha)
            ))

    # 叠加白色区块承载文字
    white_top = int(H * 0.30)
    white_h = H - white_top
    white = Image.new('RGBA', (W, white_h), (255, 255, 255, 245))
    photo.paste(white, (0, white_top))

    # 白色区顶部橙色分割线
    d2 = ImageDraw.Draw(photo)
    d2.rectangle([(0, white_top - 3), (W, white_top)], fill=(230, 80, 40))

    # 内容起始Y
    cy = white_top + 65

    # logo加大
    logo_path = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png'
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        lw, lh = logo.size
        max_w = 180
        if lw > max_w:
            ratio = max_w / lw
            new_h = int(lh * ratio)
            logo = logo.resize((max_w, new_h), Image.LANCZOS)
        photo.paste(logo, (W - max_w - 55, white_top + 20), logo)

    # 日期
    t(d2, (55, cy), '2026.05.14', fnt(22), (155, 155, 160))

    # 大数字
    y = cy + 90
    nbbox = d2.textbbox((0, 0), '480', font=fnt(240))
    nw2 = nbbox[2] - nbbox[0]
    cx = (W - nw2) // 2
    t(d2, (cx - 2, y + 2), '480', fnt(240), (0, 0, 0))
    t(d2, (cx, y), '480', fnt(240), (25, 25, 28))

    ubbox = d2.textbbox((0, 0), '万', font=fnt(80))
    uw = ubbox[2] - ubbox[0]
    t(d2, (cx + nw2 + 5, y + 55), '万', fnt(80), (80, 80, 85))

    sub = '中国人每年新发癌症'
    sbbox = d2.textbbox((0, 0), sub, font=fnt(34))
    sw = sbbox[2] - sbbox[0]
    t(d2, ((W - sw) // 2, y + 270), sub, fnt(34), (100, 100, 105))

    # 分割线
    ly = y + 340
    d2.rectangle([(80, ly), (W - 80, ly + 1)], fill=(218, 218, 220))

    t(d2, (80, ly + 30), '精算师视角', fnt(26), (230, 80, 40))

    pts = [
        ('其中不到30%', '能用上新药'),
        ('原因一：海外新药国内未批',),
        ('原因二：普通家庭无力承担',),
        ('结果：等不起，也用不起',),
    ]
    y3 = ly + 75
    for pt in pts:
        if len(pt) == 2:
            t(d2, (80, y3), pt[0], fnt(36), (30, 30, 32))
            t(d2, (80, y3 + 46), pt[1], fnt(36), (30, 30, 32))
        else:
            t(d2, (80, y3), pt[0], fnt(28), (100, 100, 105))
        y3 += 58

    # 底部
    d2.rectangle([(80, H - 200), (W - 80, H - 198)], fill=(218, 218, 220))
    t(d2, (80, H - 165), '健康的人', fnt(44), (25, 25, 28))
    t(d2, (80 + 315, H - 165), '不算账', fnt(44), (230, 80, 40))
    t(d2, (80, H - 95), '刘一｜精算师聊健康', fnt(22), (120, 120, 125))
    t(d2, (80, H - 60), '海南博鳌乐城先行区', fnt(18), (150, 150, 155))

    photo_rgb = photo.convert('RGB')
    photo_rgb.save(r'C:\Users\Administrator\Downloads\daily_poster_full_bg.png', quality=93)
    sz = os.path.getsize(r'C:\Users\Administrator\Downloads\daily_poster_full_bg.png') // 1024
    print(f'Done: {sz}KB')

make()
