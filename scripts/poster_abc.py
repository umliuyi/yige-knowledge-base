"""
三风格对比图
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920

def fnt(size):
    for p in ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def t(draw, xy, text, font, fill):
    draw.text(xy, text, font=font, fill=fill)

def make_a():
    """A: 纯白底+深黑字+橙色点缀"""
    bg = Image.new('RGB', (W, H), (250, 250, 248))
    d = ImageDraw.Draw(bg)
    t(d, (50, 50), '─'*27, fnt(10), (220, 80, 40))
    t(d, (50, 70), '2026.05.14', fnt(22), (160, 160, 165))
    t(d, (W-180, 68), '乐城视角', fnt(18), (255, 255, 255))
    t(d, (W-175, 70), '乐城视角', fnt(18), (255, 255, 255))
    nbbox = d.textbbox((0, 0), '480', font=fnt(240))
    nw = nbbox[2] - nbbox[0]
    cx = (W - nw) // 2
    t(d, (cx, 190), '480', fnt(240), (25, 25, 28))
    ub = d.textbbox((0, 0), '万', font=fnt(80))
    uw = ub[2] - ub[0]
    t(d, (cx+nw+5, 220), '万', fnt(80), (80, 80, 85))
    sub = '中国人每年新发癌症'
    sbbox = d.textbbox((0, 0), sub, font=fnt(34))
    sw = sbbox[2] - sbbox[0]
    t(d, ((W-sw)//2, 490), sub, fnt(34), (100, 100, 105))
    t(d, (80, 560), '─'*27, fnt(10), (220, 220, 225))
    t(d, (80, 590), '精算师视角', fnt(26), (230, 80, 40))
    pts = [('其中不到30%','能用上新药'), ('原因一：海外新药国内未批',), ('原因二：普通家庭无力承担',), ('结果：等不起，也用不起',)]
    y = 640
    for pt in pts:
        if len(pt) == 2:
            t(d, (80, y), pt[0], fnt(36), (30, 30, 32))
            t(d, (80, y+46), pt[1], fnt(36), (30, 30, 32))
        else:
            t(d, (80, y), pt[0], fnt(28), (100, 100, 105))
        y += 58
    t(d, (80, H-195), '─'*27, fnt(10), (220, 220, 225))
    t(d, (80, H-160), '健康的人', fnt(44), (25, 25, 28))
    t(d, (80+310, H-160), '不算账', fnt(44), (230, 80, 40))
    t(d, (80, H-95), '刘一｜精算师聊健康', fnt(22), (120, 120, 125))
    t(d, (80, H-60), '海南博鳌乐城先行区', fnt(18), (150, 150, 155))
    bg.save(r'C:\Users\Administrator\Downloads\daily_A_white.png', quality=93)
    print('A done')

def make_b():
    """B: 暖金棕渐变+奶白字"""
    bg = Image.new('RGB', (W, H), (18, 10, 4))
    d = ImageDraw.Draw(bg)
    for y2 in range(H):
        r = min(255, int(18 + y2 * 0.09))
        g = min(255, int(10 + y2 * 0.04))
        b2 = min(255, int(4 + y2 * 0.01))
        d.line([(0, y2), (W, y2)], fill=(r, g, b2))
    t(d, (50, 55), '2026.05.14', fnt(22), (200, 175, 130))
    t(d, (W-180, 53), '乐城视角', fnt(18), (255, 255, 255))
    nbbox = d.textbbox((0, 0), '480', font=fnt(240))
    nw = nbbox[2] - nbbox[0]
    cx = (W - nw) // 2
    t(d, (cx, 170), '480', fnt(240), (255, 238, 195))
    ub = d.textbbox((0, 0), '万', font=fnt(72))
    uw = ub[2] - ub[0]
    t(d, (cx+nw+5, 200), '万', fnt(72), (195, 175, 145))
    sub = '中国人每年新发癌症'
    sbbox = d.textbbox((0, 0), sub, font=fnt(34))
    sw = sbbox[2] - sbbox[0]
    t(d, ((W-sw)//2, 460), sub, fnt(34), (195, 175, 140))
    t(d, (W//4, 530), '─'*20, fnt(10), (230, 80, 40))
    t(d, (W//4, 560), '精算师视角', fnt(26), (230, 80, 40))
    pts = [('其中不到30%','能用上新药'), ('原因一：海外新药国内未批',), ('原因二：普通家庭无力承担',), ('结果：等不起，也用不起',)]
    y = 610
    for pt in pts:
        if len(pt) == 2:
            t(d, (W//4, y), pt[0], fnt(36), (255, 238, 200))
            t(d, (W//4, y+48), pt[1], fnt(36), (255, 238, 200))
        else:
            t(d, (W//4, y), pt[0], fnt(28), (155, 145, 120))
        y += 58
    t(d, (W//4, H-185), '─'*20, fnt(10), (230, 80, 40))
    t(d, (W//4, H-150), '健康的人', fnt(44), (255, 238, 195))
    t(d, (W//4+360, H-150), '不算账', fnt(44), (230, 80, 40))
    t(d, (W//4, H-85), '刘一｜精算师聊健康', fnt(22), (145, 135, 115))
    t(d, (W//4, H-50), '海南博鳌乐城先行区', fnt(18), (115, 105, 85))
    bg.save(r'C:\Users\Administrator\Downloads\daily_B_warm.png', quality=93)
    print('B done')

def make_c():
    """C: 冷蓝+深蓝+冰白字"""
    bg = Image.new('RGB', (W, H), (8, 14, 28))
    d = ImageDraw.Draw(bg)
    for y2 in range(H):
        r = int(8 + y2 * 0.003)
        g = int(14 + y2 * 0.006)
        b2 = int(28 + y2 * 0.012)
        d.line([(0, y2), (W, y2)], fill=(min(255,r), min(255,g), min(255,b2)))
    t(d, (50, 55), '2026.05.14', fnt(22), (130, 155, 190))
    t(d, (W-180, 53), '乐城视角', fnt(18), (255, 255, 255))
    nbbox = d.textbbox((0, 0), '480', font=fnt(240))
    nw = nbbox[2] - nbbox[0]
    cx = (W - nw) // 2
    t(d, (cx, 170), '480', fnt(240), (225, 240, 255))
    ub = d.textbbox((0, 0), '万', font=fnt(72))
    uw = ub[2] - ub[0]
    t(d, (cx+nw+5, 200), '万', fnt(72), (140, 175, 205))
    sub = '中国人每年新发癌症'
    sbbox = d.textbbox((0, 0), sub, font=fnt(34))
    sw = sbbox[2] - sbbox[0]
    t(d, ((W-sw)//2, 460), sub, fnt(34), (150, 180, 210))
    t(d, (W//4, 530), '─'*20, fnt(10), (55, 135, 215))
    t(d, (W//4, 560), '精算师视角', fnt(26), (55, 155, 235))
    pts = [('其中不到30%','能用上新药'), ('原因一：海外新药国内未批',), ('原因二：普通家庭无力承担',), ('结果：等不起，也用不起',)]
    y = 610
    for pt in pts:
        if len(pt) == 2:
            t(d, (W//4, y), pt[0], fnt(36), (205, 225, 248))
            t(d, (W//4, y+48), pt[1], fnt(36), (205, 225, 248))
        else:
            t(d, (W//4, y), pt[0], fnt(28), (105, 135, 165))
        y += 58
    t(d, (W//4, H-185), '─'*20, fnt(10), (55, 135, 215))
    t(d, (W//4, H-150), '健康的人', fnt(44), (195, 220, 248))
    t(d, (W//4+360, H-150), '不算账', fnt(44), (55, 155, 235))
    t(d, (W//4, H-85), '刘一｜精算师聊健康', fnt(22), (95, 125, 155))
    t(d, (W//4, H-50), '海南博鳌乐城先行区', fnt(18), (75, 100, 125))
    bg.save(r'C:\Users\Administrator\Downloads\daily_C_cool.png', quality=93)
    print('C done')

make_a()
make_b()
make_c()
print('All done')
