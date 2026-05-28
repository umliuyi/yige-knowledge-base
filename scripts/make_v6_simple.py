#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V6 simple - deep tech bg + glow orbs"""
from PIL import Image, ImageDraw, ImageFont
import os
import random

W, H = 1080, 1920

def bg():
    img = Image.new("RGB", (W, H), (5, 8, 25))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        if t < 0.4:
            r = int(5 + 15*t/0.4)
            g = int(8 + 7*t/0.4)
            b = int(25 + 35*t/0.4)
        elif t < 0.7:
            s = (t-0.4)/0.3
            r = int(20 - 5*s)
            g = int(15 + 10*s)
            b = int(60 + 40*s)
        else:
            s = (t-0.7)/0.3
            r = int(15 - 7*s)
            g = int(25 - 10*s)
            b = int(100 - 70*s)
        d.line([(0,y),(W,y)], fill=(max(0,min(255,r)),max(0,min(255,g)),max(0,min(255,b))))
    return img

def orb(draw, cx, cy, r, col):
    for i in range(r+40, r, -1):
        a = (40-i)/40.0
        rr = int(col[0]*a*0.5)
        gg = int(col[1]*a*0.5)
        bb = int(col[2]*a*0.5)
        draw.ellipse([cx-i,cy-i,cx+i,cy+i], fill=(rr,gg,bb))
    for i in range(r, 0, -1):
        t = i/r
        draw.ellipse([cx-i,cy-i,cx+i,cy+i], fill=(int(col[0]*t), int(col[1]*t), int(col[2]*t)))
    # highlight
    draw.ellipse([cx-r//3, cy-r//3, cx+r//3, cy+r//3], fill=(200,220,255))

def txt_font(sz):
    for p in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttc"]:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

def cntr(draw, s, f, y, c):
    bb = draw.textbbox((0,0), s, font=f)
    x = (W-(bb[2]-bb[0]))//2
    draw.text((x, y), s, font=f, fill=c)

def glass(draw, x, y, w, h, col, alpha):
    overlay = Image.new("RGBA", (w, h), (*col, alpha))
    d2 = ImageDraw.Draw(overlay)
    d2.rectangle([0,0,w-1,h-1], outline=(80,120,200,100), width=1)
    return overlay

def get_logo():
    try:
        l = Image.open(r"C:\Users\Administrator\.openclaw-autoclaw\workspace\logo_main.jpg").convert("RGBA")
        ratio = l.size[1]/l.size[0]
        l = l.resize((80, int(80*ratio)), Image.LANCZOS)
        return l
    except:
        return None

def make_cover(title, sub, date_str):
    img = bg()
    d = ImageDraw.Draw(img)
    # glow orbs - scattered
    orb(d, W//2, H//2-100, 200, (40,80,200))
    orb(d, W//2+280, H//2+200, 130, (60,120,220))
    orb(d, 120, H//2+150, 80, (30,100,180))
    orb(d, W-150, 250, 100, (50,100,200))
    orb(d, W//2-350, H//2+300, 60, (80,140,220))
    orb(d, W//2+200, H-300, 50, (60,120,220))
    # date tag
    gt = glass(d, 50,50,180,48, (20,40,100), 80)
    img.paste(gt, (50,50), gt)
    d2 = ImageDraw.Draw(img)
    d2.text((65,60), date_str, font=txt_font(22), fill=(150,180,220))
    # title
    tf = txt_font(88)
    if len(title) > 6:
        mid = len(title)//2
        l1 = title[:mid]
        l2 = title[mid:]
    else:
        l1 = title
        l2 = ""
    cntr(d, l1, tf, 450, (255,255,255))
    if l2:
        cntr(d, l2, tf, 570, (255,255,255))
    if sub:
        cntr(d, sub, txt_font(30), 720, (140,170,210))
    # bottom bar
    gt2 = glass(d, 0,H-140,W,140, (10,20,50), 100)
    img.paste(gt2, (0,H-140), gt2)
    lk = get_logo()
    if lk:
        img.paste(lk, (50,H-115), lk)
    d.text((150,H-100), "首位健康", font=txt_font(26), fill=(255,255,255))
    d.text((150,H-68), "HEALTH SCIENCE", font=txt_font(14), fill=(80,120,180))
    d.text((50,H-55), "刘一｜精算师聊健康", font=txt_font(18), fill=(120,150,190))
    return img

def make_content(title, body, pg, total):
    img = bg()
    d = ImageDraw.Draw(img)
    orb(d, W-80, 80, 50, (40,80,200))
    orb(d, 60, H-80, 40, (60,120,220))
    d.text((50,50), f"{pg} / {total}", font=txt_font(24), fill=(80,130,220))
    d.rectangle([50,108,W-50,112], fill=(60,100,180))
    tf = txt_font(54)
    if len(title) > 14:
        mid = len(title)//2
        l1 = title[:mid]
        l2 = title[mid:]
    else:
        l1 = title
        l2 = ""
    cntr(d, l1, tf, 240, (255,255,255))
    if l2:
        cntr(d, l2, tf, 320, (255,255,255))
    cf = txt_font(26)
    words = body
    lines = []
    while len(words) > 22:
        cut = 22
        for j in range(22, len(words)):
            if words[j] == " ":
                cut = j; break
        lines.append(words[:cut])
        words = words[cut+1:]
    lines.append(words)
    y = 480
    for line in lines[:5]:
        cntr(d, line, cf, y, (160,180,210))
        y += 48
    gt = glass(d, 0,H-90,W,90, (10,20,50), 80)
    img.paste(gt, (0,H-90), gt)
    d.text((50,H-60), "刘一｜精算师聊健康", font=txt_font(22), fill=(255,255,255))
    return img

if __name__ == "__main__":
    out = r"C:\Users\Administrator\.openclaw-autoclaw\media"
    os.makedirs(out, exist_ok=True)
    make_cover("干细胞疗法", "三大新突破", "2026.05.12").save(f"{out}\\v6_cover.png", quality=95)
    print("cover OK")
    make_content("麦吉尔大学：胰岛细胞移植新设备", "绕过传统移植需先建立血供的难题，同时降低免疫排异风险。", 1,3).save(f"{out}\\v6_c1.png", quality=95)
    print("c1 OK")
    make_content("卡罗林斯卡医学院研究新进展", "在多个干细胞系中稳定产生高质量胰岛素分泌细胞。", 2,3).save(f"{out}\\v6_c2.png", quality=95)
    print("c2 OK")
    make_content("Sana UP421：14个月持续存活", "I型糖尿病患者接受移植后细胞仍存活，无需免疫抑制剂。", 3,3).save(f"{out}\\v6_c3.png", quality=95)
    print("c3 OK")
    print("ALL DONE")
