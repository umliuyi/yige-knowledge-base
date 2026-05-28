#!/usr/bin/env python3
"""生成竖版封面预览图（9:16，手机比例）"""

from PIL import Image, ImageDraw, ImageFont
import os

# 竖版尺寸 9:16
WIDTH = 1080
HEIGHT = 1920

# 配色
BG_COLOR = (10, 10, 20)  # 深色背景
ACCENT = (255, 140, 50)   # 橙色强调
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)

def make_cover(filename, title, subtitle, tag1, tag2):
    """生成单张竖版封面"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 尝试加载字体
    try:
        font_large = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 60)
        font_medium = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 36)
        font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 28)
        font_tag = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    # 顶部装饰条
    draw.rectangle([(0, 0), (WIDTH, 8)], fill=ACCENT)

    # 精算师标签
    draw.text((60, 80), "北美精算师", font=font_small, fill=ACCENT)

    # 主标题
    draw.text((60, 160), title, font=font_large, fill=WHITE)

    # 副标题
    draw.text((60, 260), subtitle, font=font_medium, fill=GRAY)

    # 分割线
    draw.rectangle([(60, 340), (WIDTH - 60, 342)], fill=ACCENT)

    # 话题标签
    y = 400
    for tag in [tag1, tag2]:
        draw.text((60, y), tag, font=font_tag, fill=(100, 100, 100))
        y += 50

    # 底部刘一信息
    draw.rectangle([(0, HEIGHT - 180), (WIDTH, HEIGHT - 176)], fill=(30, 30, 40))
    draw.text((60, HEIGHT - 140), "刘一｜精算师聊健康", font=font_medium, fill=ACCENT)
    draw.text((60, HEIGHT - 90), "关注我，用精算逻辑管理健康风险", font=font_small, fill=GRAY)

    img.save(filename)
    print(f"已生成: {filename}")

# 6条脚本的封面
scripts = [
    ("cover_1.png", "你高估了自己的身体", "感觉良好≠风险为零", "#精算师 #健康风险", ""),
    ("cover_2.png", "体检报告，你会看吗？", "看趋势，不看单点指标", "#体检报告 #精算师", ""),
    ("cover_3.png", "为什么看病越来越贵？", "医疗技术在进步，你的财务准备够吗？", "#医疗费用 #精算师", ""),
    ("cover_4.png", "一生要花多少看病钱？", "把医疗支出放在人生周期里看", "#医疗费用 #精算师", ""),
    ("cover_5.png", "为什么有人看病不花钱？", "医疗资源获取能力的差距", "#医疗资源 #精算师", ""),
    ("cover_6.png", "健康的人不算账\n生病的人才算", "健康风险管理最佳时间是还健康的时候", "#精算师 #健康管理", ""),
]

output_dir = os.path.expanduser("~/.openclaw")
os.makedirs(output_dir, exist_ok=True)

for fname, title, subtitle, tag1, tag2 in scripts:
    path = os.path.join(output_dir, fname)
    make_cover(path, title, subtitle, tag1, tag2)

print("\n全部生成完毕！")