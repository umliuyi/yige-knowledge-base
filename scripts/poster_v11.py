"""
乐城早报海报 v11 - 回v9结构，减中间区块的重量感
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920

def fnt(size):
    for p in ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def load_bg(path):
    from PIL import Image
    img = Image.open(path).convert('RGB')
    pw, ph = img.size
    tr = 9/16
    if pw/ph > tr:
        nw = int(ph * tr)
        img = img.crop(((pw-nw)//2, 0, (pw+nw)//2, ph))
    else:
        nh = int(pw / tr)
        img = img.crop((0, (ph-nh)//2, pw, (ph+nh)//2))
    return img.resize((W, H), Image.LANCZOS)

def draw_outline(draw, pos, text, font, fill, oc=(0,0,0), ow=2):
    x, y = pos
    for dx in range(-ow, ow+1):
        for dy in range(-ow, ow+1):
            if dx*dx+dy*dy <= ow*ow:
                draw.text((x+dx, y+dy), text, font=font, fill=oc)
    draw.text(pos, text, font=font, fill=fill)

def make_v11(bg_path, logo_path, output):
    # 背景
    bg = load_bg(bg_path)

    # 底部渐变暗化
    gs = int(H * 0.38)
    for y in range(gs, H):
        rat = (y - gs) / (H - gs)
        dark = 1.0 - 0.82 * rat
        for x in range(W):
            r, g, b = bg.getpixel((x, y))
            bg.putpixel((x, y), (
                max(0, int(r * dark)),
                max(0, int(g * dark)),
                max(0, int(b * dark))))

    d = ImageDraw.Draw(bg)

    # 顶部日期（左上）
    draw_outline(d, (50, 50), '2026.05.14', fnt(22), (200,200,210), (0,0,0), 1)

    # 右上标签（细边框）
    tag = '乐城视角'
    tbbox = d.textbbox((0,0), tag, font=fnt(17))
    tw = tbbox[2]-tbbox[0]
    d.rectangle([(W-55-tw-20, 46),(W-55, 74)], outline=(220,60,35), width=1)
    d.text((W-55-tw-12, 48), tag, font=fnt(17), fill=(255,255,255))

    # === 大数字区 ===
    y = 155
    nbbox = d.textbbox((0,0), '480', font=fnt(230))
    nw = nbbox[2]-nbbox[0]
    cx = (W - nw) // 2
    draw_outline(d, (cx-2, y+2), '480', fnt(230), (0,0,0), (0,0,0), 4)
    draw_outline(d, (cx, y), '480', fnt(230), (255,255,255), (0,0,0), 2)

    ubbox = d.textbbox((0,0), '万', font=fnt(65))
    uw = ubbox[2]-ubbox[0]
    d.text((cx+nw+5, y+45), '万', font=fnt(65), fill=(190,190,205))

    sub = '中国人每年新发癌症'
    sbbox = d.textbbox((0,0), sub, font=fnt(32))
    sw = sbbox[2]-sbbox[0]
    d.text(((W-sw)//2, y+260), sub, font=fnt(32), fill=(200,200,210))

    # 细分割线
    line_y = y + 335
    d.rectangle([(W//4, line_y),(W-W//4, line_y+1)], fill=(220,60,35))

    # === 中间区域：精算师视角 ===
    # 用留白+细线代替实底色块
    y2 = line_y + 35

    # 小标题
    d.text((W//4, y2), '精算师视角', font=fnt(22), fill=(220,60,35))

    # 要点：左对齐，字号缩小，行距适中，留白
    pts = [
        ('其中不到30%', '能用上新药'),
        ('原因一：海外新药国内未批',),
        ('原因二：普通家庭无力承担',),
    ]
    y3 = y2 + 42
    for pt in pts:
        if len(pt) == 2:
            draw_outline(d, (W//4, y3), pt[0], fnt(36), (255,255,255), (0,0,0), 1)
            y3 += 42
            draw_outline(d, (W//4, y3), pt[1], fnt(36), (255,255,255), (0,0,0), 1)
        else:
            d.text((W//4, y3), pt[0], font=fnt(28), fill=(140,140,155))
        y3 += 56

    # 再一条分割线
    line2_y = y3 + 25
    d.rectangle([(W//4, line2_y),(W-W//4, line2_y+1)], fill=(50,50,60))

    # 一句结论
    d.text((W//4, line2_y+20), '结果：等不起，也用不起', font=fnt(28), fill=(160,160,175))

    # === 底部金句 ===
    sig_top = H - 170
    d.rectangle([(W//4, sig_top),(W-W//4, sig_top+1)], fill=(220,60,35))

    q1 = '健康的人'
    q2 = '不算账'
    draw_outline(d, (W//4+20, sig_top+25), q1, fnt(46), (200,200,210), (0,0,0), 2)
    d.text((W//4+20+330, sig_top+25), q2, font=fnt(46), fill=(220,60,35))

    # 签名
    d.text((W//4, sig_top+95), '刘一｜精算师聊健康', font=fnt(22), fill=(120,120,130))
    d.text((W//4, sig_top+125), '海南博鳌乐城先行区', font=fnt(18), fill=(80,80,95))

    # 日期右下
    ds = '2026.05.14'
    dbbox = d.textbbox((0,0), ds, font=fnt(18))
    dw = dbbox[2]-dbbox[0]
    d.text((W-W//4-dw, sig_top+125), ds, font=fnt(18), fill=(80,80,95))

    # === logo（右上区域，和日期同高）===
    if logo_path and os.path.exists(logo_path):
        from PIL import Image as PILImage
        logo = PILImage.open(logo_path).convert('RGBA')
        lw, lh = logo.size
        max_w = 160
        if lw > max_w:
            ratio = max_w / lw
            logo = logo.resize((max_w, int(lh * ratio)), PILImage.LANCZOS)
        logo_pos = (W - max_w - 50, 50)
        bg.paste(logo, logo_pos, logo)

    bg_rgb = bg.convert('RGB')
    bg_rgb.save(output, quality=93)
    print(f'Done: {os.path.getsize(output)//1024}KB')
    return output

if __name__ == '__main__':
    bg = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\lecheng_official.jpg'
    logo = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png'
    out = r'C:\Users\Administrator\Downloads\daily_news_v11.png'
    make_v11(bg, logo, out)
