"""
v20 - 顶部图片加大10%，四个序号等间距分布
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920
TOP_H = int(H * 0.24)  # 加大10%: 1920*0.24 = 461px（原20%=384px）

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

    # 照片底部柔和渐变
    fade = Image.new('RGBA', (W, 80), (0, 0, 0, 0))
    for y in range(80):
        alpha = int(220 * y / 80)
        for x in range(W):
            fade.putpixel((x, y), (0, 0, 0, alpha))
    photo_rgba = photo.convert('RGBA')
    photo_rgba.paste(fade, (0, TOP_H - 80))

    # 白底
    canvas = Image.new('RGB', (W, H), (255, 255, 255))
    canvas.paste(photo_rgba, (0, 0))
    d = ImageDraw.Draw(canvas)

    # 分割线
    d.rectangle([(0, TOP_H), (W, TOP_H + 3)], fill=(220, 75, 35))

    # 白色区起点
    cy = TOP_H + 40

    # 日期（左上）
    t(d, (55, cy), "2026.05.14", fnt(20), (160, 160, 165))

    # Logo（右上）
    logo_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        lw, lh = logo.size
        max_w = 160
        if lw > max_w:
            ratio = max_w / lw
            logo = logo.resize((max_w, int(lh * ratio)), Image.LANCZOS)
        canvas.paste(logo, (W - max_w - 40, cy), logo)

    # 主标题
    y = cy + 80
    title = "药品管理法明日正式施行"
    tbbox = d.textbbox((0, 0), title, font=fnt(72))
    tw = tbbox[2] - tbbox[0]
    t(d, ((W - tw) // 2, y), title, fnt(72), (20, 20, 25))

    # 副标题
    sub = "市场独占期落地，进口新药加速进乐城"
    sbbox = d.textbbox((0, 0), sub, font=fnt(28))
    sw = sbbox[2] - sbbox[0]
    t(d, ((W - sw) // 2, y + 95), sub, fnt(28), (110, 110, 115))

    # 分割线
    ly = y + 160
    d.rectangle([(80, ly), (W - 80, ly + 1)], fill=(210, 210, 215))

    # 精算师视角标签
    t(d, (80, ly + 18), "精算师视角", fnt(22), (220, 75, 35))

    # 四个要点：等间距从cy3到bottom_y均匀排列
    pts = [
        ("01", "15款国产1类新药密集获批"),
        ("02", "29个乐城新技术已批准落地"),
        ("03", "818号令施行，细胞治疗入监管时代"),
        ("04", "ADC赛道爆发，中国进入全面爆发期"),
    ]

    start_y = ly + 65
    end_y = H - 175  # 底部分割线位置
    total_space = end_y - start_y
    spacing = total_space // 5  # 分成5个空格（4项+间隔）

    for i, (num, desc) in enumerate(pts):
        py = start_y + i * spacing
        # 序号
        t(d, (80, py), num, fnt(36), (220, 75, 35))
        # 数字+描述
        nbbox = d.textbbox((0, 0), num, font=fnt(36))
        t(d, (140, py + 3), desc, fnt(30), (60, 60, 65))

    # 底部分割线
    d.rectangle([(80, H - 175), (W - 80, H - 173)], fill=(210, 210, 215))

    # 底部签名
    t(d, (80, H - 140), "关注我，用精算师的眼睛看懂大健康", fnt(30), (20, 20, 25))
    t(d, (80, H - 88), "刘一｜精算师聊健康", fnt(20), (130, 130, 135))
    t(d, (80, H - 58), "海南博鳌乐城先行区", fnt(16), (160, 160, 165))

    out = r"C:\Users\Administrator\Downloads\daily_poster_v20.png"
    canvas.save(out, quality=93)
    print(f"Done: {os.path.getsize(out)//1024}KB  photo_top=0-{TOP_H}  content={cy}-{H}")

make()