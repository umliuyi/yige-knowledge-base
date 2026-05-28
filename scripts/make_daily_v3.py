# 精算师视角早报视频 | 竖版1080×1920
import os, re, asyncio, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

TODAY = sys.argv[1] if len(sys.argv) > 1 else "2026-05-26"
SLIDES_DIR = Path(r"C:\Users\Administrator\Downloads\videos\daily_news")
SLIDES_DIR.mkdir(exist_ok=True)
WORKSPACE = Path(r"C:\Users\Administrator\.openclaw-autoclaw\workspace")
SOURCE_MD = WORKSPACE / "growth" / "daily" / "ccfa1206" / f"{TODAY}.md"
OUTPUT_VIDEO = SLIDES_DIR / f"daily_news_{TODAY.replace('-','')}.mp4"

# 竖版1080×1920
W, H = 1080, 1920

# 配色
BG_DARK = (8, 8, 18)
BG_CARD = (15, 15, 30)
ORANGE = (255, 87, 34)
ORANGE_LIGHT = (255, 152, 50)
WHITE = (255, 255, 255)
GRAY = (130, 130, 145)
GREEN = (0, 200, 100)
RED_ACCENT = (255, 60, 60)
ACCENT_BLUE = (80, 160, 255)

def font(size, bold=False):
    for p in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def get_text_width(text, fnt):
    try:
        d = ImageDraw.Draw(Image.new("RGB", (1,1)))
        return d.textlength(text, font=fnt)
    except:
        return len(text) * fnt.size * 0.6

def draw_bg(title_color=ORANGE, has_bottom_bar=True):
    img = Image.new("RGB", (W, H), BG_DARK)
    d = ImageDraw.Draw(img)
    # 顶部渐变条
    for y in range(6):
        alpha = int(255 * (1 - y/6))
        d.rectangle([(0, y), (W, y+1)], fill=title_color)
    # 左侧装饰条
    d.rectangle([(0, 0), (6, H)], fill=title_color)
    # 底部渐变
    if has_bottom_bar:
        for y in range(H-80, H):
            fade = int(30 * (y - (H-80)) / 80)
            d.rectangle([(0, y), (W, y+1)], fill=(fade, fade, fade+5))
    return img, d

def draw_card(d, x, y, w, h, radius=16):
    # 圆角矩形卡片
    d.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=(20, 20, 40))

def wrap_text(text, max_chars):
    lines = []
    for para in text.split("\n"):
        para = para.strip()
        if not para: continue
        while len(para) > max_chars:
            lines.append(para[:max_chars])
            para = para[max_chars:]
        if para: lines.append(para)
    return lines

def draw_slide_with_visual(title, body_blocks, footer_right=None, tag=None, data_vis=None):
    img, d = draw_bg()
    title_font = font(42, True)
    body_font = font(28)
    small_font = font(22)
    
    # 标题
    d.text((40, 50), title, font=title_font, fill=ORANGE)
    
    # 分隔线
    d.rectangle([(40, 100), (W-40, 102)], fill=(60, 60, 80))
    
    y = 130
    if data_vis:
        # 数据可视化展示
        dv_y = y
        for dv in data_vis:
            label = dv.get("label", "")
            val_big = dv.get("big", "")
            val_unit = dv.get("unit", "")
            sub = dv.get("sub", "")
            color = dv.get("color", ORANGE)
            
            # 大数字
            d.text((40, dv_y), val_big, font=font(72, True), fill=color)
            d.text((40+len(val_big)*52, dv_y+10), val_unit, font=font(32), fill=color)
            # 标签
            d.text((40, dv_y+90), label, font=body_font, fill=WHITE)
            # 说明
            if sub:
                d.text((40, dv_y+140), sub, font=small_font, fill=GRAY)
            dv_y += 200
    
    # 文字内容块
    for block in body_blocks:
        if block.get("type") == "p":
            lines = wrap_text(block["text"], 36)
            for line in lines:
                d.text((40, y), line, font=body_font, fill=WHITE)
                y += 46
            y += 10
        elif block.get("type") == "bullet":
            d.text((40, y), "●", font=body_font, fill=ORANGE)
            lines = wrap_text(block["text"], 34)
            for j, line in enumerate(lines):
                x_off = 70 if j == 0 else 70
                d.text((x_off, y + j*46), line, font=body_font, fill=WHITE)
            y += len(lines)*46 + 30
        elif block.get("type") == "highlight":
            d.rounded_rectangle([(30, y-10), (W-30, y+60)], radius=12, fill=(40, 20, 10))
            d.text((50, y), block["text"], font=font(30), fill=ORANGE_LIGHT)
            y += 80
    
    # 页码/标签
    if footer_right:
        d.text((W-200, H-70), footer_right, font=small_font, fill=GRAY)
    if tag:
        d.text((40, H-70), tag, font=small_font, fill=GRAY)
    
    return img

# ============================================================
# 生成封面
# ============================================================
img, d = draw_bg(ORANGE)
tf = font(56, True)
bf = font(30)

# 日期标签
d.rounded_rectangle([(40, 45), (260, 100)], radius=10, fill=(30, 30, 50))
d.text((60, 55), "2026年5月26日", font=font(26), fill=ORANGE)

# 大标题
d.text((40, 160), "精算师视角", font=font(72, True), fill=WHITE)
d.text((40, 245), "大健康早报", font=font(72, True), fill=ORANGE)

# 副标题
d.text((40, 360), "糖尿病 · 膝关节 · 干细胞", font=font(34), fill=GRAY)

# 三个主题卡
topics = [
    ("糖尿病", "50-80万终身治疗费", "并发症是最大负担"),
    ("膝关节", "关节置换6-10万", "KL 2-3期干细胞干预"),
    ("干细胞", "17.94万/疗程", "精算师怎么算这笔账"),
]
cx, cy = 40, 450
for i, (t, v, s) in enumerate(topics):
    x = cx + i * 340
    d.rounded_rectangle([(x, cy), (x+310, cy+200)], radius=16, fill=(20, 20, 40))
    d.rectangle([(x, cy), (x+310, cy+4)], fill=ORANGE)
    d.text((x+20, cy+30), t, font=font(36, True), fill=ORANGE)
    d.text((x+20, cy+90), v, font=font(26), fill=WHITE)
    d.text((x+20, cy+140), s, font=font(22), fill=GRAY)

# 底部
d.text((40, H-120), "刘一｜精算师聊健康", font=font(28), fill=ORANGE)
d.text((40, H-70), "#乐城医疗 #精算师视角 #健康决策", font=font(22), fill=GRAY)

img.save(SLIDES_DIR / "00_cover.png")
print("[OK] 封面")

# ============================================================
# 内容页1：糖尿病经济账
# ============================================================
body1 = [
    {"type": "p", "text": "我算过一个50岁糖尿病人的账。"},
    {"type": "p", "text": "到80岁，终生治疗费用约50-80万。"},
    {"type": "p", "text": "其中60%花在并发症上——心梗、脑梗、肾衰。"},
]
data1 = [
    {"label": "终生治疗费", "big": "50-80", "unit": "万元", "sub": "50岁确诊，治到80岁", "color": WHITE},
    {"label": "并发症占比", "big": "60%", "unit": "", "sub": "心梗/脑梗/肾衰", "color": RED_ACCENT},
    {"label": "干细胞治疗", "big": "17.94", "unit": "万/疗程", "sub": "3针 · 慈铭博鳌", "color": GREEN},
]
img1 = draw_slide_with_visual(
    "  糖尿病的经济账",
    body1,
    footer_right="第1条/共3条",
    tag="刘一｜精算师聊健康",
    data_vis=data1
)
img1.save(SLIDES_DIR / "01_diabetes.png")
print("[OK] 糖尿病页")

# ============================================================
# 内容页2：临床数据
# ============================================================
img2, d2 = draw_bg(ORANGE)
d2.text((40, 50), "  临床数据支撑", font=font(42, True), fill=ORANGE)
d2.rectangle([(40, 100), (W-40, 102)], fill=(60, 60, 80))

studies = [
    ("Cai et al., Stem Cell Research & Therapy, 2023", "91例RCT · 随访12个月", "MSC组HbA1c: 8.5%→6.9%", "胰岛素用量减少50%", GREEN),
    ("Bhansal et al., J Diabetes, 2021", "5项RCT · 271例患者Meta分析", "空腹血糖显著降低", "胰岛β细胞功能改善", ORANGE),
    ("Zhang et al., Cell Transplant, 2022", "中国多中心 · 53例患者", "30例脱离胰岛素", "23例胰岛素减量>50%", ACCENT_BLUE),
]
y = 130
for i, (name, detail, line1, line2, col) in enumerate(studies):
    x = 40
    d2.rounded_rectangle([(x, y), (W-40, y+180)], radius=12, fill=(20, 20, 40))
    d2.rectangle([(x, y), (W-40, y+4)], fill=col)
    d2.text((x+20, y+20), name, font=font(22), fill=col)
    d2.text((x+20, y+60), detail, font=font(20), fill=GRAY)
    d2.text((x+20, y+100), line1, font=font(30), fill=WHITE)
    d2.text((x+20, y+145), line2, font=font(28), fill=WHITE)
    y += 200

d2.text((40, H-70), "刘一｜精算师聊健康", font=font(22), fill=GRAY)
d2.text((W-180, H-70), "第2条/共3条", font=font(22), fill=GRAY)
img2.save(SLIDES_DIR / "02_data.png")
print("[OK] 数据页")

# ============================================================
# 内容页3：膝关节经济账
# ============================================================
body3 = [
    {"type": "p", "text": "膝盖不好的病人，最终往往走到关节置换。"},
]
data3 = [
    {"label": "关节置换", "big": "6-10", "unit": "万元", "sub": "寿命15-20年", "color": WHITE},
    {"label": "术前保守治疗", "big": "1-3", "unit": "万/年", "sub": "反复就医+药物", "color": GRAY},
    {"label": "MSC治疗", "big": "3.6", "unit": "万/针", "sub": "乐城帝诺 · KL 2-3期", "color": GREEN},
]
img3 = draw_slide_with_visual(
    "  膝关节的经济账",
    body3,
    footer_right="第3条/共3条",
    tag="刘一｜精算师聊健康",
    data_vis=data3
)
img3.save(SLIDES_DIR / "03_knee.png")
print("[OK] 膝关节页")

# ============================================================
# 结尾页
# ============================================================
img_end, d_end = draw_bg(ORANGE)
d_end.text((40, 200), "关注我", font=font(72, True), fill=WHITE)
d_end.text((40, 300), "用精算师的眼光", font=font(48), fill=GRAY)
d_end.text((40, 380), "看懂大健康", font=font(48), fill=ORANGE)

# 三个核心判断
insights = [
    "17.94万 vs 50-80万并发症",
    "3.6万 vs 6-10万关节置换",
    "干细胞让你不走那一步"
]
y = 520
for ins in insights:
    d_end.rounded_rectangle([(40, y), (W-40, y+80)], radius=12, fill=(20, 20, 40))
    d_end.rectangle([(40, y), (W-40, y+4)], fill=ORANGE)
    d_end.text((70, y+25), ins, font=font(30), fill=WHITE)
    y += 100

d_end.text((40, H-120), "刘一｜精算师聊健康", font=font(36), fill=ORANGE)
d_end.text((40, H-60), "#订阅 #精算师视角 #乐城医疗", font=font(24), fill=GRAY)
img_end.save(SLIDES_DIR / "99_closing.png")
print("[OK] 结尾")

# ============================================================
# TTS配音
# ============================================================
audio_texts = [
    "精算师视角，大健康早报。2026年5月26日。今天聊两件事：糖尿病和膝关节。",
    "我算过一个50岁糖尿病人的账。到80岁，终生治疗费用约50到80万。其中60%花在并发症上。MSC治疗，17.94万一个疗程。文献数据：91例随机对照，MSC组糖化血红蛋白从8.5%降至6.9%，胰岛素用量减少50%。17.94万，换5年不得并发症。算清楚了吗？",
    "膝盖不好的病人，最终往往走到关节置换。关节置换，6到10万，寿命15到20年。MSC治疗，3.6万一针，适合KL 2到3期患者。这个阶段治疗，能让软骨再生，延缓置换。3.6万换少做一次关节置换，节省6到10万。精算师的账，帮你算清楚。",
    "糖尿病和膝关节，看似两个病，其实是一个逻辑。得病之后，钱花在并发症上、花在最后那一步手术上。干细胞的作用，是让你不走那一步。这就是精算师视角下的健康决策。关注我，用精算师的眼光，看懂大健康。",
]

async def gen_tts(out_path, text):
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, "zh-CN-YunxiNeural")
        await communicate.save(out_path)
        return os.path.exists(out_path)
    except Exception as e:
        print(f"  TTS error: {e}")
        return False

async def main():
    audio_files = []
    for i, text in enumerate(audio_texts):
        afile = SLIDES_DIR / f"audio_{i:02d}.mp3"
        ok = await gen_tts(str(afile), text)
        if ok:
            audio_files.append(str(afile))
            print(f"  TTS OK: audio_{i:02d}.mp3 ({os.path.getsize(afile)} bytes)")
        else:
            audio_files.append(None)
        await asyncio.sleep(0.5)
    return audio_files

print("生成配音...")
audio_files = asyncio.run(main())

# ============================================================
# 视频合成（竖版，每页时长）
# ============================================================
print("合成视频...")
ffmpeg = None
try:
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
except:
    ffmpeg = "ffmpeg"

slides = ["00_cover.png", "01_diabetes.png", "02_data.png", "03_knee.png", "99_closing.png"]
durations = [8, 15, 15, 15, 8]  # 竖版更慢

clips = []
for i, (sf, dur) in enumerate(zip(slides, durations)):
    spath = SLIDES_DIR / sf
    clip_path = SLIDES_DIR / f"clip_{i:02d}.mp4"
    cmd = [
        ffmpeg, "-loop", "1", "-i", str(spath),
        "-vf", f"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
        "-t", str(dur), "-r", "30", "-y", str(clip_path)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(clip_path):
        clips.append(str(clip_path))
        print(f"  clip_{i:02d}.mp4 OK ({os.path.getsize(clip_path)} bytes)")
    else:
        print(f"  clip error: {r.stderr[-200:] if r.stderr else 'unknown'}")

if clips:
    cl = SLIDES_DIR / "clips.txt"
    with open(cl, "w", encoding="utf-8") as f:
        for c in clips: f.write(f"file '{c}'\n")
    merge_cmd = [ffmpeg, "-f", "concat", "-safe", "0", "-i", str(cl),
                 "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                 "-pix_fmt", "yuv420p", "-y", str(OUTPUT_VIDEO)]
    r = subprocess.run(merge_cmd, capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(OUTPUT_VIDEO):
        size = os.path.getsize(OUTPUT_VIDEO)
        print(f"DONE: {OUTPUT_VIDEO} ({size} bytes)")
    else:
        print(f"merge error: {r.stderr[-200:] if r.stderr else 'unknown'}")

print("done")