"""
乐城早报海报模板 v10
可配置，每天只需修改配置参数
"""
from PIL import Image, ImageDraw, ImageFont
import os, requests, io

W, H = 1080, 1920

def fnt(size):
    for p in ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def load_bg(cfg):
    bg_img = None
    local = cfg.get('bg_image_path')
    if local and os.path.exists(local):
        try:
            bg_img = Image.open(local)
            print(f"背景图: {bg_img.size}")
        except Exception as e:
            print(f"本地图片失败: {e}")
    if bg_img is None:
        url = cfg.get('bg_image_url', '')
        if url:
            try:
                r = requests.get(url, timeout=15, headers={'User-Agent':'Mozilla/5.0'})
                if r.status_code == 200 and len(r.content) > 30000:
                    bg_img = Image.open(io.BytesIO(r.content))
                    print(f"网络图: {bg_img.size}")
            except Exception as e:
                print(f"下载失败: {e}")
    if bg_img is None:
        bg_img = Image.new('RGB', (W, H), cfg.get('color_bg', (8,8,12)))
        d = ImageDraw.Draw(bg_img)
        for y in range(H):
            r = int(8 * (1-y/H) + 4*y/H)
            g = int(8 * (1-y/H) + 4*y/H)
            b = int(12 * (1-y/H) + 6*y/H)
            d.line([(0,y),(W,y)], fill=(r,g,b))
    pw, ph = bg_img.size
    tr = 9/16
    if pw/ph > tr:
        nw = int(ph * tr)
        bg_img = bg_img.crop(((pw-nw)//2, 0, (pw+nw)//2, ph))
    else:
        nh = int(pw / tr)
        bg_img = bg_img.crop((0, (ph-nh)//2, pw, (ph+nh)//2))
    bg_img = bg_img.resize((W, H), Image.LANCZOS)
    return bg_img

def draw_outline(draw, pos, text, font, fill, oc=(0,0,0), ow=3):
    x, y = pos
    for dx in range(-ow, ow+1):
        for dy in range(-ow, ow+1):
            if dx*dx+dy*dy <= ow*ow:
                draw.text((x+dx, y+dy), text, font=font, fill=oc)
    draw.text(pos, text, font=font, fill=fill)

def make_poster(cfg, output_path):
    poster = load_bg(cfg)
    d = ImageDraw.Draw(poster)

    # 底部渐变暗化
    gs = int(H * 0.35)
    for y in range(gs, H):
        rat = (y - gs) / (H - gs)
        dark = 1.0 - 0.75 * rat
        for x in range(W):
            r, g, b = poster.getpixel((x, y))
            poster.putpixel((x, y), (
                max(0, int(r * dark)),
                max(0, int(g * dark)),
                max(0, int(b * dark))))

    # 日期
    draw_outline(d, (55, 55), cfg['date'], fnt(24), (220,220,225), (0,0,0), 2)

    # 标签
    tag = cfg['tag']
    lbbox = d.textbbox((0,0), tag, font=fnt(18))
    lw = lbbox[2]-lbbox[0]
    d.rectangle([(W-55-lw-20,50),(W-55,78)], fill=cfg['color_accent'])
    d.text((W-55-lw-12,52), tag, font=fnt(18), fill=(255,255,255))

    # 大数字
    y = 170
    main = cfg['main_number']
    mbbox = d.textbbox((0,0), main, font=fnt(230))
    mw = mbbox[2]-mbbox[0]
    cx = (W - mw) // 2
    draw_outline(d, (cx-3, y+3), main, fnt(230), (0,0,0), (0,0,0), 5)
    draw_outline(d, (cx, y), main, fnt(230), (255,255,255), (0,0,0), 3)

    unit = cfg['main_unit']
    ubbox = d.textbbox((0,0), unit, font=fnt(68))
    uw = ubbox[2]-ubbox[0]
    d.text((cx+mw+5, y+50), unit, font=fnt(68), fill=(195,195,210))

    sub = cfg['main_desc']
    sbbox = d.textbbox((0,0), sub, font=fnt(36))
    sw = sbbox[2]-sbbox[0]
    d.text(((W-sw)//2, y+250), sub, font=fnt(36), fill=(225,225,230))

    # 精算视角区块
    y2 = y + 370
    pts = cfg['section_points']
    rh = len(pts) * 65 + 80
    rt = y2 - 15
    ri = Image.new('RGBA', (W-100, rh), (15,15,20,110))
    poster.paste(ri, (50, rt), ri)
    rd = ImageDraw.Draw(poster)
    rd.text((75, rt+15), cfg['section_title'], font=fnt(26), fill=cfg['color_accent'])
    y3 = rt + 60
    for pt in pts:
        if len(pt) == 2:
            draw_outline(rd, (75, y3), pt[0], fnt(42), (255,255,255), (0,0,0), 2)
            y3 += 56
            draw_outline(rd, (75, y3), pt[1], fnt(42), (255,255,255), (0,0,0), 2)
        else:
            rd.text((75, y3), pt[0], font=fnt(32), fill=(155,155,170))
        y3 += 65

    # 底部签名
    si = Image.new('RGBA', (W, 200), (0,0,0,170))
    poster.paste(si, (0, H-200), si)
    sd = ImageDraw.Draw(poster)
    draw_outline(sd, (75, H-130), cfg['quote1'], fnt(50), (195,195,205), (0,0,0), 3)
    sd.text((75+295, H-130), cfg['quote2'], font=fnt(50), fill=cfg['color_accent'])
    sd.text((75, H-70), cfg['signature'], font=fnt(26), fill=(135,135,145))
    sd.text((75, H-38), cfg['location'], font=fnt(20), fill=(85,85,95))
    ds = cfg['date']
    dbbox = sd.textbbox((0,0), ds, font=fnt(20))
    dw = dbbox[2]-dbbox[0]
    sd.text((W-75-dw, H-38), ds, font=fnt(20), fill=(85,85,95))

    poster_rgb = poster.convert('RGB')
    poster_rgb.save(output_path, quality=93)
    sz = os.path.getsize(output_path) // 1024
    print(f"Done: {sz}KB")


# ==================== 每日配置 ====================
if __name__ == '__main__':
    cfg = {
        'date': '2026.05.13',
        'weekday': '星期二',
        'main_number': '480',
        'main_unit': '万',
        'main_desc': '中国人每年新发癌症',
        'section_title': '精算师视角',
        'section_points': [
            ('其中不到30%', '能用上新药'),
            ('原因一：海外新药国内未批',),
            ('原因二：普通家庭无力承担',),
            ('结果：等不起，也用不起',),
        ],
        'quote1': '健康的人',
        'quote2': '不算账',
        'signature': '刘一｜精算师聊健康',
        'location': '海南博鳌乐城先行区',
        'tag': '乐城视角',
        'bg_image_path': r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\template_bg_test.jpg',
        'bg_image_url': '',
        'color_accent': (210, 50, 30),
        'color_bg': (8, 8, 12),
    }
    out = r'C:\Users\Administrator\Downloads\daily_news_poster_template.png'
    make_poster(cfg, out)
