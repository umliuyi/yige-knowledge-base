#!/usr/bin/env python3
"""生成竖版封面预览图 V2 - 优化阅读体验+避开按钮区域"""

from PIL import Image, ImageDraw, ImageFont
import os

# 竖版尺寸 9:16
WIDTH = 1080
HEIGHT = 1920

# 配色
BG_COLOR = (10, 10, 20)  # 深色背景
ACCENT = (255, 140, 50)   # 橙色强调
WHITE = (255, 255, 255)
DARK_GRAY = (80, 80, 80)
LIGHT_GRAY = (130, 130, 130)

# 安全区域（避开短视频按钮）
# 右侧按钮区：右边 120px
# 底部标题区：下边 300px
RIGHT_SAFE = WIDTH - 160
BOTTOM_SAFE = HEIGHT - 380

def load_font(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size)
    except:
        return ImageFont.load_default()

def make_cover_v2(filename, num, title, subtitle, tags):
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_num = load_font(28)
    font_title = load_font(72)
    font_sub = load_font(36)
    font_tag = load_font(26)
    font_brand = load_font(32)

    # === 顶部区域（安全，不被按钮挡）===
    # 左上角：精算师标签
    draw.rectangle([(50, 50), (220, 90)], outline=ACCENT, width=2)
    draw.text((60, 55), "北美精算师", font=font_num, fill=ACCENT)

    # 顶部装饰线
    draw.rectangle([(50, 110), (WIDTH-50, 114)], fill=ACCENT)

    # === 中央区域：标题（核心内容，左对齐）===
    # 计算标题换行
    max_chars = 16
    if len(title) > max_chars:
        # 找到中间空格换行
        mid = len(title) // 2
        for i in range(mid, len(title)):
            if title[i] == '\n':
                line1 = title[:i]
                line2 = title[i+1:]
                break
        else:
            # 没找到空格，强制从中间拆
            line1 = title[:mid]
            line2 = title[mid:]
    else:
        line1 = title.replace('\n', '')
        line2 = ""

    # 主标题（居中偏上，远离按钮区）
    y = 300
    draw.text((80, y), line1, font=font_title, fill=WHITE)
    if line2:
        y += 85
        draw.text((80, y), line2, font=font_title, fill=WHITE)

    # 副标题
    y += 120
    draw.text((80, y), subtitle, font=font_sub, fill=LIGHT_GRAY)

    # === 分隔线 ===
    y += 80
    draw.rectangle([(80, y), (WIDTH-80, y+2)], fill=DARK_GRAY)

    # === 话题标签（左下角，安全区域）===
    y += 40
    for tag in tags:
        draw.text((80, y), tag, font=font_tag, fill=(100, 100, 100))
        y += 45

    # === 底部品牌信息（300px安全区外）===
    # 底部渐变条
    draw.rectangle([(0, HEIGHT-300), (WIDTH, HEIGHT-296)], fill=(30, 30, 40))

    # 品牌名
    draw.text((80, HEIGHT-240), "刘一｜精算师聊健康", font=font_brand, fill=ACCENT)

    # 引导语
    draw.text((80, HEIGHT-185), "用精算逻辑管理健康风险", font=font_num, fill=DARK_GRAY)

    # 序号
    draw.text((WIDTH-150, HEIGHT-240), f"0{num}" if num < 10 else str(num), font=load_font(48), fill=(40, 40, 50))

    img.save(filename)
    print(f"已生成: {filename}")

# 6条脚本
scripts = [
    ("cover_v2_1.png", 1, "你高估了\n自己的身体", "感觉良好 ≠ 风险为零", ["#精算师", "#健康风险"]),
    ("cover_v2_2.png", 2, "体检报告\n你会看吗？", "看趋势，不看单点指标", ["#体检报告", "#精算师"]),
    ("cover_v2_3.png", 3, "为什么看病\n越来越贵？", "医疗技术在进步，你的财务准备够吗？", ["#医疗费用", "#精算师"]),
    ("cover_v2_4.png", 4, "一生要花多少\n看病钱？", "把医疗支出放在人生周期里看", ["#医疗费用", "#长期规划"]),
    ("cover_v2_5.png", 5, "为什么有人\n看病不花钱？", "医疗资源获取能力的差距", ["#医疗资源", "#精算师"]),
    ("cover_v2_6.png", 6, "健康的人\n不算账", '生病的人才知道当初那个"没事"有多贵', ["#精算师", "#健康管理"]),
]

output_dir = os.path.join(os.path.expanduser("~"), ".openclaw-autoclaw", "media")
os.makedirs(output_dir, exist_ok=True)

for fname, num, title, subtitle, tags in scripts:
    path = os.path.join(output_dir, fname)
    make_cover_v2(path, num, title, subtitle, tags)

print("\n全部生成完毕！")