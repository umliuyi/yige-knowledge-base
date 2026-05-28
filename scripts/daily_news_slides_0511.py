# -*- coding: utf-8 -*-
"""
早报内容 → 幻灯片视频
生成 2026-05-11 早报幻灯片
"""
from PIL import Image, ImageDraw, ImageFont
import os, re

OUTPUT_DIR = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1920, 1080

BG      = (8, 8, 18)
ORANGE  = (255, 87, 34)
CYAN    = (0, 188, 212)
WHITE   = (255, 255, 255)
GRAY    = (160, 160, 170)
DARK    = (30, 30, 50)

def font(size, bold=False):
    for p in [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

def gradient_bg(img, draw):
    w, h = img.size
    top, bot = (12, 12, 30), (4, 4, 12)
    for y in range(h):
        r = int(top[0]*(1-y/h) + bot[0]*y/h)
        g = int(top[1]*(1-y/h) + bot[1]*y/h)
        b = int(top[2]*(1-y/h) + bot[2]*y/h)
        draw.line([(0,y),(w,y)], fill=(r,g,b))

def add_left_bar(draw, color=ORANGE, width=6):
    draw.rectangle([(0,0),(width, H)], fill=color)

def add_bottom_line(draw, color=CYAN):
    draw.rectangle([(0, H-5), (W, H)], fill=color)

def add_page_num(draw, num, total):
    txt = f"{num}/{total}"
    f = font(22)
    draw.text((W-100, H-70), txt, font=f, fill=GRAY)

def make_cover():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient_bg(img, draw)

    draw.rectangle([(0,0),(W,8)], fill=ORANGE)

    f_date = font(32)
    draw.text((80, 60), "2026年5月11日 星期一", font=f_date, fill=GRAY)

    f_title = font(96, bold=True)
    title = "大健康早报"
    bbox = draw.textbbox((0,0), title, font=f_title)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H//2-160), title, font=f_title, fill=WHITE)

    f_sub = font(44)
    tagline = "医疗 · AI · 资本 · 美妆 · 政策"
    bbox2 = draw.textbbox((0,0), tagline, font=f_sub)
    sw = bbox2[2]-bbox2[0]
    draw.text(((W-sw)//2, H//2-40), tagline, font=f_sub, fill=GRAY)

    f_acc = font(36)
    acc = "刘一 | 精算师聊健康"
    abbox = draw.textbbox((0,0), acc, font=f_acc)
    aw = abbox[2]-abbox[0]
    draw.text(((W-aw)//2, H-130), acc, font=f_acc, fill=ORANGE)

    add_bottom_line(draw)

    path = os.path.join(OUTPUT_DIR, "00_cover.png")
    img.save(path)
    print(f"  [封面] {path}")
    return path

def make_news_slide(num, total, tag, title, points):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient_bg(img, draw)

    add_left_bar(draw, ORANGE, 6)

    f_tag = font(26)
    draw.text((80, 55), f"[{num}/{total}] {tag}", font=f_tag, fill=ORANGE)

    f_title = font(52, bold=True)
    draw.text((80, 110), title, font=f_title, fill=WHITE)

    draw.rectangle([(80, 200),(W-80, 204)], fill=ORANGE)

    f_pt = font(32)
    y = 240
    for line in points:
        line = line.strip()
        if not line:
            continue
        if line.startswith("•"):
            draw.ellipse([(85, y+10),(100, y+25)], fill=ORANGE)
            draw.text((115, y), line[1:].strip(), font=f_pt, fill=WHITE)
        else:
            draw.text((100, y), line, font=f_pt, fill=GRAY)
        y += 58
        if y > H - 120:
            break

    add_page_num(draw, num, total)
    add_bottom_line(draw)

    slug = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', title)[:8]
    path = os.path.join(OUTPUT_DIR, f"0{num}_{slug}.png")
    img.save(path)
    print(f"  [新闻{num}] {path}")
    return path

def make_data_slide(num, total, big_num, big_label, sub_text):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient_bg(img, draw)

    f_num = font(180, bold=True)
    draw.text((W//2 - 300, H//2 - 200), big_num, font=f_num, fill=ORANGE)

    f_label = font(52)
    draw.text((W//2 + 220, H//2 - 40), big_label, font=f_label, fill=WHITE)

    f_sub = font(36)
    bbox = draw.textbbox((0,0), sub_text, font=f_sub)
    sw = bbox[2]-bbox[0]
    draw.text(((W-sw)//2, H//2 + 80), sub_text, font=f_sub, fill=GRAY)

    add_page_num(draw, num, total)
    add_bottom_line(draw)

    path = os.path.join(OUTPUT_DIR, f"0{num}_data.png")
    img.save(path)
    print(f"  [数据{num}] {path}")
    return path

def make_closing():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient_bg(img, draw)

    f_main = font(90, bold=True)
    t1 = "关注我"
    bbox = draw.textbbox((0,0), t1, font=f_main)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H//2-100), t1, font=f_main, fill=WHITE)

    f_sub = font(52)
    t2 = "刘一 | 精算师聊健康"
    bbox2 = draw.textbbox((0,0), t2, font=f_sub)
    sw = bbox2[2]-bbox2[0]
    draw.text(((W-sw)//2, H//2), t2, font=f_sub, fill=ORANGE)

    f_date = font(30)
    t3 = "每早8:30 | 大健康资讯早知道"
    bbox3 = draw.textbbox((0,0), t3, font=f_date)
    sw3 = bbox3[2]-bbox3[0]
    draw.text(((W-sw3)//2, H//2+80), t3, font=f_date, fill=GRAY)

    add_bottom_line(draw)

    path = os.path.join(OUTPUT_DIR, "99_closing.png")
    img.save(path)
    print(f"  [结尾] {path}")
    return path

if __name__ == "__main__":
    print("=" * 50)
    print("生成 2026-05-11 早报幻灯片...")
    
    slides = []
    TOTAL = 7

    # 封面
    slides.append(make_cover())

    # 新闻1: 正大天晴×GSK 乙肝新药
    slides.append(make_news_slide(
        1, TOTAL,
        "医疗 · 制药",
        "正大天晴×葛兰素史克：乙肝新药加速入华",
        [
            "• 中国生物制药旗下正大天晴",
            "  与全球制药巨头GSK达成独家战略合作",
            "• 共同推动乙肝治疗药物 bepirovirsen",
            "  在中国内地上市进程",
            "• bepirovirsen 属于反义寡核苷酸(ASO)类",
            "  创新药，针对慢性乙肝患者",
            "• 中国乙肝感染者约7000万，用药需求巨大",
        ]
    ))

    # 新闻2: 美图AI无痕改字
    slides.append(make_news_slide(
        2, TOTAL,
        "AI · 科技",
        '美图AI"无痕改字"功能落地：支持五语种',
        [
            "• 美图影像研究院(MT Lab)6篇论文",
            "  同时被ICLR、CVPR、ICML三大顶会录用",
            '• "无痕改字"AI功能已上线',
            "  美图设计室App和美图秀秀PC版",
            "• 支持中、英、日、韩、泰五语种",
            "  保持字体风格与画面质感一致",
            "• 突破传统改字的预设词表限制",
        ]
    ))

    # 新闻3: 创业板突破3900点
    slides.append(make_news_slide(
        3, TOTAL,
        "资本市场 · 股市",
        "创业板指突破3900点：创逾10年新高",
        [
            "• A股午盘创业板指涨近2.75%",
            "  突破3900点，为2015年6月以来新高",
            "• 科创50指数涨逾5%",
            "  半导体、电脑硬件板块领涨",
            "• 澜起科技涨停(涨超20%)",
            "  兆易创新涨超12%",
            "• 医疗科技板块同步走强",
        ]
    ))

    # 新闻4: 进出口化妆品新规
    slides.append(make_news_slide(
        4, TOTAL,
        "美妆 · 消费",
        "进出口化妆品新规12月施行：电子标签来了",
        [
            "• 海关总署发布新修订的",
            "  《进出口化妆品检验检疫监督管理办法》",
            "• 新《办法》将于2026年12月1日起正式施行",
            "• 上海市率先启动进口化妆品",
            "  电子标签试点(今日起正式实施)",
            "• 消费者可扫码验真，利好海淘、代购",
        ]
    ))

    # 新闻5: 广东AI服务登记
    slides.append(make_news_slide(
        5, TOTAL,
        "AI · 政策",
        '广东省新增6款AI服务登记：累计已达53款',
        [
            '• 据"网信广东"官方公众号发布',
            "• 截至2026年5月11日",
            "  广东省新增6款生成式AI服务完成登记",
            "• 广东累计已完成53款",
            "  生成式人工智能服务登记",
            "• 体现各地持续推进AI监管规范化",
            "  AI服务进入合规发展新阶段",
        ]
    ))

    # 结尾
    slides.append(make_closing())

    print(f"\n共生成 {len(slides)} 张幻灯片")
    print(f"保存在: {OUTPUT_DIR}")