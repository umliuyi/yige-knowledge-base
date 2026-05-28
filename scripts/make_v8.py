from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920

photo = Image.open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\photo_new.jpg')
print(f"Photo: {photo.size}")

# Crop to 9:16 portrait (center crop from middle)
pw, ph = photo.size
target_ratio = 9/16
photo_ratio = pw/ph
if photo_ratio > target_ratio:
    # Too wide, crop width
    new_w = int(ph * target_ratio)
    left = (pw - new_w) // 2
    photo = photo.crop((left, 0, left + new_w, ph))
else:
    new_h = int(pw / target_ratio)
    top = (ph - new_h) // 2
    photo = photo.crop((0, top, pw, top + new_h))

# Resize to fit poster dimensions
photo = photo.resize((W, H), Image.LANCZOS)
print(f"Cropped: {photo.size}")

poster = Image.new('RGB', (W, H), (5, 5, 7))

# === Left side: photo (42% width) ===
left_w = int(W * 0.42)
photo_left = photo.resize((left_w, H), Image.LANCZOS)
poster.paste(photo_left, (0, 0))

# === Dark gradient overlay on photo (right edge dark) ===
for x in range(left_w):
    alpha = int(70 * (left_w - x) / left_w)
    for y in range(H):
        r, g, b = poster.getpixel((x, y))
        poster.putpixel((x, y), (
            max(0, r - alpha),
            max(0, g - alpha),
            max(0, b - alpha)
        ))

d = ImageDraw.Draw(poster)

def fnt(size):
    for p in ['C:/Windows/Fonts/msyh.ttc','C:/Windows/Fonts/simhei.ttf']:
        try: return ImageFont.truetype(p,size)
        except: pass
    return ImageFont.load_default()

rx = left_w + 55

# Date
d.text((rx, 55), '2026.05.12', font=fnt(24), fill=(80, 80, 90))

# Label
label = '乐城视角'
lbbox = d.textbbox((0,0), label, font=fnt(18))
lw = lbbox[2]-lbbox[0]
d.rectangle([(W-55-lw-20,50),(W-55,78)], fill=(210,50,30))
d.text((W-55-lw-12,52), label, font=fnt(18), fill=(255,255,255))

# Line
d.rectangle([(rx,112),(W-55,113)], fill=(25,25,30))

# Main number
y = 155
main = '480'
mbbox = d.textbbox((0,0), main, font=fnt(200))
mw = mbbox[2]-mbbox[0]
d.text((rx, y), main, font=fnt(200), fill=(255,255,255))

unit = '万'
ubbox = d.textbbox((0,0), unit, font=fnt(58))
uw = ubbox[2]-ubbox[0]
d.text((rx+mw+8, y+120), unit, font=fnt(58), fill=(180,180,195))

sub = '中国人每年新发癌症'
d.text((rx, y+278), sub, font=fnt(34), fill=(115,115,130))

d.rectangle([(rx,y+338),(W-55,y+339)], fill=(28,28,32))

# Actuary
y2 = y+378
d.text((rx, y2), '精算师视角', font=fnt(24), fill=(210,50,30))
y3 = y2+46

pts = [
    ('其中不到30%','能用上新药'),
    ('原因一：海外新药国内未批',),
    ('原因二：普通家庭无力承担',),
    ('结果：等不起，也用不起',),
]
for pt in pts:
    if len(pt) == 2:
        d.text((rx, y3), pt[0], font=fnt(38), fill=(255,255,255))
        y3 += 52
        d.text((rx, y3), pt[1], font=fnt(38), fill=(255,255,255))
    else:
        d.text((rx, y3), pt[0], font=fnt(30), fill=(105,105,120))
    y3 += 60

# Bottom
d.rectangle([(rx,H-210),(W-55,H-208)], fill=(25,25,30))

q1 = '健康的人'
q2 = '不算账'
d.text((rx, H-168), q1, font=fnt(44), fill=(165,165,180))
d.text((rx+270, H-168), q2, font=fnt(44), fill=(210,50,30))

d.text((rx, H-108), '刘一｜精算师聊健康', font=fnt(22), fill=(70,70,82))
d.text((rx, H-72), '海南博鳌乐城先行区', font=fnt(18), fill=(50,50,60))

ds = '2026.05.12'
dbbox = d.textbbox((0,0), ds, font=fnt(18))
dw = dbbox[2]-dbbox[0]
d.text((W-55-dw, H-72), ds, font=fnt(18), fill=(50,50,60))

out = r'C:\Users\Administrator\Downloads\daily_news_poster_v8.png'
poster.save(out, quality=95)
print(f'Done: {os.path.getsize(out)//1024}KB')
from PIL import Image as I
img = I.open(out)
print(f'Final: {img.size}')
