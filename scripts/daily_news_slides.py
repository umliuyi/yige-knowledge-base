#!/usr/bin/env python3
"""
早报内容 → 幻灯片视频
自动读取 markdown 内容，生成专业幻灯片，拼接配音视频
"""
from PIL import Image, ImageDraw, ImageFont
import os, sys, re

# ============ 配置 ============
SOURCE_FILE = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206\2026-05-27.md"
OUTPUT_DIR  = r"C:\Users\Administrator\Downloads\videos\daily_news"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1920, 1080
# ============================

# 配色方案（精算师风格：深色+橙色）
BG      = (8, 8, 18)
ORANGE  = (255, 87, 34)
CYAN    = (0, 188, 212)
WHITE   = (255, 255, 255)
GRAY    = (160, 160, 170)
DARK    = (30, 30, 50)
RED     = (220, 50, 50)

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
    """从上到下渐变背景"""
    w, h = img.size
    top, bot = (12, 12, 30), (4, 4, 12)
    for y in range(h):
        r = int(top[0]*(1-y/h) + bot[0]*y/h)
        g = int(top[1]*(1-y/h) + bot[1]*y/h)
        b = int(top[2]*(1-y/h) + bot[2]*y/h)
        draw.line([(0,y),(w,y)], fill=(r,g,b))

def glow_text(draw, xy, text, fill, font_obj, glow_color=None, glow_radius=3):
    """文字发光效果"""
    if glow_color:
        for dx in range(-glow_radius, glow_radius+1):
            for dy in range(-glow_radius, glow_radius+1):
                d = (dx**2 + dy**2) ** 0.5
                if d <= glow_radius:
                    alpha = int(80 * (1 - d/glow_radius))
                    c = tuple(max(0,min(255, glow_color[i] + alpha)) for i in range(3))
                    draw.text((xy[0]+dx, xy[1]+dy), text, font=font_obj, fill=c)
    draw.text(xy, text, font=font_obj, fill=fill)

def add_left_bar(draw, color=ORANGE, width=6):
    draw.rectangle([(0,0),(width, H)], fill=color)

def add_bottom_line(draw, color=CYAN):
    draw.rectangle([(0, H-5), (W, H)], fill=color)

def add_page_num(draw, num, total):
    txt = f"{num}/{total}"
    f = font(22)
    draw.text((W-100, H-70), txt, font=f, fill=GRAY)

def make_cover(date_str, tagline):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient_bg(img, draw)
    
    # 顶部橙色条
    draw.rectangle([(0,0),(W,8)], fill=ORANGE)
    
    # 日期
    f_date = font(32)
    draw.text((80, 60), date_str, font=f_date, fill=GRAY)
    
    # 主标题
    f_title = font(96, bold=True)
    title = "大健康早报"
    bbox = draw.textbbox((0,0), title, font=f_title)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, H//2-160), title, font=f_title, fill=WHITE)
    
    # 副标题（标签）
    f_sub = font(44)
    bbox2 = draw.textbbox((0,0), tagline, font=f_sub)
    sw = bbox2[2]-bbox2[0]
    draw.text(((W-sw)//2, H//2-40), tagline, font=f_sub, fill=GRAY)
    
    # 底部账号
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

def make_news_slide(num, total, tag, title, points, highlight_key=None):
    """新闻内容页"""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient_bg(img, draw)
    
    # 左侧橙色竖线
    add_left_bar(draw, ORANGE, 6)
    
    # 新闻编号标签
    f_tag = font(26)
    draw.text((80, 55), f"[{num}/{total}] {tag}", font=f_tag, fill=ORANGE)
    
    # 标题
    f_title = font(58, bold=True)
    draw.text((80, 110), title, font=f_title, fill=WHITE)
    
    # 分隔线
    draw.rectangle([(80, 200),(W-80, 204)], fill=ORANGE)
    
    # 要点
    f_pt = font(36)
    y = 240
    for line in points:
        line = line.strip()
        if not line:
            continue
        if line.startswith("•"):
            # 橙色圆点 + 白色文字
            draw.ellipse([(85, y+10),(100, y+25)], fill=ORANGE)
            draw.text((115, y), line[1:].strip(), font=f_pt, fill=WHITE)
        else:
            draw.text((100, y), line, font=f_pt, fill=GRAY)
        y += 65
        if y > H - 120:
            break
    
    # 右下角页码
    add_page_num(draw, num, total)
    add_bottom_line(draw)
    
    slug = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', title)[:6]
    path = os.path.join(OUTPUT_DIR, f"0{num}_{slug}.png")
    img.save(path)
    print(f"  [新闻{num}] {path}")
    return path

def make_data_slide(num, total, big_num, big_label, sub_text):
    """数据冲击页"""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    gradient_bg(img, draw)
    
    # 大数字
    f_num = font(220, bold=True)
    draw.text((W//2 - 350, H//2 - 220), big_num, font=f_num, fill=ORANGE)
    
    # 单位/标签
    f_label = font(52)
    draw.text((W//2 + 280, H//2 - 60), big_label, font=f_label, fill=WHITE)
    
    # 说明
    f_sub = font(36)
    bbox = draw.textbbox((0,0), sub_text, font=f_sub)
    sw = bbox[2]-bbox[0]
    draw.text(((W-sw)//2, H//2 + 60), sub_text, font=f_sub, fill=GRAY)
    
    # 页码
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
    
    # 中心
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

# ========================
# 幻灯片内容（从早报提取）
# ========================
if __name__ == "__main__":
    print("=" * 50)
    print("生成早报幻灯片...")
    
    slides = []
    
    # 封面
    slides.append(make_cover(
        "2026年5月9日 星期五",
        "CAR-T · 基因碎纸机 · 医疗AI · 患者故事"
    ))
    
    # 第1条：强化版CAR-T
    slides.append(make_news_slide(
        1, 5,
        "CAR-T · 血液癌",
        "强化版CAR-T疗法：11人中5人完全缓解",
        [
            "• 德国团队开发富集型CAR-T制剂，",
            "  干细胞记忆T细胞比例提高近10倍",
            "• 11名难治性血液癌症患者：",
            "  5人完全缓解，1人部分缓解",
            "• 副作用更低，无需高强度预处理",
            "• 结论：同等剂量下完全缓解率",
            "  远高于常规CAR-T疗法",
        ]
    ))
    
    # 第2条：基因碎纸机
    slides.append(make_news_slide(
        2, 5,
        "CRISPR · 精准医疗",
        '"基因碎纸机"Cas12a2：定向灭杀癌细胞',
        [
            "• 美国犹他大学团队发表《自然》",
            "• 识别病变细胞特有RNA后",
            "  触发细胞自我毁灭",
            "• KRAS突变肺癌：疗效媲美顺铂",
            "  健康细胞完全不受损",
            "• HPV小鼠实验：清除90%以上",
            "  感染细胞并抑制肿瘤生长",
        ]
    ))
    
    # 第3条：医疗AI
    slides.append(make_news_slide(
        3, 5,
        "AI · 医疗影像",
        "胸部CT一扫多查，落地30家医院",
        [
            "• 全国首款AI多病种产品",
            "  进入国家药监局创新通道",
            "• 单次胸部CT识别近百种异常",
            "  准确率97.8%",
            "• 已落地中山医院、北大人民医院",
            "  等30家医院，累计250万例",
            "• 阅片时间缩短33%",
        ]
    ))
    
    # 第4条：慢淋母亲故事
    slides.append(make_data_slide(
        4, 5,
        "56岁",
        "慢淋患者完全缓解",
        "真实病例：北京大学第一医院，国产BTK抑制剂+医保覆盖"
    ))
    
    # 第5条：dilanubicem
    slides.append(make_news_slide(
        5, 5,
        "干细胞 · 血癌",
        "新型干细胞产品：96%一年存活率",
        [
            "• 美国弗雷德·哈金森癌症中心",
            "  二期临床试验结果发布",
            "• 28名患者中27人存活一年以上",
            "  存活率96%，无严重排异",
            "• 与CAR-T形成互补：",
            "  不同机制，适合不同患者",
        ]
    ))
    
    # 结尾
    slides.append(make_closing())
    
    print(f"\n共生成 {len(slides)} 张幻灯片")
    print(f"保存在: {OUTPUT_DIR}")
