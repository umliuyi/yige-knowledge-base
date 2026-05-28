# -*- coding: utf-8 -*-
"""早报封面 V5 - 科技感风格"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920

C_DARK = (5, 15, 35)
C_MID = (15, 30, 70)
C_ACCENT = (50, 100, 180)
C_WHITE = (255, 255, 255)
C_GRAY = (180, 180, 200)
C_GLOW = (100, 150, 255)

def make_bg():
    img = Image.new("RGB", (W, H), C_DARK)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(5 + (15-5)*t + (50-15)*t*0.3)
        g = int(15 + (30-15)*t + (100-30)*t*0.3)
        b = int(35 + (70-35)*t + (180-35)*t*0.4)
        if r > 255: r = 255
        if g > 255: g = 255
        if b > 255: b = 255
        d.line([(0,y),(W,y)], fill=(r,g,b))
    return img

def glow_dot(draw, cx, cy, r, col):
    # outer glow
    for i in range(r+15, r, -1):
        alpha = 0.3 + 0.7*(r+15-i)/(15)
        rr = int(col[0]*alpha) if col[0]*alpha < 255 else 255
        gg = int(col[1]*alpha) if col[1]*alpha < 255 else 255
        bb = int(col[2]*alpha) if col[2]*alpha < 255 else 255
        draw.ellipse([cx-i,cy-i,cx+i,cy+i], fill=(rr,gg,bb))
    draw.ellipse([cx-r,cy-r,cx+r,cy+r], fill=col)
    # highlight
    hr = max(2, r//3)
    draw.ellipse([cx-hr//2,cy-hr//2,cx+hr//2,cy+hr//2], fill=(200,220,255))

def draw_mol(draw, cx, cy, sc=1.0):
    r = int(10*sc)
    glow_dot(draw, cx, cy, r, C_GLOW)
    bonds = [
        (cx, cy-int(70*sc)),
        (cx+int(61*sc), cy-int(35*sc)),
        (cx+int(61*sc), cy+int(35*sc)),
        (cx, cy+int(70*sc)),
        (cx-int(61*sc), cy+int(35*sc)),
        (cx-int(61*sc), cy-int(35*sc)),
    ]
    for bx, by in bonds:
        draw.line([cx,cy,bx,by], fill=(80,120,200), width=2)
        glow_dot(draw, bx, by, int(6*sc), (150,180,255))

def font(sz):
    for p in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttc"]:
        try:
            return ImageFont.truetype(p, sz)
        except:
            pass
    return ImageFont.load_default()

def cntr(draw, txt, f, y, c):
    bb = draw.textbbox((0,0), txt, font=f)
    w = bb[2]-bb[0]
    x = (W-w)//2
    draw.text((x,y), txt, font=f, fill=c)

def logo():
    try:
        l = Image.open(r"C:\Users\Administrator\.openclaw-autoclaw\workspace\logo_main.jpg").convert("RGBA")
        ratio = l.size[1]/l.size[0]
        l = l.resize((100, int(100*ratio)), Image.LANCZOS)
        return l
    except:
        return None

def page_cover(title, sub, date_str):
    img = make_bg()
    d = ImageDraw.Draw(img)
    # molecule decor
    draw_mol(d, W-180, 280, 1.8)
    draw_mol(d, 150, H-380, 1.2)
    draw_mol(d, W-80, H-180, 0.9)
    draw_mol(d, W//2, 80, 0.7)
    # top line
    d.rectangle([60,50,W-60,54], fill=(100,150,255))
    # date tag
    d.rounded_rectangle([60,60,230,108], radius=12, fill=(30,60,130))
    d.text((80,72), date_str, font=font(24), fill=(150,180,220))
    # title
    tf = font(80)
    if len(title) > 8:
        mid = len(title)//2
        for i in range(mid, len(title)):
            if title[i] == " ":
                l1, l2 = title[:i], title[i+1:]
                break
        else:
            l1, l2 = title[:mid], title[mid:]
    else:
        l1, l2 = title, ""
    cntr(d, l1, tf, 480, C_WHITE)
    if l2:
        cntr(d, l2, tf, 590, C_WHITE)
    if sub:
        cntr(d, sub, font(32), 740, C_GRAY)
    # bottom bar
    d.rectangle([0,H-165,W,H-161], fill=(30,60,120))
    d.rectangle([0,H-161,W,H], fill=(10,25,55))
    lk = logo()
    if lk:
        img.paste(lk, (60,H-128), lk)
    d.text((180,H-112), "首位健康", font=font(28), fill=C_WHITE)
    d.text((180,H-78), "HEALTH SCIENCE", font=font(16), fill=(100,130,180))
    d.text((60,H-62), "刘一｜精算师聊健康", font=font(20), fill=C_GRAY)
    return img

def page_content(title, body, pg, total):
    img = make_bg()
    d = ImageDraw.Draw(img)
    draw_mol(d, W-80, 100, 0.8)
    draw_mol(d, 100, H-130, 0.7)
    d.text((60,50), f"{pg} / {total}", font=font(24), fill=(100,150,255))
    d.rectangle([60,108,W-60,112], fill=(80,120,200))
    tf = font(52)
    if len(title) > 16:
        mid = len(title)//2
        for i in range(mid, len(title)):
            if title[i] == " ":
                l1, l2 = title[:i], title[i+1:]
                break
        else:
            l1, l2 = title[:mid], title[mid:]
    else:
        l1, l2 = title, ""
    cntr(d, l1, tf, 240, C_WHITE)
    if l2:
        cntr(d, l2, tf, 318, C_WHITE)
    cf = font(28)
    words = body
    lines = []
    while len(words) > 18:
        cut = 18
        for j in range(18, len(words)):
            if words[j] == " ":
                cut = j
                break
        lines.append(words[:cut])
        words = words[cut+1:]
    lines.append(words)
    y = 480
    for line in lines[:6]:
        cntr(d, line, cf, y, C_GRAY)
        y += 48
    d.rectangle([0,H-100,W,H-96], fill=(30,60,120))
    d.text((60,H-70), "刘一｜精算师聊健康", font=font(24), fill=C_WHITE)
    return img

if __name__ == "__main__":
    out = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\covers_v5"
    os.makedirs(out, exist_ok=True)
    img = page_cover("干细胞疗法", "三大新突破", "2026.05.12")
    img.save(f"{out}/cover_v5.png", quality=95)
    print("OK cover")
    img2 = page_content("麦吉尔大学：胰岛细胞移植新设备", "绕过传统移植需先建立血供的难题，同时降低免疫排异风险。", 1, 3)
    img2.save(f"{out}/content_v5_1.png", quality=95)
    print("OK c1")
    img3 = page_content("卡罗林斯卡医学院研究新进展", "在多个干细胞系中稳定产生高质量胰岛素分泌细胞，移植后逆转糖尿病。", 2, 3)
    img3.save(f"{out}/content_v5_2.png", quality=95)
    print("OK c2")
    img4 = page_content("Sana UP421：14个月持续存活", "I型糖尿病患者接受移植后细胞仍存活，无需免疫抑制剂。", 3, 3)
    img4.save(f"{out}/content_v5_3.png", quality=95)
    print("OK c3")
    print("All done!")
