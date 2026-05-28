from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1080, 1920

# Load the photo
photo = Image.open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\photo.jpg')
# photo is 1080x1920, use it as left side

# Create poster: left side = photo, right side = text on dark bg
poster = Image.new('RGB', (W, H), (5, 5, 7))
draw = ImageDraw.Draw(poster)

def fnt(size):
    for p in ['C:/Windows/Fonts/msyh.ttc','C:/Windows/Fonts/simhei.ttf']:
        try: return ImageFont.truetype(p,size)
        except: pass
    return ImageFont.load_default()

# === Left side: photo (left 42%) ===
left_w = int(W * 0.42)

# Resize photo to fill left side
photo_resized = photo.resize((left_w, H), Image.LANCZOS)
# Add dark overlay to make text readable when overlaid
overlay = Image.new('RGB', (left_w, H), (0, 0, 0))
poster.paste(photo_resized, (0, 0))

# Add subtle dark gradient overlay on left photo
for x in range(left_w):
    alpha = int(40 * (left_w - x) / left_w)
    draw.line([(x,0),(x,H)], fill=(0,0,0))

# === Right side text ===
rx = left_w + 55

# Date (top right of text area)
draw.text((rx, 55), '2026.05.12', font=fnt(24), fill=(80, 80, 90))

# Label
label = '乐城视角'
lbbox = draw.textbbox((0,0), label, font=fnt(18))
lw = lbbox[2]-lbbox[0]
draw.rectangle([(W-55-lw-20,50),(W-55,78)], fill=(210,50,30))
draw.text((W-55-lw-12,52), label, font=fnt(18), fill=(255,255,255))

# Line
draw.rectangle([(rx,112),(W-55,113)], fill=(25,25,30))

# Main number
y = 155
main = '480'
mbbox = draw.textbbox((0,0), main, font=fnt(200))
mw = mbbox[2]-mbbox[0]
draw.text((rx, y), main, font=fnt(200), fill=(255,255,255))

unit = '万'
ubbox = draw.textbbox((0,0), unit, font=fnt(58))
uw = ubbox[2]-ubbox[0]
draw.text((rx+mw+8, y+120), unit, font=fnt(58), fill=(180,180,195))

sub = '中国人每年新发癌症'
draw.text((rx, y+278), sub, font=fnt(34), fill=(115,115,130))

draw.rectangle([(rx,y+338),(W-55,y+339)], fill=(28,28,32))

# Actuary
y2 = y+378
draw.text((rx, y2), '精算师视角', font=fnt(24), fill=(210,50,30))
y3 = y2+46

pts = [
    ('其中不到30%','能用上新药'),
    ('原因一：海外新药国内未批',),
    ('原因二：普通家庭无力承担',),
    ('结果：等不起，也用不起',),
]
for pt in pts:
    if len(pt) == 2:
        draw.text((rx, y3), pt[0], font=fnt(38), fill=(255,255,255))
        y3 += 52
        draw.text((rx, y3), pt[1], font=fnt(38), fill=(255,255,255))
    else:
        draw.text((rx, y3), pt[0], font=fnt(30), fill=(105,105,120))
    y3 += 60

# Bottom
draw.rectangle([(rx,H-210),(W-55,H-208)], fill=(25,25,30))

q1 = '健康的人'
q2 = '不算账'
draw.text((rx, H-168), q1, font=fnt(44), fill=(165,165,180))
draw.text((rx+270, H-168), q2, font=fnt(44), fill=(210,50,30))

draw.text((rx, H-108), '刘一｜精算师聊健康', font=fnt(22), fill=(70,70,82))
draw.text((rx, H-72), '海南博鳌乐城先行区', font=fnt(18), fill=(50,50,60))

ds = '2026.05.12'
dbbox = draw.textbbox((0,0), ds, font=fnt(18))
dw = dbbox[2]-dbbox[0]
draw.text((W-55-dw, H-72), ds, font=fnt(18), fill=(50,50,60))

out = r'C:\Users\Administrator\Downloads\daily_news_poster_v7.png'
poster.save(out, quality=95)
print('Done:', os.path.getsize(out)//1024,'KB')
