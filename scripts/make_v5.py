from PIL import Image, ImageDraw, ImageFont
import os, random

W, H = 1080, 1920

def make_poster_v5a():
    """左右分栏：左侧图区 + 右侧文字"""
    img = Image.new('RGB', (W, H), (5, 5, 7))
    d = ImageDraw.Draw(img)

    def fnt(size):
        for p in ['C:/Windows/Fonts/msyh.ttc','C:/Windows/Fonts/simhei.ttf']:
            try: return ImageFont.truetype(p,size)
            except: pass
        return ImageFont.load_default()

    # 左侧图区（深色渐变，模拟图片氛围）
    left_w = int(W * 0.45)
    for x in range(left_w):
        ratio = x / left_w
        r = int(5 + 8*ratio)
        g = int(5 + 6*ratio)
        b = int(7 + 15*ratio)
        d.line([(x,0),(x,H)], fill=(r,g,b))

    # 左侧底部渐变遮罩
    for y in range(H):
        ratio = y / H
        r = int(5*(1-ratio) + 0*ratio)
        g = int(5*(1-ratio) + 0*ratio)
        b = int(7*(1-ratio) + 0*ratio)
        d.line([(0,y),(left_w,y)], fill=(r,g,b))

    # 左侧顶部日期（图片区域内）
    d.text((40, 55), '2026.05.12', font=fnt(22), fill=(160,160,170))

    # 左侧底部小字
    d.text((40, H-90), '海南博鳌乐城', font=fnt(20), fill=(80,80,90))
    d.text((40, H-60), 'LECHENG ZONE', font=fnt(16), fill=(50,50,60))

    rx = left_w + 55

    # 右上标签
    label = '乐城视角'
    lbbox = d.textbbox((0,0), label, font=fnt(18))
    lw = lbbox[2]-lbbox[0]
    d.rectangle([(W-55-lw-20,50),(W-55,78)], fill=(220,50,30))
    d.text((W-55-lw-12,52), label, font=fnt(18), fill=(255,255,255))

    # 线
    d.rectangle([(rx,112),(W-55,113)], fill=(25,25,30))

    # 主标题
    y = 155
    main = '480'
    mbbox = d.textbbox((0,0), main, font=fnt(200))
    mw = mbbox[2]-mbbox[0]
    d.text((rx, y), main, font=fnt(200), fill=(255,255,255))

    unit = '万'
    d.text((rx+mw+8, y+120), unit, font=fnt(58), fill=(180,180,195))

    sub = '中国人每年新发癌症'
    d.text((rx, y+278), sub, font=fnt(34), fill=(115,115,130))

    d.rectangle([(rx,y+338),(W-55,y+339)], fill=(28,28,32))

    # 精算师视角
    y2 = y+378
    d.text((rx, y2), '精算师视角', font=fnt(24), fill=(220,50,30))
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

    # 底部
    d.rectangle([(rx,H-210),(W-55,H-208)], fill=(25,25,30))

    q1 = '健康的人'
    q2 = '不算账'
    d.text((rx, H-168), q1, font=fnt(44), fill=(165,165,180))
    d.text((rx+270, H-168), q2, font=fnt(44), fill=(220,50,30))

    d.text((rx, H-108), '刘一｜精算师聊健康', font=fnt(22), fill=(70,70,82))
    d.text((rx, H-72), '海南博鳌乐城先行区', font=fnt(18), fill=(50,50,60))

    ds = '2026.05.12'
    dbbox = d.textbbox((0,0), ds, font=fnt(18))
    dw = dbbox[2]-dbbox[0]
    d.text((W-55-dw, H-72), ds, font=fnt(18), fill=(50,50,60))

    out = r'C:\Users\Administrator\Downloads\daily_news_poster_v5a.png'
    img.save(out, quality=95)
    print('v5a done:', os.path.getsize(out)//1024,'KB')
    return out

def make_poster_v5b():
    """全屏纯文字，极简风格，参考图3"""
    img = Image.new('RGB', (W, H), (8, 8, 12))
    d = ImageDraw.Draw(img)

    def fnt(size):
        for p in ['C:/Windows/Fonts/msyh.ttc','C:/Windows/Fonts/simhei.ttf']:
            try: return ImageFont.truetype(p,size)
            except: pass
        return ImageFont.load_default()

    # 顶部区域
    d.text((60, 60), '2026.05.12', font=fnt(22), fill=(70,70,80))

    # 右上标签
    label = '乐城视角'
    lbbox = d.textbbox((0,0), label, font=fnt(16))
    lw = lbbox[2]-lbbox[0]
    d.rectangle([(W-55-lw-18,54),(W-55,78)], fill=(200,50,30))
    d.text((W-55-lw-10,56), label, font=fnt(16), fill=(255,255,255))

    d.rectangle([(60,105),(W-60,106)], fill=(25,25,32))

    # 大量留白的中部
    # 主标题
    y = 220
    main = '480万'
    mbbox = d.textbbox((0,0), main, font=fnt(180))
    mw = mbbox[2]-mbbox[0]
    d.text(((W-mw)//2, y), main, font=fnt(180), fill=(255,255,255))

    sub = '中国每年新发癌症患者'
    sbbox = d.textbbox((0,0), sub, font=fnt(30))
    sw = sbbox[2]-sbbox[0]
    d.text(((W-sw)//2, y+195), sub, font=fnt(30), fill=(100,100,115))

    # 精算视角（居中）
    d.rectangle([(60,y+280),(W-60,y+281)], fill=(22,22,28))

    pts = [
        '精算师视角',
        '',
        '其中不到30%能用上新药',
        '',
        '原因一：海外新药国内尚未批准',
        '原因二：普通家庭难以承担费用',
        '',
        '大多数人等不起，也用不起',
    ]
    y2 = y+320
    for pt in pts:
        if pt == '精算师视角':
            d.text(((W-d.textbbox((0,0),pt,font=fnt(22))[2])//2, y2), pt, font=fnt(22), fill=(200,50,30))
        elif pt == '':
            pass
        else:
            tbbox = d.textbbox((0,0), pt, font=fnt(28))
            tw = tbbox[2]-tbbox[0]
            d.text(((W-tw)//2, y2), pt, font=fnt(28), fill=(110,110,125))
        y2 += 42 if pt else 20

    # 底部
    d.rectangle([(60,H-200),(W-60,H-198)], fill=(22,22,28))

    q = '健康的人不算账，生病的人'
    qbbox = d.textbbox((0,0), q, font=fnt(42))
    qw = qbbox[2]-qbbox[0]
    d.text(((W-qw)//2, H-158), q, font=fnt(42), fill=(255,255,255))

    q2 = '才算'
    q2bbox = d.textbbox((0,0), q2, font=fnt(42))
    q2w = q2bbox[2]-q2bbox[0]
    d.text(((W-q2w)//2, H-108), q2, font=fnt(42), fill=(200,50,30))

    sig = '刘一｜精算师聊健康'
    sbbox = d.textbbox((0,0), sig, font=fnt(22))
    sw = sbbox[2]-sbbox[0]
    d.text(((W-sw)//2, H-60), sig, font=fnt(22), fill=(65,65,75))

    out = r'C:\Users\Administrator\Downloads\daily_news_poster_v5b.png'
    img.save(out, quality=95)
    print('v5b done:', os.path.getsize(out)//1024,'KB')
    return out

def make_poster_v5c():
    """全屏深色，大数字+红色强调，参考图4"""
    img = Image.new('RGB', (W, H), (4, 4, 6))
    d = ImageDraw.Draw(img)

    def fnt(size):
        for p in ['C:/Windows/Fonts/msyh.ttc','C:/Windows/Fonts/simhei.ttf']:
            try: return ImageFont.truetype(p,size)
            except: pass
        return ImageFont.load_default()

    # 左上角日期
    d.text((55, 50), '2026.05.12', font=fnt(22), fill=(70,70,82))

    # 右上标签
    label = '乐城视角'
    lbbox = d.textbbox((0,0), label, font=fnt(18))
    lw = lbbox[2]-lbbox[0]
    d.rectangle([(W-55-lw-20,45),(W-55,75)], fill=(210,50,30))
    d.text((W-55-lw-12,47), label, font=fnt(18), fill=(255,255,255))

    d.rectangle([(55,100),(W-55,101)], fill=(22,22,28))

    # 主数字
    y = 145
    main = '480'
    mbbox = d.textbbox((0,0), main, font=fnt(240))
    mw = mbbox[2]-mbbox[0]
    d.text((55, y), main, font=fnt(240), fill=(255,255,255))

    unit = '万'
    d.text((55+mw+8, y+60), unit, font=fnt(72), fill=(200,200,215))

    sub = '中国人每年新发癌症'
    d.text((55, y+300), sub, font=fnt(36), fill=(110,110,125))

    d.rectangle([(55,y+375),(W-55,y+376)], fill=(28,28,35))

    # 精算师视角
    y2 = y+415
    d.text((55, y2), '精算师视角', font=fnt(26), fill=(210,50,30))
    y3 = y2+50

    pts = [
        ('其中不到30%','能用上新药'),
        ('原因一：海外新药国内未批',),
        ('原因二：普通家庭无力承担',),
        ('结果：等不起，也用不起',),
    ]
    for pt in pts:
        if len(pt) == 2:
            d.text((55, y3), pt[0], font=fnt(42), fill=(255,255,255))
            y3 += 56
            d.text((55, y3), pt[1], font=fnt(42), fill=(255,255,255))
        else:
            d.text((55, y3), pt[0], font=fnt(30), fill=(105,105,120))
        y3 += 65

    # 底部
    d.rectangle([(55,H-200),(W-55,H-198)], fill=(22,22,28))

    q1 = '健康的人'
    q2 = '不算账'
    d.text((55, H-158), q1, font=fnt(48), fill=(160,160,175))
    d.text((55+270, H-158), q2, font=fnt(48), fill=(210,50,30))

    d.text((55, H-95), '刘一｜精算师聊健康', font=fnt(24), fill=(68,68,80))
    d.text((55, H-62), '海南博鳌乐城先行区', font=fnt(20), fill=(48,48,58))

    ds = '2026.05.12'
    dbbox = d.textbbox((0,0), ds, font=fnt(20))
    dw = dbbox[2]-dbbox[0]
    d.text((W-55-dw, H-62), ds, font=fnt(20), fill=(48,48,58))

    out = r'C:\Users\Administrator\Downloads\daily_news_poster_v5c.png'
    img.save(out, quality=95)
    print('v5c done:', os.path.getsize(out)//1024,'KB')
    return out

make_poster_v5a()
make_poster_v5b()
make_poster_v5c()
print('All done')
