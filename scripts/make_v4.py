from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920
img = Image.new('RGB', (W, H), (5, 5, 7))
d = ImageDraw.Draw(img)

def fnt(size):
    for p in ['C:/Windows/Fonts/msyh.ttc','C:/Windows/Fonts/simhei.ttf']:
        try: return ImageFont.truetype(p,size)
        except: pass
    return ImageFont.load_default()

# Left side: image area placeholder
left_w = int(W * 0.42)
d.rectangle([(0, 0),(left_w, H)], fill=(8, 8, 10))

rx = left_w + 40

# Date
d.text((rx, 55), '2026.05.12', font=fnt(24), fill=(80, 80, 90))

# Label
label = '乐城视角'
lbbox = d.textbbox((0,0), label, font=fnt(18))
lw = lbbox[2]-lbbox[0]
d.rectangle([(W-55-lw-20, 50),(W-55,78)], fill=(220,50,30))
d.text((W-55-lw-12, 52), label, font=fnt(18), fill=(255,255,255))

# Line
d.rectangle([(rx,110),(W-55,111)], fill=(25,25,30))

# Main number
y = 150
main = '480'
mbbox = d.textbbox((0,0), main, font=fnt(200))
mw = mbbox[2]-mbbox[0]
d.text((rx, y), main, font=fnt(200), fill=(255,255,255))

unit = '万'
ubbox = d.textbbox((0,0), unit, font=fnt(60))
d.text((rx+mw+5, y+120), unit, font=fnt(60), fill=(200,200,210))

sub = '中国人每年新发癌症'
d.text((rx, y+270), sub, font=fnt(34), fill=(120,120,135))

d.rectangle([(rx,y+330),(W-55,y+331)], fill=(30,30,35))

# Actuary perspective
y2 = y+370
d.text((rx, y2), '精算师视角', font=fnt(26), fill=(220,60,30))
y3 = y2+45

pts = [
    ('其中不到30%','能用上新药'),
    ('原因一：海外新药国内未批',),
    ('原因二：普通家庭无力承担',),
    ('结果：大多数人等不起，也用不起',),
]
for pt in pts:
    if len(pt) == 2:
        d.text((rx, y3), pt[0], font=fnt(40), fill=(255,255,255))
        y3 += 55
        d.text((rx, y3), pt[1], font=fnt(40), fill=(255,255,255))
    else:
        d.text((rx, y3), pt[0], font=fnt(32), fill=(110,110,125))
    y3 += 62

# Bottom
d.rectangle([(rx,H-220),(W-55,H-218)], fill=(25,25,30))

q1 = '健康的人'
q2 = '不算账'
d.text((rx, H-180), q1, font=fnt(46), fill=(180,180,195))
bbox2 = d.textbbox((0,0), q2, font=fnt(46))
w2 = bbox2[2]-bbox2[0]
d.text((rx+300, H-180), q2, font=fnt(46), fill=(220,60,30))

d.text((rx, H-120), '刘一｜精算师聊健康', font=fnt(24), fill=(75,75,85))
d.text((rx, H-80), '海南博鳌乐城先行区', font=fnt(20), fill=(55,55,65))

ds = '2026.05.12'
dbbox = d.textbbox((0,0), ds, font=fnt(20))
dw = dbbox[2]-dbbox[0]
d.text((W-55-dw, H-80), ds, font=fnt(20), fill=(55,55,65))

out = r'C:\Users\Administrator\Downloads\daily_news_poster_v4.png'
img.save(out, quality=95)
print('Done:', os.path.getsize(out)//1024, 'KB')
