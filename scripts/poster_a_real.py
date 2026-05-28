"""
A风格 + 真实背景图
白底为主，图片点缀
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

def make_poster_a():
    from PIL import Image as PILImage

    # 白底背景
    bg = PILImage.new('RGB', (W, H), (250, 250, 248))
    d = ImageDraw.Draw(bg)

    # 加载真实图片（半透明叠加在白底上）
    photo = PILImage.open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\lecheng_official.jpg').convert('RGBA')

    # 裁切为9:16
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

    # 图片叠加在白底上（透明度30%，放在中右区域）
    # 右侧叠加，不遮挡左侧文字区
    overlay = PILImage.new('RGBA', (W, H), (0, 0, 0, 0))
    # 右侧图片区（宽40%，全高）
    left_img = int(W * 0.42)
    photo_cropped = photo.crop((0, 0, left_img, H))
    overlay.paste(photo_cropped, (0, 0), photo_cropped)

    # 加淡灰叠加层让图片退后
    gray = PILImage.new('RGBA', (W, H), (250, 250, 248, 60))
    overlay = PILImage.alpha_composite(overlay.convert('RGBA'), gray)

    # 图片放在右侧，左侧白底
    bg_rgba = bg.convert('RGBA')
    bg_rgba.paste(overlay, (0, 0), overlay)
    poster = bg_rgba.convert('RGB')
    d = ImageDraw.Draw(poster)

    # === 顶部 ===
    # 橙色装饰线
    d.rectangle([(50, 50), (W-50, 52)], fill=(230, 80, 40))
    # 日期
    t(d, (50, 68), '2026.05.14', fnt(22), (160, 160, 165))
    # 右上标签
    d.rectangle([(W-200, 65), (W-70, 88)], fill=(230, 80, 40))
    t(d, (W-195, 67), '乐城视角', fnt(18), (255, 255, 255))

    # === 大数字 ===
    y = 180
    nbbox = d.textbbox((0, 0), '480', font=fnt(240))
    nw2 = nbbox[2] - nbbox[0]
    cx = (W - nw2) // 2 + 50  # 往右偏一点，给左侧白底留字
    t(d, (cx, y), '480', fnt(240), (25, 25, 28))

    ubox = d.textbbox((0, 0), '万', font=fnt(80))
    uw = ubox[2] - ubox[0]
    t(d, (cx + nw2 + 5, y + 50), '万', fnt(80), (80, 80, 85))

    sub = '中国人每年新发癌症'
    sbbox = d.textbbox((0, 0), sub, font=fnt(34))
    sw = sbbox[2] - sbbox[0]
    t(d, ((W + 100 - sw) // 2, y + 280), sub, fnt(34), (100, 100, 105))

    # 分割线
    d.rectangle([(80, y + 350), (W - 80, y + 352)], fill=(220, 220, 225))

    # 精算师视角
    t(d, (80, y + 385), '精算师视角', fnt(26), (230, 80, 40))

    # 要点
    pts = [
        ('其中不到30%', '能用上新药'),
        ('原因一：海外新药国内未批',),
        ('原因二：普通家庭无力承担',),
        ('结果：等不起，也用不起',),
    ]
    y3 = y + 435
    for pt in pts:
        if len(pt) == 2:
            t(d, (80, y3), pt[0], fnt(36), (30, 30, 32))
            t(d, (80, y3 + 46), pt[1], fnt(36), (30, 30, 32))
        else:
            t(d, (80, y3), pt[0], fnt(28), (100, 100, 105))
        y3 += 58

    # 底部
    d.rectangle([(80, H - 200), (W - 80, H - 198)], fill=(220, 220, 225))
    t(d, (80, H - 165), '健康的人', fnt(44), (25, 25, 28))
    t(d, (80 + 310, H - 165), '不算账', fnt(44), (230, 80, 40))
    t(d, (80, H - 95), '刘一｜精算师聊健康', fnt(22), (120, 120, 125))
    t(d, (80, H - 60), '海南博鳌乐城先行区', fnt(18), (150, 150, 155))

    # logo（左上，和日期同高）
    logo_path = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png'
    if os.path.exists(logo_path):
        logo = PILImage.open(logo_path).convert('RGBA')
        lw, lh = logo.size
        max_w = 140
        if lw > max_w:
            ratio = max_w / lw
            logo = logo.resize((max_w, int(lh * ratio)), PILImage.LANCZOS)
        poster.paste(logo, (50, 50), logo)

    poster.save(r'C:\Users\Administrator\Downloads\daily_poster_A_real.png', quality=93)
    sz = os.path.getsize(r'C:\Users\Administrator\Downloads\daily_poster_A_real.png') // 1024
    print(f'Done: {sz}KB')

make_poster_a()
