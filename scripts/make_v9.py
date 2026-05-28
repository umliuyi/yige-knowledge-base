from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920

# Load photo as full background
photo = Image.open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\photo_new.jpg')
print(f"Photo: {photo.size}")

# Crop to 9:16 portrait
pw, ph = photo.size
target_ratio = 9/16
photo_ratio = pw/ph
if photo_ratio > target_ratio:
    new_w = int(ph * target_ratio)
    left = (pw - new_w) // 2
    photo = photo.crop((left, 0, left + new_w, ph))
else:
    new_h = int(pw / target_ratio)
    top = (ph - new_h) // 2
    photo = photo.crop((0, top, pw, top + new_h))
photo = photo.resize((W, H), Image.LANCZOS)
print(f"Cropped: {photo.size}")

# Full background image
poster = photo.copy()

# Add subtle dark overlay at bottom for readability (bottom 60%)
overlay = Image.new('RGB', (W, H), (0, 0, 0))
od = ImageDraw.Draw(overlay)
# Gradient: transparent at top, dark at bottom
for y in range(H):
    if y > H * 0.3:  # only apply gradient in bottom 70%
        ratio = (y - H * 0.3) / (H * 0.7)
        alpha = int(180 * ratio)  # max 180/255 ≈ 70% dark
        od.line([(0,y),(W,y)], fill=(0, 0, 0))

# Blend overlay onto photo (multiply-like effect)
for y in range(H):
    if y > H * 0.3:
        ratio = (y - H * 0.3) / (H * 0.7)
        darken = 1.0 - 0.55 * ratio
        for x in range(W):
            r, g, b = poster.getpixel((x, y))
            poster.putpixel((x, y), (
                int(r * darken),
                int(g * darken),
                int(b * darken)
            ))

d = ImageDraw.Draw(poster)

def fnt(size):
    for p in ['C:/Windows/Fonts/msyh.ttc','C:/Windows/Fonts/simhei.ttf']:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

# === 顶部区域（明亮，轻覆盖）===
# 半透明白色顶栏
top_bar = Image.new('RGBA', (W, 120), (255, 255, 255, 0))
poster.paste(top_bar, (0, 0), top_bar)

# 日期（左上）
d.text((55, 55), '2026.05.12', font=fnt(24), fill=(220, 220, 225))

# 右上标签
label = '乐城视角'
lbbox = d.textbbox((0,0), label, font=fnt(18))
lw = lbbox[2]-lbbox[0]
d.rectangle([(W-55-lw-20,50),(W-55,78)], fill=(210,50,30))
d.text((W-55-lw-12,52), label, font=fnt(18), fill=(255,255,255))

# === 中部大字区（大量留白）===
y = 180

# 超大数字
main = '480'
mbbox = d.textbbox((0,0), main, font=fnt(220))
mw = mbbox[2]-mbbox[0]
# 添加白色文字阴影增强可读性
d.text(((W-mw)//2 - 2, y), main, font=fnt(220), fill=(0,0,0))
d.text(((W-mw)//2 + 2, y), main, font=fnt(220), fill=(0,0,0))
d.text(((W-mw)//2, y), main, font=fnt(220), fill=(255,255,255))

unit = '万'
ubbox = d.textbbox((0,0), unit, font=fnt(65))
uw = ubbox[2]-ubbox[0]
d.text(((W-uw)//2 + mw//2 + 5, y + 40), unit, font=fnt(65), fill=(200,200,210))

sub = '中国人每年新发癌症'
sbbox = d.textbbox((0,0), sub, font=fnt(36))
sw = sbbox[2]-sbbox[0]
d.text(((W-sw)//2, y + 240), sub, font=fnt(36), fill=(230,230,235))

# === 精算师视角（半透明灰底+白字）===
y2 = y + 360

# 半透明灰底
rect_h = 430
rect_top = y2 - 20
alpha = 120
rect_img = Image.new('RGBA', (W - 100, rect_h), (15, 15, 20, alpha))
poster.paste(rect_img, (50, rect_top), rect_img)
rd = ImageDraw.Draw(poster)

# 精算师标签
rd.text((75, rect_top + 15), '精算师视角', font=fnt(24), fill=(210,50,30))

# 核心观点
y3 = rect_top + 55
pts = [
    ('其中不到30%','能用上新药'),
    ('原因一：海外新药国内未批',),
    ('原因二：普通家庭无力承担',),
    ('结果：等不起，也用不起',),
]
for pt in pts:
    if len(pt) == 2:
        rd.text((75, y3), pt[0], font=fnt(40), fill=(255,255,255))
        y3 += 55
        rd.text((75, y3), pt[1], font=fnt(40), fill=(255,255,255))
    else:
        rd.text((75, y3), pt[0], font=fnt(30), fill=(160,160,175))
    y3 += 65

# === 底部签名 ===
sig_h = 180
sig_img = Image.new('RGBA', (W, sig_h), (0, 0, 0, 160))
poster.paste(sig_img, (0, H - sig_h))

d2 = ImageDraw.Draw(poster)

q1 = '健康的人'
q2 = '不算账'
d2.text((75, H-140), q1, font=fnt(48), fill=(200,200,210))
d2.text((75+300, H-140), q2, font=fnt(48), fill=(210,50,30))

d2.text((75, H-75), '刘一｜精算师聊健康', font=fnt(26), fill=(140,140,150))
d2.text((75, H-40), '海南博鳌乐城先行区', font=fnt(20), fill=(90,90,100))

ds = '2026.05.12'
dbbox = d2.textbbox((0,0), ds, font=fnt(20))
dw = dbbox[2]-dbbox[0]
d2.text((W-75-dw, H-40), ds, font=fnt(20), fill=(90,90,100))

out = r'C:\Users\Administrator\Downloads\daily_news_poster_v9.png'
poster.save(out, quality=95)
print(f'Done: {os.path.getsize(out)//1024}KB')
img2 = Image.open(out)
print(f'Final: {img2.size}')
