import sys, os
sys.path.insert(0, r'C:\Users\Administrator\.openclaw-autoclaw\workspace\scripts')
from daily_poster_template import make_poster

def make_with_logo(cfg, logo_path, logo_pos, output):
    from PIL import Image
    
    # First make base poster
    make_poster(cfg, output + '.tmp.png')
    
    # Then paste logo on top
    base = Image.open(output + '.tmp.png').convert('RGBA')
    logo = Image.open(logo_path).convert('RGBA')
    
    # Resize logo to reasonable size (max width 200px)
    lw, lh = logo.size
    max_w = 200
    if lw > max_w:
        ratio = max_w / lw
        new_h = int(lh * ratio)
        logo = logo.resize((max_w, new_h), Image.LANCZOS)
    
    lw2, lh2 = logo.size
    
    if logo_pos == 'top_left':
        x, y = 55, 130  # below the date
    elif logo_pos == 'bottom_right':
        x = base.width - lw2 - 55
        y = base.height - lh2 - 55
    elif logo_pos == 'bottom_left':
        x, y = 55, base.height - lh2 - 55
    elif logo_pos == 'center_bottom':
        x = (base.width - lw2) // 2
        y = base.height - lh2 - 60
    else:
        x, y = 55, 130
    
    base.paste(logo, (x, y), logo)
    rgb = base.convert('RGB')
    rgb.save(output, quality=93)
    os.remove(output + '.tmp.png')
    print(f'Done: {os.path.getsize(output)//1024}KB')

cfg = {
    'date': '2026.05.13',
    'weekday': '星期二',
    'main_number': '480',
    'main_unit': '万',
    'main_desc': '中国人每年新发癌症',
    'section_title': '精算师视角',
    'section_points': [
        ('其中不到30%', '能用上新药'),
        ('原因一：海外新药国内未批',),
        ('原因二：普通家庭无力承担',),
        ('结果：等不起，也用不起',),
    ],
    'quote1': '健康的人',
    'quote2': '不算账',
    'signature': '刘一｜精算师聊健康',
    'location': '海南博鳌乐城先行区',
    'tag': '乐城视角',
    'bg_image_path': r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\lecheng_official.jpg',
    'bg_image_url': '',
    'color_accent': (210, 50, 30),
    'color_bg': (8, 8, 12),
}
logo = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\ref_images\logo.png'
out = r'C:\Users\Administrator\Downloads\daily_news_with_logo.png'
make_with_logo(cfg, logo, 'top_left', out)
