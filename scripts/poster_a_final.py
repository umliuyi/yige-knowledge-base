"""
A风格：顶部1/4图片 + 下面白色
logo放白色区右上角
"""
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
    from PIL import Image as PILImage

    photo = PILImage.open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\lecheng_official.jpg').convert('RGB')
    pw, ph = photo.size
    tr = 9.0 / 16.0
    pr = pw / ph
    if pr > tr:
        nw = int(ph * tr)
        photo = photo.crop(((pw-nw)//2, 0, (pw+nw)//2, ph))
    else:
        nh = int(pw / tr)
        photo = photo.crop((0, (ph-nh)//2, pw, (ph+nh)//2))
    photo = photo.resize((W, H), PILImage.LANCZOS)

    # 顶部1/4高度
    photo_top = int(H * 0.26)
    # 裁切图片顶部1/4
    photo_cropped = photo.crop((0, 0, W, photo_top))

    # 白色背景
    white = PILImage.new('RGB', (W, H), (250, 250, 248))

    # 把图片贴在白色底的顶部
    white.paste(photo_cropped, (0, 0))

    d = ImageDraw.Draw(white)

    # === 图片与白色区的分割线 ===
    d.rectangle([(0, photo_top-1), (W, photo_top+2)], fill=(230, 80, 40))

    # === 白色区域的顶部padding ===
    content_top = photo_top + 60  # 内容从图片下方60px开始

    # === 日期（左上，在白色区） ===
    t(d, (55, content_top + 5), '2026.05.14', fnt(22), (155, 155, 160))

    # === logo（白色区右上角，避开短视频发布按钮）===
    logo_path = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png'
    if os.path.exists(logo_path):
        logo = PILImage.open(logo_path).convert('RGBA')
        lw, lh = logo.size
        max_w = 140
        if lw > max_w:
            ratio = max_w / lw
            logo = logo.resize((max_w, int(lh * ratio)), PILImage.LANCZOS)
        # logo在白色区右上角（避开发布按钮，通常在更靠右或更靠上）
        logo_x = W - max_w - 50
        logo_y = content_top + 5
        white.paste(logo, (logo_x, logo_y), logo)

    # === 大数字 ===
    y = content_top + 110
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
    t(d, ((W - sw)//2, y + 275), sub, fnt(34), (100, 100, 105))

    # 分割线
    line_y = y + 350
    d.rectangle([(80, line_y), (W - 80, line_y + 1)], fill=(218, 218, 220))

    # === 精算师视角 ===
    t(d, (80, line_y + 30), '精算师视角', fnt(26), (230, 80, 40))

    pts = [
        ('其中不到30%', '能用上新药'),
        ('原因一：海外新药国内未批',),
        ('原因二：普通家庭无力承担',),
        ('结果：等不起，也用不起',),
    ]
    y3 = line_y + 75
    for pt in pts:
        if len(pt) == 2:
            t(d, (80, y3), pt[0], fnt(36), (30, 30, 32))
            t(d, (80, y3 + 46), pt[1], fnt(36), (30, 30, 32))
        else:
            t(d, (80, y3), pt[0], fnt(28), (100, 100, 105))
        y3 += 58

    # === 底部金句 ===
    d.rectangle([(80, H - 200), (W - 80, H - 198)], fill=(218, 218, 220))
    t(d, (80, H - 165), '健康的人', fnt(44), (25, 25, 28))
    t(d, (80 + 315, H - 165), '不算账', fnt(44), (230, 80, 40))
    t(d, (80, H - 95), '刘一｜精算师聊健康', fnt(22), (120, 120, 125))
    t(d, (80, H - 62), '海南博鳌乐城先行区', fnt(18), (150, 150, 155))

    white.save(r'C:\Users\Administrator\Downloads\daily_A_final.png', quality=93)
    sz = os.path.getsize(r'C:\Users\Administrator\Downloads\daily_A_final.png') // 1024
    print(f'Done: {sz}KB')

make()
