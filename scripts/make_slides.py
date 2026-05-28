#!/usr/bin/env python3
"""
早报幻灯片生成器 - 测试版
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT = r"C:\Users\Administrator\Downloads\videos\slides"
os.makedirs(OUTPUT, exist_ok=True)

W, H = 1920, 1080

# 品牌配色
COLORS = {
    'bg': (10, 10, 20),           # 深色背景
    'primary': (255, 87, 34),     # 橙色强调
    'secondary': (0, 188, 212),    # 青色
    'white': (255, 255, 255),
    'gray': (180, 180, 180),
    'gradient_top': (20, 20, 40),
    'gradient_bot': (5, 5, 15),
}

def load_font(size, bold=False):
    """加载字体"""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",   # 黑体
        "C:/Windows/Fonts/simsun.ttc",  # 宋体
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

def draw_gradient_bg(draw, width, height):
    """渐变背景"""
    for y in range(height):
        ratio = y / height
        r = int(COLORS['gradient_top'][0] * (1-ratio) + COLORS['gradient_bot'][0] * ratio)
        g = int(COLORS['gradient_top'][1] * (1-ratio) + COLORS['gradient_bot'][1] * ratio)
        b = int(COLORS['gradient_top'][2] * (1-ratio) + COLORS['gradient_bot'][2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def make_cover(title, subtitle, date_str):
    """封面页"""
    img = Image.new('RGB', (W, H), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H)
    
    # 顶部装饰线
    draw.rectangle([(0, 0), (W, 6)], fill=COLORS['primary'])
    
    # 日期标签
    font_date = load_font(28)
    draw.text((80, 60), date_str, font=font_date, fill=COLORS['gray'])
    
    # 主标题
    font_title = load_font(90, bold=True)
    # 计算标题位置使其居中
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H//2 - 100), title, font=font_title, fill=COLORS['white'])
    
    # 副标题
    font_sub = load_font(40)
    bbox2 = draw.textbbox((0, 0), subtitle, font=font_sub)
    sw = bbox2[2] - bbox2[0]
    draw.text(((W - sw) // 2, H//2 + 20), subtitle, font=font_sub, fill=COLORS['gray'])
    
    # 底部账号信息
    font_account = load_font(30)
    account = "刘一 | 精算师聊健康"
    abbox = draw.textbbox((0, 0), account, font=font_account)
    aw = abbox[2] - abbox[0]
    draw.text(((W - aw) // 2, H - 100), account, font=font_account, fill=COLORS['primary'])
    
    # 底部装饰线
    draw.rectangle([(0, H-4), (W, H)], fill=COLORS['secondary'])
    
    path = os.path.join(OUTPUT, "slide_cover.png")
    img.save(path)
    print(f"封面: {path}")
    return path

def make_content_slide(title, body_lines, highlight=None):
    """内容页"""
    img = Image.new('RGB', (W, H), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H)
    
    # 左侧竖条
    draw.rectangle([(0, 0), (8, H)], fill=COLORS['primary'])
    
    # 标题
    font_title = load_font(60, bold=True)
    draw.text((80, 60), title, font=font_title, fill=COLORS['white'])
    
    # 分隔线
    draw.rectangle([(80, 160), (W - 80, 165)], fill=COLORS['primary'])
    
    # 正文
    font_body = load_font(38)
    y = 200
    for line in body_lines:
        if line.startswith("•"):
            # 要点
            font_pt = load_font(36)
            draw.text((100, y), line, font=font_pt, fill=COLORS['white'])
            # 橙色圆点
            draw.ellipse([(75, y + 10), (90, y + 25)], fill=COLORS['primary'])
        elif line.startswith("【"):
            # 高亮标签
            font_tag = load_font(30)
            draw.text((80, y), line, font=font_tag, fill=COLORS['secondary'])
        else:
            draw.text((80, y), line, font=font_body, fill=COLORS['gray'])
        y += 70
    
    # 右下角页码装饰
    font_page = load_font(24)
    draw.text((W - 150, H - 80), "早报", font=font_page, fill=COLORS['gray'])
    
    path = os.path.join(OUTPUT, f"slide_{title[:4]}.png")
    img.save(path)
    print(f"内容页: {path}")
    return path

def make_data_slide(title, big_number, unit, description):
    """数据页"""
    img = Image.new('RGB', (W, H), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H)
    
    # 大数字
    font_num = load_font(200, bold=True)
    # 数字颜色渐变
    draw.text((W//2 - 300, H//2 - 200), big_number, font=font_num, fill=COLORS['primary'])
    
    # 单位
    font_unit = load_font(60)
    draw.text((W//2 + 200, H//2 - 80), unit, font=font_unit, fill=COLORS['white'])
    
    # 说明
    font_desc = load_font(36)
    bbox = draw.textbbox((0, 0), description, font=font_desc)
    dw = bbox[2] - bbox[0]
    draw.text(((W - dw)//2, H//2 + 60), description, font=font_desc, fill=COLORS['gray'])
    
    # 标题
    font_title = load_font(50, bold=True)
    bbox2 = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox2[2] - bbox2[0]
    draw.text(((W - tw)//2, 80), title, font=font_title, fill=COLORS['white'])
    
    path = os.path.join(OUTPUT, f"slide_data.png")
    img.save(path)
    print(f"数据页: {path}")
    return path

def make_closing_slide():
    """结尾页"""
    img = Image.new('RGB', (W, H), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H)
    
    # 中心文字
    font_main = load_font(70, bold=True)
    text = "关注我"
    bbox = draw.textbbox((0, 0), text, font=font_main)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw)//2, H//2 - 100), text, font=font_main, fill=COLORS['white'])
    
    font_sub = load_font(50)
    sub = "刘一 | 精算师聊健康"
    sbbox = draw.textbbox((0, 0), sub, font=font_sub)
    sw = sbbox[2] - sbbox[0]
    draw.text(((W - sw)//2, H//2), sub, font=font_sub, fill=COLORS['primary'])
    
    path = os.path.join(OUTPUT, "slide_closing.png")
    img.save(path)
    print(f"结尾: {path}")
    return path

if __name__ == "__main__":
    print("生成测试幻灯片...")
    
    # 测试封面
    make_cover(
        "2026年大健康早报",
        "CAR-T · mRNA疫苗 · 乐城五周年",
        "2026年5月9日 | 第12期"
    )
    
    # 测试数据页
    make_data_slide(
        "2023年中国新增癌症患者",
        "480万",
        "人/年",
        "平均每分钟9人确诊"
    )
    
    # 测试内容页
    make_content_slide(
        "CAR-T治疗最新进展",
        [
            "【产品动态】",
            "• 奕凯达、阿基仑赛等CAR-T疗法已在国内上市",
            "• 一次治疗费用约120万，权益卡可报销",
            "• 乐城先行区可享受海外已上市新药",
            "【精算视角】",
            "• 大病治疗成本=家庭收入的5-10倍",
            "• 120万 vs 365元/年权益卡，杠杆率超3000倍",
        ]
    )
    
    make_closing_slide()
    
    print("\n幻灯片生成完成！")
    print(f"保存在: {OUTPUT}")
