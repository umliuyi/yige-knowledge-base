"""
顶部占1/5，背景图填满那1/5，不裁切保持原比例
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920
PHOTO_TOP = int(H * 0.20)  # 顶部1/5 = 384px

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

    # 高度方向填满1/5宽度(1080)，高度保持比例不裁切
    # 缩放到宽度1080，高度等比
    scale = W / pw
    new_h = int(ph * scale)
    photo = photo.resize((W, new_h), Image.LANCZOS)

    # 创建白底画布
    canvas = Image.new('RGB', (W, H), (255, 255, 255))

    # 把图片粘贴到顶部（不裁切，保持原比例）
    canvas.paste(photo, (0, 0))

    # 在图片底部和白色区交界处做渐变过渡
    grad_h = 80
    grad_top = new_h
    for i in range(grad_h):
        alpha = int(200 * i / grad_h)
        for x in range(W):
            y = grad_top + i
            if y >= H:
                break
            r, g, b = canvas.getpixel((x, y))
            canvas.putpixel((x, y), (
                int((r * alpha + 255 * (grad_h - i)) / grad_h),
                int((g * alpha + 255 * (grad_h - i)) / grad_h),
                int((b * alpha + 255 * (grad_h - i)) / grad_h)
            ))

    # 白色区块从1/5处开始
    white_block = Image.new('RGB', (W, H - PHOTO_TOP), (255, 255, 255))
    canvas.paste(white_block, (0, PHOTO_TOP))

    d = ImageDraw.Draw(canvas)

    # 橙色分割线
    d.rectangle([(0, PHOTO_TOP - 3), (W, PHOTO_TOP)], fill=(230, 80, 40))

    content_y = PHOTO_TOP + 65

    # Logo (180px)
    logo_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        lw, lh = logo.size
        max_w = 180
        if lw > max_w:
            ratio = max_w / lw
            logo = logo.resize((max_w, int(lh * ratio)), Image.LANCZOS)
        canvas.paste(logo, (W - max_w - 55, content_y), logo)

    # 日期
    t(d, (55, content_y), "2026.05.14", fnt(22), (155, 155, 160))

    # 大数字
    y = content_y + 90
    nbbox = d.textbbox((0, 0), "480", font=fnt(240))
    nw = nbbox[2] - nbbox[0]
    cx = (W - nw) // 2
    t(d, (cx, y), "480", fnt(240), (25, 25, 28))

    ubbox = d.textbbox((0, 0), "万", font=fnt(80))
    t(d, (cx + nw + 5, y + 55), "万", fnt(80), (80, 80, 85))

    sub = "中国人每年新发癌症"
    sbbox = d.textbbox((0, 0), sub, font=fnt(34))
    sw = sbbox[2] - sbbox[0]
    t(d, ((W - sw) // 2, y + 270), sub, fnt(34), (100, 100, 105))

    # 分割线
    ly = y + 340
    d.rectangle([(80, ly), (W - 80, ly + 1)], fill=(218, 218, 220))

    t(d, (80, ly + 30), "精算师视角", fnt(26), (230, 80, 40))

    pts = [
        ("其中不到30%", "能用上新药"),
        ("原因一：海外新药国内未批",),
        ("原因二：普通家庭无力承担",),
        ("结果：等不起，也用不起",),
    ]
    y3 = ly + 75
    for pt in pts:
        if len(pt) == 2:
            t(d, (80, y3), pt[0], fnt(36), (30, 30, 32))
            t(d, (80, y3 + 46), pt[1], fnt(36), (30, 30, 32))
        else:
            t(d, (80, y3), pt[0], fnt(28), (100, 100, 105))
        y3 += 58

    # 底部
    d.rectangle([(80, H - 200), (W - 80, H - 198)], fill=(218, 218, 220))
    t(d, (80, H - 165), "健康的人", fnt(44), (25, 25, 28))
    t(d, (80 + 315, H - 165), "不算账", fnt(44), (230, 80, 40))
    t(d, (80, H - 95), "刘一｜精算师聊健康", fnt(22), (120, 120, 125))
    t(d, (80, H - 62), "海南博鳌乐城先行区", fnt(18), (150, 150, 155))

    out = r"C:\Users\Administrator\Downloads\daily_poster_1of5.png"
    canvas.save(out, quality=93)
    print(f"Done: {os.path.getsize(out) // 1024}KB")

make()