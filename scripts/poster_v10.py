"""
乐城早报海报 v10 - 极简电影感
核心原则：只有一个焦点，其余全部弱化
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920

def fnt(size):
    for p in ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def load_bg(path_or_url):
    from PIL import Image
    import io, requests
    if path_or_url and os.path.exists(path_or_url):
        img = Image.open(path_or_url).convert('RGB')
    else:
        img = Image.new('RGB', (W, H), (5, 8, 15))
    # crop to 9:16
    pw, ph = img.size
    tr = 9/16
    if pw/ph > tr:
        nw = int(ph * tr)
        img = img.crop(((pw-nw)//2, 0, (pw+nw)//2, ph))
    else:
        nh = int(pw / tr)
        img = img.crop((0, (ph-nh)//2, pw, (ph+nh)//2))
    img = img.resize((W, H), Image.LANCZOS)
    return img

def make_poster(bg_path, date, big_number, big_unit, quote1, quote2, signature, location, tag, accent, output):
    # 背景
    bg = load_bg(bg_path)

    # 底部大面积渐变暗化（为文字留白）
    for y in range(int(H * 0.4), H):
        ratio = (y - H * 0.4) / (H * 0.6)
        darken = 1.0 - 0.80 * ratio
        for x in range(W):
            r, g, b = bg.getpixel((x, y))
            bg.putpixel((x, y), (
                max(0, int(r * darken)),
                max(0, int(g * darken)),
                max(0, int(b * darken))))

    d = ImageDraw.Draw(bg)

    # === 顶部：极简 ==
    # 日期（小字，右上）
    date_bbox = d.textbbox((0,0), date, font=fnt(20))
    d.text((W - date_bbox[2] - 55, 50), date, font=fnt(20), fill=(200, 200, 210))

    # 左上：标签（细线框）
    lbbox = d.textbbox((0,0), tag, font=fnt(18))
    lw = lbbox[2] - lbbox[0]
    # 细边框标签
    d.rectangle([(50, 48), (50+lw+24, 78)], outline=accent, width=1)
    d.text((50+12, 50), tag, font=fnt(18), fill=(255,255,255))

    # === 唯一焦点：超大数字 ===
    # 数字占据画面中部约40%高度，视觉冲击力
    num_y = int(H * 0.32)
    num_size = 280
    nf = fnt(num_size)
    nbbox = d.textbbox((0,0), big_number, font=nf)
    nw = nbbox[2] - nbbox[0]

    # 白色数字，居中，加微阴影
    shadow_nf = fnt(num_size)
    for dx, dy in [(3,3), (2,2), (1,1)]:
        d.text(((W-nw)//2+dx, num_y+dy), big_number, font=shadow_nf, fill=(0,0,0))
    d.text(((W-nw)//2, num_y), big_number, font=nf, fill=(255,255,255))

    # 单位（同行，小一号）
    unit_f = fnt(90)
    ubbox = d.textbbox((0,0), big_unit, font=unit_f)
    uw = ubbox[2] - ubbox[0]
    d.text(((W+nw)//2 + 5, num_y + 30), big_unit, font=unit_f, fill=(200,200,215))

    # === 唯一金句 ===
    # 极简分割线
    line_y = int(H * 0.60)
    d.rectangle([(W//4, line_y), (W-W//4, line_y+1)], fill=accent)

    # 金句分两行，超大，超强对比
    q1_y = line_y + 40
    q1 = quote1
    q1f = fnt(72)
    q1bbox = d.textbbox((0,0), q1, font=q1f)
    q1w = q1bbox[2] - q1bbox[0]
    # 白色
    d.text(((W-q1w)//2, q1_y), q1, font=q1f, fill=(255,255,255))

    q2_y = q1_y + 80
    q2 = quote2
    q2f = fnt(72)
    q2bbox = d.textbbox((0,0), q2, font=q2f)
    q2w = q2bbox[2] - q2bbox[0]
    # 强调色
    d.text(((W-q2w)//2, q2_y), q2, font=q2f, fill=accent)

    # === 底部签名（极小，留白）===
    sig_y = H - 90
    sig_f = fnt(24)
    d.text((55, sig_y), signature, font=sig_f, fill=(150,150,160))
    loc_f = fnt(18)
    d.text((55, sig_y + 32), location, font=loc_f, fill=(100,100,110))

    bg.save(output, quality=93)
    sz = os.path.getsize(output) // 1024
    print(f"Done: {sz}KB")
    return sz

if __name__ == '__main__':
    bg = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\lecheng_official.jpg'
    out = r'C:\Users\Administrator\Downloads\daily_news_v10.png'
    make_poster(
        bg_path=bg,
        date='2026.05.14',
        big_number='480',
        big_unit='万',
        quote1='健康的人',
        quote2='不算账',
        signature='刘一｜精算师聊健康',
        location='海南博鳌乐城先行区',
        tag='乐城视角',
        accent=(220, 60, 35),
        output=out
    )
