"""
乐城早报 v12 - 文字可读性优先
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920

def fnt(size):
    for p in ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def make_v12(bg_path, logo_path, output):
    from PIL import Image as PILImage

    # Load and crop background
    bg = PILImage.open(bg_path).convert('RGB')
    pw, ph = bg.size
    target = 9.0 / 16.0
    ratio = pw / ph
    if ratio > target:
        nw = int(ph * target)
        bg = bg.crop(((pw - nw) // 2, 0, (pw + nw) // 2, ph))
    else:
        nh = int(pw / target)
        bg = bg.crop((0, (ph - nh) // 2, pw, (ph + nh) // 2))
    bg = bg.resize((W, H), PILImage.LANCZOS)

    # Darken bottom 60%
    dark = bg.copy()
    d = ImageDraw.Draw(dark)
    for y in range(H):
        if y < int(H * 0.35):
            continue
        rat = (y - H * 0.35) / (H * 0.65)
        alpha = int(100 + 120 * rat)
        for x in range(W):
            r2, g2, b2 = dark.getpixel((x, y))
            dark.putpixel((x, y), (
                max(0, r2 - alpha),
                max(0, g2 - alpha),
                max(0, b2 - alpha)
            ))
    poster = dark
    pd = ImageDraw.Draw(poster)

    def txt(pos, text, font, fill, oc=(0,0,0), ow=5):
        x, y = pos
        for dx in range(-ow, ow+1):
            for dy in range(-ow, ow+1):
                if dx*dx + dy*dy <= ow*ow:
                    pd.text((x+dx, y+dy), text, font=font, fill=oc)
        pd.text(pos, text, font=font, fill=fill)

    # Date top-left
    txt((55, 52), '2026.05.14', fnt(24), (210,210,220), (0,0,0), 3)

    # Tag top-right
    tag = '乐城视角'
    tbbox = pd.textbbox((0,0), tag, font=fnt(18))
    tw = tbbox[2] - tbbox[0]
    pd.rectangle([(W-55-tw-24, 48), (W-55, 76)], fill=(220,60,35))
    pd.text((W-55-tw-16, 50), tag, font=fnt(18), fill=(255,255,255))

    # Big number
    y = 160
    nbbox = pd.textbbox((0,0), '480', font=fnt(240))
    nw2 = nbbox[2] - nbbox[0]
    cx = (W - nw2) // 2
    txt((cx-3, y+3), '480', fnt(240), (0,0,0), (0,0,0), 6)
    txt((cx, y), '480', fnt(240), (255,255,255), (0,0,0), 4)

    ubbox = pd.textbbox((0,0), '万', font=fnt(72))
    uw = ubbox[2] - ubbox[0]
    pd.text((cx+nw2+5, y+55), '万', font=fnt(72), fill=(180,180,205))

    sub = '中国人每年新发癌症'
    sbbox = pd.textbbox((0,0), sub, font=fnt(34))
    sw = sbbox[2] - sbbox[0]
    txt(((W-sw)//2, y+265), sub, fnt(34), (200,200,215), (0,0,0), 3)

    ly = y + 340
    pd.rectangle([(W//4, ly), (W-W//4, ly+1)], fill=(220,60,35))

    # Middle info block with semi-transparent bg
    mid_top = ly + 25
    mid_h = 380
    mid_img = PILImage.new('RGBA', (W, mid_h), (0, 0, 0, 0))
    md = ImageDraw.Draw(mid_img)
    md.rectangle([(0, 0), (W, mid_h)], fill=(0, 0, 0, 105))
    poster.paste(mid_img, (0, mid_top), mid_img)
    md2 = ImageDraw.Draw(poster)

    md2.text((W//4, mid_top+15), '精算师视角', font=fnt(26), fill=(220,60,35))

    pts = [
        ('其中不到30%', '能用上新药'),
        ('原因一：海外新药国内未批',),
        ('原因二：普通家庭无力承担',),
        ('结果：等不起，也用不起',),
    ]
    y3 = mid_top + 60
    for pt in pts:
        if len(pt) == 2:
            txt((W//4, y3), pt[0], fnt(40), (255,255,255), (0,0,0), 3)
            y3 += 52
            txt((W//4, y3), pt[1], fnt(40), (255,255,255), (0,0,0), 3)
        else:
            md2.text((W//4, y3), pt[0], font=fnt(30), fill=(130,130,150))
        y3 += 62

    # Bottom signature block
    bot_top = H - 200
    bot_img = PILImage.new('RGBA', (W, 200), (0, 0, 0, 0))
    bld = ImageDraw.Draw(bot_img)
    bld.rectangle([(0, 0), (W, 200)], fill=(0, 0, 0, 160))
    poster.paste(bot_img, (0, bot_top), bot_img)
    bld2 = ImageDraw.Draw(poster)

    txt((W//4, bot_top+20), '健康的人', fnt(50), (190,190,205), (0,0,0), 4)
    bld2.text((W//4+380, bot_top+20), '不算账', font=fnt(50), fill=(220,60,35))
    bld2.text((W//4, bot_top+95), '刘一｜精算师聊健康', font=fnt(24), fill=(120,120,135))
    bld2.text((W//4, bot_top+128), '海南博鳌乐城先行区', font=fnt(20), fill=(80,80,95))

    ds = '2026.05.14'
    dbbox = bld2.textbbox((0,0), ds, font=fnt(20))
    dw = dbbox[2] - dbbox[0]
    bld2.text((W-W//4-dw, bot_top+128), ds, font=fnt(20), fill=(80,80,95))

    # Logo
    if logo_path and os.path.exists(logo_path):
        logo = PILImage.open(logo_path).convert('RGBA')
        lw2, lh2 = logo.size
        max_w = 150
        if lw2 > max_w:
            rat2 = max_w / lw2
            logo = logo.resize((max_w, int(lh2 * rat2)), PILImage.LANCZOS)
        poster.paste(logo, (50, 50), logo)

    poster_rgb = poster.convert('RGB')
    poster_rgb.save(output, quality=93)
    print(f'Done: {os.path.getsize(output)//1024}KB')

if __name__ == '__main__':
    bg = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\lecheng_official.jpg'
    logo = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png'
    out = r'C:\Users\Administrator\Downloads\daily_news_v12.png'
    make_v12(bg, logo, out)
