#!/usr/bin/env python3
"""
早报幻灯片 v2 - 乐城视角
- 每页1条新闻，深色背景，科技感
- 1920x1080，每页停留9秒
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, sys, re, math, urllib.request

# ============ 配置 ============
SOURCE_FILE = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\日报\2026-05-11-早报-乐城视角.md"
OUTPUT_DIR  = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1920, 1080
SLIDE_DURATION = 9  # 每页停留秒数

# 配色
BG_DARK    = (6, 6, 16)
BG_BLUE    = (8, 12, 32)
ORANGE     = (255, 102, 38)
ORANGE_DIM = (200, 70, 20)
WHITE      = (255, 255, 255)
GRAY       = (130, 135, 145)
GRAY_DARK  = (60, 65, 80)
CYAN       = (0, 200, 220)
RED_ACC    = (220, 60, 60)
# ============================

def font_path(size, bold=False):
    candidates = [
        f"C:/Windows/Fonts/msyh.ttc",
        f"C:/Windows/Fonts/simhei.ttf",
        f"C:/Windows/Fonts/NotoSansCJK-Regular.ttc",
        f"C:/Windows/Fonts/arial.ttf",
    ] if not bold else [
        f"C:/Windows/Fonts/msyhbd.ttc",
        f"C:/Windows/Fonts/simhei.ttf",
        f"C:/Windows/Fonts/arialbd.ttf",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()

def download_img(url, cached_path):
    """下载图片到本地缓存"""
    if os.path.exists(cached_path):
        return cached_path
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        })
        with urllib.request.urlopen(req, timeout=10) as r, open(cached_path, 'wb') as f:
            f.write(r.read())
        return cached_path
    except Exception as e:
        print(f"    下载图片失败 {url}: {e}")
        return None

def gradient_bg(img, draw):
    """深色渐变背景"""
    w, h = img.size
    top, bot = BG_BLUE, BG_DARK
    for y in range(h):
        t = y / h
        r = int(top[0]*(1-t) + bot[0]*t)
        g = int(top[1]*(1-t) + bot[1]*t)
        b = int(top[2]*(1-t) + bot[2]*t)
        draw.line([(0,y),(w,y)], fill=(r,g,b))

def draw_grid_lines(draw, alpha=8):
    """细网格线增加科技感"""
    step = 60
    color = (30, 40, 70)
    for x in range(0, W, step):
        draw.line([(x,0),(x,H)], fill=color, width=1)
    for y in range(0, H, step):
        draw.line([(0,y),(W,y)], fill=color, width=1)

def add_top_bar(draw, color=ORANGE, h=5):
    draw.rectangle([(0,0),(W,h)], fill=color)

def add_bottom_bar(draw, color=ORANGE, h=4):
    draw.rectangle([(0,H-h),(W,H)], fill=color)

def glow_text(draw, xy, text, fill, font_obj, glow_color=None, glow_r=3):
    if glow_color:
        for dx in range(-glow_r, glow_r+1):
            for dy in range(-glow_r, glow_r+1):
                dist = math.sqrt(dx**2+dy**2)
                if dist <= glow_r:
                    alpha = int(60*(1-dist/glow_r))
                    c = tuple(max(0,min(255, glow_color[i]+alpha)) for i in range(3))
                    draw.text((xy[0]+dx, xy[1]+dy), text, font=font_obj, fill=c)
    draw.text(xy, text, font=font_obj, fill=fill)

def wrap_text(text, font_obj, max_w):
    """简单文字换行"""
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph.strip():
            lines.append('')
            continue
        words = paragraph
        current = ''
        for ch in words:
            test = current + ch
            bbox = ImageDraw.Draw(Image.new('RGB',(1,1))).textbbox((0,0), test, font=font_obj)
            if bbox[2] - bbox[0] > max_w:
                if current:
                    lines.append(current)
                current = ch
            else:
                current = test
        if current:
            lines.append(current)
    return lines

def make_bg():
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    gradient_bg(img, draw)
    draw_grid_lines(draw)
    return img, draw

# ---- 封面 ----
def make_cover():
    img, draw = make_bg()
    add_top_bar(draw, ORANGE, 6)

    # 顶部日期
    f_date = font_path(28)
    draw.text((80, 45), "2026年5月11日 星期一", font=f_date, fill=GRAY)

    # 左侧竖线装饰
    draw.rectangle([(0, 0), (5, H)], fill=ORANGE)

    # 乐城视角标签
    f_tag = font_path(30)
    draw.text((80, 120), "乐城视角 · 大健康早报", font=f_tag, fill=ORANGE)

    # 主标题
    f_title = font_path(110, bold=True)
    title = "每日早报"
    bbox = draw.textbbox((0,0), title, font=f_title)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H//2-100), title, font=f_title, fill=WHITE)

    # 副标题
    f_sub = font_path(40)
    sub = "医疗 · 政策 · 投资 · 精算"
    bbox2 = draw.textbbox((0,0), sub, font=f_sub)
    sw = bbox2[2]-bbox2[0]
    draw.text(((W-sw)//2, H//2+20), sub, font=f_sub, fill=GRAY)

    # 底部信息
    f_bot = font_path(28)
    info = "刘一 精算师  |  每早8:30更新"
    bbox3 = draw.textbbox((0,0), info, font=f_bot)
    bw = bbox3[2]-bbox3[0]
    draw.text(((W-bw)//2, H-100), info, font=f_bot, fill=GRAY_DARK)

    add_bottom_bar(draw)

    path = os.path.join(OUTPUT_DIR, "00_cover.png")
    img.save(path, quality=95)
    print(f"  [封面] {path}")
    return path

# ---- 新闻页（每条新闻单独一页，标题+内容一体化） ----
def make_news_page(num, total, tag, title, body_blocks, image_url=None):
    """
    body_blocks: list of (label, text) tuples
    """
    img, draw = make_bg()
    add_top_bar(draw, ORANGE, 5)
    draw.rectangle([(0,0),(5,H)], fill=ORANGE)

    # 页码
    f_pg = font_path(22)
    draw.text((W-110, 40), f"{num}/{total}", font=f_pg, fill=GRAY_DARK)

    # 标签
    f_tag = font_path(24)
    draw.text((80, 38), f"  {tag}", font=f_tag, fill=ORANGE)

    # 标题
    f_title = font_path(64, bold=True)
    draw.text((80, 85), title, font=f_title, fill=WHITE)

    # 标题下分隔线
    draw.rectangle([(80, 175),(W-80, 178)], fill=ORANGE)

    # 内容区
    y = 205
    for block in body_blocks:
        if len(block) == 2:
            label, text = block
            # 小标签
            f_lbl = font_path(26)
            draw.text((80, y), f"▎{label}", font=f_lbl, fill=ORANGE)
            y += 38

            # 正文（处理换行）
            f_body = font_path(32)
            lines = wrap_text(text, f_body, W - 200)
            for line in lines:
                draw.text((80, y), line, font=f_body, fill=WHITE)
                y += 52
                if y > H - 130:
                    break
            y += 15
        else:
            text = block[0]
            f_body = font_path(32)
            lines = wrap_text(text, f_body, W - 200)
            for line in lines:
                draw.text((80, y), line, font=f_body, fill=WHITE)
                y += 52
                if y > H - 130:
                    break
        if y > H - 130:
            break

    add_bottom_bar(draw)

    # 保存
    slug = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', title)[:8]
    path = os.path.join(OUTPUT_DIR, f"0{num}_{slug}.png")
    img.save(path, quality=92)
    print(f"  [新闻{num}] {path}")
    return path

# ---- 数据冲击页 ----
def make_data_page(num, total, big_num, unit, label, note):
    img, draw = make_bg()
    add_top_bar(draw, CYAN, 4)

    # 数字
    f_num = font_path(200, bold=True)
    draw.text((W//2 - 400, H//2 - 200), big_num, font=f_num, fill=ORANGE)

    # 单位
    f_unit = font_path(70)
    draw.text((W//2 + 100, H//2 - 60), unit, font=f_unit, fill=WHITE)

    # 标签
    f_lbl = font_path(38)
    bbox = draw.textbbox((0,0), label, font=f_lbl)
    lw = bbox[2]-bbox[0]
    draw.text(((W-lw)//2, H//2 + 60), label, font=f_lbl, fill=WHITE)

    # 备注
    f_note = font_path(28)
    bbox2 = draw.textbbox((0,0), note, font=f_note)
    nw = bbox2[2]-bbox2[0]
    draw.text(((W-nw)//2, H//2+130), note, font=f_note, fill=GRAY)

    # 页码
    f_pg = font_path(22)
    draw.text((W-110, H-80), f"{num}/{total}", font=f_pg, fill=GRAY_DARK)

    add_bottom_bar(draw)

    path = os.path.join(OUTPUT_DIR, f"0{num}_data.png")
    img.save(path, quality=92)
    print(f"  [数据{num}] {path}")
    return path

# ---- 结尾页 ----
def make_closing():
    img, draw = make_bg()
    draw.rectangle([(0,0),(5,H)], fill=ORANGE)

    f_main = font_path(100, bold=True)
    t1 = "感谢观看"
    bbox = draw.textbbox((0,0), t1, font=f_main)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H//2-80), t1, font=f_main, fill=WHITE)

    f_sub = font_path(40)
    t2 = "刘一  |  精算师聊健康  |  乐城视角"
    bbox2 = draw.textbbox((0,0), t2, font=f_sub)
    sw = bbox2[2]-bbox2[0]
    draw.text(((W-sw)//2, H//2+30), t2, font=f_sub, fill=ORANGE)

    f_date = font_path(28)
    t3 = "每早8:30 · 大健康资讯早知道"
    bbox3 = draw.textbbox((0,0), t3, font=f_date)
    sw3 = bbox3[2]-bbox3[0]
    draw.text(((W-sw3)//2, H//2+100), t3, font=f_date, fill=GRAY)

    add_bottom_bar(draw)

    path = os.path.join(OUTPUT_DIR, "99_closing.png")
    img.save(path, quality=95)
    print(f"  [结尾] {path}")
    return path

# ========================
# 乐城视角早报内容
# ========================
if __name__ == "__main__":
    print("=" * 50)
    print("生成乐城视角早报幻灯片 v2 ...")

    slides = []

    # 封面
    slides.append(make_cover())

    # 第1条：正大天晴×GSK乙肝新药
    slides.append(make_news_page(
        1, 5,
        "药械 · 乐城特许政策",
        "正大天晴×GSK战略合作：乙肝新药加速入华，乐城机遇几何？",
        [
            ("热点事件", "正大天晴与GSK达成战略合作，推动乙肝ASO新药bepirovirsen进入中国内地，由正大天晴负责进口分销。"),
            ("对乐城的影响", "bepirovirsen属于境外已上市、境内尚未获批的创新药，这类品种正是乐城'先行区'特许药械政策的核心适用对象。乐城真实世界数据通道可为该药提供加速审评桥梁，若乐城率先引进，患者不出国门即可用上这款乙肝重磅新药。"),
            ("精算视角", "中国约7000万乙肝感染者中，目标群体约300-500万人。按人均年治疗费用6-8万元测算，假设乐城承接1%目标患者，年新增特药收入约1.8-4亿元，净利率可达25-35%。"),
        ]
    ))

    # 第2条：化妆品电子标签
    slides.append(make_news_page(
        2, 5,
        "消费医疗 · 合规",
        "进口化妆品电子标签新规落地：海南自贸港的合规挑战与差异化机遇",
        [
            ("热点事件", "海关总署修订《进出口化妆品检验检疫监督管理办法》，上海率先试点进口化妆品电子标签，12月1日起全国施行。"),
            ("对乐城的影响", "电子标签制度意味着每件进口化妆品必须加贴可追溯的电子身份码。乐城若率先建立'先行区特供化妆品'追溯体系，联合乐城特有的医疗资质背书，可将普通跨境购升级为'医疗级消费护肤'新定位。"),
            ("精算视角", "海南离岛免税化妆品年销售额约80-120亿元，合规成本约占营收0.5-1.5%。若乐城通过'医疗级溯源'获取5-10%的中高端客群增量，对应年增收约4-12亿元，ROI显著高于普通商超渠道。"),
        ]
    ))

    # 第3条：数据页 - 7000万
    slides.append(make_data_page(
        3, 5,
        "7000万",
        "人",
        "中国乙肝病毒感染者规模",
        "bepirovirsen目标用药人群约300-500万 | 年治疗费用6-8万元"
    ))

    # 第4条：数据页 - 80-120亿
    slides.append(make_data_page(
        4, 5,
        "80-120亿",
        "元/年",
        "海南离岛免税化妆品年销售额",
        "乐城若获5-10%中高端客群增量，年增收可达4-12亿元"
    ))

    # 结尾
    slides.append(make_closing())

    print(f"\n共生成 {len(slides)} 张幻灯片")
    print(f"保存在: {OUTPUT_DIR}")
    print(f"每页停留: {SLIDE_DURATION}秒")
    print(f"预计视频时长: {len(slides) * SLIDE_DURATION}秒")
