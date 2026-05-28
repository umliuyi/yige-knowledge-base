"""
精算师视角早报视频幻灯片生成器 v2
- 专业设计：精算师风格
- 发布级品质
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import sys

# 尺寸
W, H = 1080, 1920

# 颜色系统
BG_DARK = (10, 20, 40)          # 深蓝背景
BG_ACCENT = (20, 50, 90)        # 蓝色强调
ORANGE = (255, 140, 0)          # 橙色强调
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
LIGHT_GRAY = (120, 120, 120)
YELLOW = (255, 220, 80)         # 精算师金

# 字体路径
FONT_PATH = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc" # 微软雅黑粗体

def safe_font(size, bold=False):
    try:
        path = FONT_BOLD if bold else FONT_PATH
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_gradient_bg(img, top_color, bottom_color):
    """从上到下的渐变背景"""
    for y in range(H):
        ratio = y / H
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        ImageDraw.Draw(img).line([(0, y), (W, y)], fill=(r, g, b))

def wrap_text(text, width=20):
    lines = []
    for para in text.split('\n'):
        if para.strip():
            wrapped = textwrap.wrap(para, width=width)
            lines.extend(wrapped)
        else:
            lines.append('')
    return lines

def make_slide_cover(date_str, subtitle=""):
    """封面"""
    img = Image.new('RGB', (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    # 顶部装饰条
    draw.rectangle([(0, 0), (W, 8)], fill=ORANGE)

    # 精算师视角标签
    font_tag = safe_font(28, bold=True)
    draw.text((60, 80), "精算师视角", fill=ORANGE, font=font_tag)

    # 主标题
    font_title = safe_font(96, bold=True)
    title_lines = wrap_text("大健康\n早报", width=8)
    for i, line in enumerate(title_lines):
        y = 260 + i * 110
        draw.text((60, y), line, fill=WHITE, font=font_title)

    # 日期
    font_date = safe_font(40)
    draw.text((60, 560), date_str, fill=GRAY, font=font_date)

    # 精算师金线
    draw.line([(60, 620), (400, 620)], fill=YELLOW, width=3)

    # 副标题（主题）
    if subtitle:
        font_sub = safe_font(36)
        subs = wrap_text(subtitle, width=20)
        for i, line in enumerate(subs[:2]):
            draw.text((60, 680 + i * 50), line, fill=GRAY, font=font_sub)

    # 底部账号条
    draw.rectangle([(0, H - 100), (W, H)], fill=(5, 10, 20))
    font_account = safe_font(32)
    draw.text((60, H - 75), "刘一｜精算师聊健康", fill=LIGHT_GRAY, font=font_account)

    return img

def make_slide_content(title, body, source="", tag=""):
    """内容页"""
    img = Image.new('RGB', (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    # 左侧标签条
    draw.rectangle([(0, 0), (8, H)], fill=ORANGE)

    # 顶部横线
    draw.line([(60, 60), (W - 60, 60)], fill=(40, 60, 100), width=1)

    # 标签
    if tag:
        font_tag = safe_font(26, bold=True)
        draw.text((60, 80), tag, fill=ORANGE, font=font_tag)

    # 主标题
    font_title = safe_font(64, bold=True)
    title_lines = wrap_text(title, width=14)
    for i, line in enumerate(title_lines[:3]):
        draw.text((60, 160 + i * 80), line, fill=WHITE, font=font_title)

    # 精算师金线
    draw.line([(60, 430), (300, 430)], fill=YELLOW, width=3)

    # 正文
    font_body = safe_font(36)
    body_lines = wrap_text(body, width=22)
    for i, line in enumerate(body_lines[:12]):
        draw.text((60, 480 + i * 50), line, fill=GRAY, font=font_body)

    # 来源
    if source:
        font_source = safe_font(24)
        draw.text((60, H - 150), f"来源: {source}", fill=LIGHT_GRAY, font=font_source)

    # 底部账号
    draw.rectangle([(0, H - 100), (W, H)], fill=(5, 10, 20))
    font_account = safe_font(32)
    draw.text((60, H - 75), "刘一｜精算师聊健康", fill=LIGHT_GRAY, font=font_account)

    return img

def make_slide_closing():
    """结尾页"""
    img = Image.new('RGB', (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    # 橙色大标题
    font_main = safe_font(80, bold=True)
    lines = wrap_text("关注我\n精算师帮你\n算清楚大健康这笔账", width=10)
    for i, line in enumerate(lines):
        draw.text((60, 300 + i * 100), line, fill=ORANGE, font=font_main)

    # 账号
    font_account = safe_font(40)
    draw.text((60, H - 180), "刘一｜精算师聊健康", fill=WHITE, font=font_account)

    # 底部标签
    font_tag = safe_font(28)
    draw.text((60, H - 120), "海南博鳌乐城先行区", fill=LIGHT_GRAY, font=font_tag)

    return img

if __name__ == "__main__":
    import os
    out_dir = r"C:\Users\Administrator\Downloads\videos\daily_news\test_v2"
    os.makedirs(out_dir, exist_ok=True)

    # 测试封面
    cover = make_slide_cover("2026年5月25日", "MSC治疗糖尿病：精算师怎么算这笔账")
    cover.save(os.path.join(out_dir, "cover.png"))

    # 测试内容页
    content = make_slide_content(
        "17.94万 vs 50万",
        "糖尿病患者终生治疗费约50-80万。\n60%用于并发症（心梗、脑梗、肾衰）。\nMSC治疗，17.94万/疗程。\n文献：30-40%患者胰岛素减量50%。\n5年少花25万并发症治疗费。\n\n17.94万，换5年不得并发症。\n不划算吗？",
        source="Cytotherapy 2026 | PMID:42562645",
        tag="精算师视角"
    )
    content.save(os.path.join(out_dir, "content1.png"))

    print(f"Done. Files in {out_dir}")
