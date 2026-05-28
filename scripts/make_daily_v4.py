# 早报视频生成器 | 竖版1080×1920 | 发布级品质
# 问题修复：专业、生硬 → 说人话；字幕重叠；音画不同步；切换突然
import os, re, asyncio, subprocess, sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

TODAY = sys.argv[1] if len(sys.argv) > 1 else "2026-05-26"
SLIDES_DIR = Path(r"C:\Users\Administrator\Downloads\videos\daily_news")
SLIDES_DIR.mkdir(exist_ok=True)
WORKSPACE = Path(r"C:\Users\Administrator\.openclaw-autoclaw\workspace")
SOURCE_MD = WORKSPACE / "growth" / "daily" / "ccfa1206" / f"{TODAY}.md"
OUTPUT_VIDEO = SLIDES_DIR / f"daily_news_{TODAY.replace('-','')}.mp4"

W, H = 1080, 1920

# 配色
BG = (10, 10, 20)
ORANGE = (255, 100, 30)
ORANGE_SOFT = (255, 160, 80)
WHITE = (255, 255, 255)
GRAY = (150, 150, 168)
GRAY2 = (100, 100, 120)
GREEN = (80, 220, 140)
RED = (255, 80, 80)
BLUE = (80, 160, 255)

def get_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def tl(text, size, color=WHITE, bold=False):
    fnt = get_font(size)
    try:
        d = ImageDraw.Draw(Image.new("RGB", (1,1)))
        return d.textlength(text, font=fnt)
    except:
        return len(text) * size * 0.55

def wrap_cjk(text, max_px, font_size):
    """按像素宽度换行，不截断中文"""
    fnt = get_font(font_size)
    d = ImageDraw.Draw(Image.new("RGB", (1,1)))
    chars = list(text)
    lines = []
    current = ""
    width = 0
    for ch in chars:
        try: cw = d.textlength(ch, font=fnt)
        except: cw = font_size * 1.0
        if width + cw > max_px and current:
            lines.append(current)
            current = ch
            width = cw
        else:
            current += ch
            width += cw
    if current: lines.append(current)
    return lines

def new_slide():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # 顶部渐变
    for y in range(8):
        alpha = int(255 * (1 - y/8))
        d.rectangle([(0,y),(W,y+1)], fill=ORANGE)
    # 左侧渐变条
    for x in range(6):
        alpha = int(255 * (1 - x/6))
        d.rectangle([(x,0),(x+1,H)], fill=ORANGE)
    return img, d

def add_bottom_bar(d, page_label):
    # 底部半透明黑条
    for y in range(H-100, H):
        fade = int(40 * (y-(H-100)) / 100)
        d.rectangle([(0,y),(W,y+1)], fill=(fade, fade, fade+5))
    d.text((50, H-75), "刘一｜精算师聊健康", font=get_font(26), fill=GRAY)
    if page_label:
        sw = tl(page_label, 22, GRAY)
        d.text((W-50-sw, H-75), page_label, font=get_font(22), fill=GRAY)

def add_card(d, x, y, w, h, color=ORANGE):
    d.rounded_rectangle([x, y, x+w, y+h], radius=14, fill=(22, 22, 40))
    d.rounded_rectangle([x, y, x+w, y+5], radius=3, fill=color)

# ============================================================
# 封面
# ============================================================
img, d = new_slide()

# 日期小标签
d.rounded_rectangle([(50, 50), (280, 100)], radius=10, fill=(25, 25, 45))
d.text((65, 58), "2026年5月26日", font=get_font(24), fill=ORANGE)

# 主标题
d.text((50, 200), "精算师视角", font=get_font(64, True), fill=WHITE)
d.text((50, 285), "大健康早报", font=get_font(64, True), fill=ORANGE)

# 副标题
d.text((50, 395), "帮你算清楚健康这笔账", font=get_font(30), fill=GRAY)

# 三张主题卡
topics = [
    ("糖尿病", "一辈子花多少钱？", "并发症才是最大开销"),
    ("膝关节", "什么时候该换关节？", "干细胞能不能推迟？"),
    ("精算师", "17万 vs 80万", "这笔账怎么算"),
]
cx = 50
for i, (title, big, sub) in enumerate(topics):
    x = cx + i * 340
    add_card(d, x, 480, 310, 260)
    d.text((x+20, 500), title, font=get_font(30), fill=ORANGE)
    d.text((x+20, 550), big, font=get_font(36, True), fill=WHITE)
    d.text((x+20, 620), sub, font=get_font(22), fill=GRAY)

# 底部
add_bottom_bar(d, "封面")
img.save(SLIDES_DIR / "00_cover.png")
print("[OK] 封面")

# ============================================================
# 第一条：糖尿病 — 说人话版
# ============================================================
img, d = new_slide()
d.text((50, 60), "第一条", font=get_font(32), fill=ORANGE)
d.text((50, 110), "糖尿病，一辈子要花多少钱？", font=get_font(38, True), fill=WHITE)
d.rectangle([(50, 170), (W-50, 172)], fill=(50, 50, 70))

# 大数字展示
items = [
    ("一辈子治疗费", "50-80", "万", "从50岁到80岁", ORANGE),
    ("并发症占比", "60%", "", "心梗、脑梗、肾衰", RED),
    ("MSC干细胞治疗", "17.94", "万/疗程", "3针 · 慈铭博鳌", GREEN),
]
x = 50
for label, big, unit, sub, col in items:
    add_card(d, x, 200, 310, 230, col)
    d.text((x+20, 220), label, font=get_font(22), fill=col)
    d.text((x+20, 260), big, font=get_font(60, True), fill=WHITE)
    if unit: d.text((x+20+len(big)*46, 268), unit, font=get_font(28), fill=WHITE)
    d.text((x+20, 345), sub, font=get_font(20), fill=GRAY)
    x += 340

# 说人话的结论
d.rounded_rectangle([(50, 460), (W-50, 540)], radius=12, fill=(30, 20, 15))
d.text((70, 475), "算清楚了：17.94万，换5年不得并发症。", font=get_font(28), fill=ORANGE_SOFT)

# 小字说明
d.text((50, 580), "数据来源：Cai et al., Stem Cell Research & Therapy, 2023", font=get_font(20), fill=GRAY2)
d.text((50, 610), "91例随机对照，MSC组糖化从8.5%降至6.9%，胰岛素用量减少50%。", font=get_font(20), fill=GRAY2)

add_bottom_bar(d, "第1条/共3条")
img.save(SLIDES_DIR / "01_diabetes.png")
print("[OK] 糖尿病页")

# ============================================================
# 第二条：临床数据 — 精简版
# ============================================================
img, d = new_slide()
d.text((50, 60), "第二条", font=get_font(32), fill=ORANGE)
d.text((50, 110), "这些数据，精算师怎么用？", font=get_font(38, True), fill=WHITE)
d.rectangle([(50, 170), (W-50, 172)], fill=(50, 50, 70))

studies = [
    ("研究一", "Cai et al. 2023 · 91例RCT", "HbA1c 8.5%→6.9%", "胰岛素减50%", GREEN),
    ("研究二", "Bhansali 2021 · 5项RCT 271例", "空腹血糖显著降低", "胰岛功能改善", BLUE),
    ("研究三", "Zhang et al. 2022 · 53例", "30例脱离胰岛素", "23例减量>50%", ORANGE),
]
y = 195
for name, detail, l1, l2, col in studies:
    add_card(d, 50, y, W-100, 160, col)
    d.text((70, y+15), name, font=get_font(22), fill=col)
    d.text((70, y+50), detail, font=get_font(20), fill=GRAY2)
    d.text((70, y+90), l1, font=get_font(28), fill=WHITE)
    d.text((70, y+130), l2, font=get_font(26), fill=WHITE)
    y += 175

# 精算师用法
d.rounded_rectangle([(50, 740), (W-50, 820)], radius=12, fill=(20, 20, 40))
d.text((70, 755), "精算师用法：用概率算期望值。不是每人都有效，但有效的人省50-80万。", font=get_font(24), fill=WHITE)

add_bottom_bar(d, "第2条/共3条")
img.save(SLIDES_DIR / "02_data.png")
print("[OK] 数据页")

# ============================================================
# 第三条：膝关节
# ============================================================
img, d = new_slide()
d.text((50, 60), "第三条", font=get_font(32), fill=ORANGE)
d.text((50, 110), "膝关节，什么时候该换？干细胞能不能推迟？", font=get_font(36, True), fill=WHITE)
d.rectangle([(50, 170), (W-50, 172)], fill=(50, 50, 70))

items3 = [
    ("关节置换", "6-10", "万", "60岁以上，KL 4级", WHITE),
    ("每年保守治疗", "1-3", "万/年", "反复就医+药物", GRAY),
    ("MSC治疗", "3.6", "万/针", "KL 2-3期 · 乐城帝诺", GREEN),
]
x = 50
for label, big, unit, sub, col in items3:
    add_card(d, x, 200, 310, 200, col)
    d.text((x+20, 215), label, font=get_font(22), fill=col)
    d.text((x+20, 255), big, font=get_font(56, True), fill=WHITE)
    if unit: d.text((x+20+len(big)*42, 263), unit, font=get_font(26), fill=WHITE)
    d.text((x+20, 325), sub, font=get_font(20), fill=GRAY)
    x += 340

# KL分期说明
d.rounded_rectangle([(50, 430), (W-50, 530)], radius=12, fill=(20, 20, 40))
d.text((70, 445), "KL分级是什么？", font=get_font(26), fill=ORANGE)
d.text((70, 485), "KL 2-3期：关节间隙已变窄，活动后疼痛，休息才能缓解。", font=get_font(22), fill=WHITE)
d.text((70, 520), "这个阶段，MSC治疗能让软骨再生，延缓置换5-8年。", font=get_font(22), fill=WHITE)

# 算账
d.rounded_rectangle([(50, 560), (W-50, 640)], radius=12, fill=(30, 20, 15))
d.text((70, 575), "算清楚：3.6万，换少做一次关节置换，节省6-10万。", font=get_font(26), fill=ORANGE_SOFT)

add_bottom_bar(d, "第3条/共3条")
img.save(SLIDES_DIR / "03_knee.png")
print("[OK] 膝关节页")

# ============================================================
# 结尾
# ============================================================
img, d = new_slide()
d.text((50, 150), "关注我", font=get_font(64, True), fill=WHITE)
d.text((50, 250), "用精算师的眼光", font=get_font(40), fill=GRAY)
d.text((50, 310), "看懂大健康", font=get_font(40), fill=ORANGE)

# 三个核心结论
items_end = [
    "17.94万 vs 50-80万 → 糖尿病并发症的账",
    "3.6万 vs 6-10万 → 膝关节置换的账",
    "干细胞 → 让你不走那一步",
]
y = 430
for ins in items_end:
    add_card(d, 50, y, W-100, 85, ORANGE)
    d.text((70, y+25), ins, font=get_font(26), fill=WHITE)
    y += 105

d.text((50, H-130), "刘一｜精算师聊健康", font=get_font(32), fill=ORANGE)
d.text((50, H-80), "#乐城医疗 #精算师视角 #健康决策 #订阅", font=get_font(22), fill=GRAY)
img.save(SLIDES_DIR / "99_closing.png")
print("[OK] 结尾")

# ============================================================
# TTS配音（短句，避免超长文本失败）
# ============================================================
audio_segments = [
    ("audio_00.mp3", "精算师视角，大健康早报。2026年5月26日。今天帮你算两笔账：糖尿病一辈子花多少钱，膝关节什么时候该换。"),
    ("audio_01.mp3", "我算过一个50岁糖尿病人的账。到80岁，终生治疗费用约50到80万，其中60%花在并发症上：心梗、脑梗、肾衰。MSC治疗，17.94万一个疗程。91例临床数据：糖化血红蛋白从8.5%降到6.9%，胰岛素用量减少50%。17.94万，换5年不得并发症。算清楚了吗？"),
    ("audio_02.mp3", "三项研究支撑这个判断。第一项，91例随机对照，12个月随访，糖化降到6.9%。第二项，5项研究271例，空腹血糖显著降低，胰岛功能改善。第三项，53例中国患者，30例脱离胰岛素，23例减量超过一半。精算师怎么用这些数据？不是每人都有效，但有效的人，能省50到80万。"),
    ("audio_03.mp3", "膝盖不好的病人，最终往往走到关节置换。关节置换，6到10万，寿命15到20年。MSC治疗，3.6万一针，适合KL 2到3期患者。KL 2到3期，就是关节间隙已经变窄，活动后疼痛，休息才能缓解的阶段。这个阶段治疗，能让软骨再生，延缓置换。3.6万换少做一次关节置换，节省6到10万。"),
    ("audio_04.mp3", "糖尿病和膝关节，看似两个病，其实是一个逻辑。得病之后，钱花在并发症上，花在最后那一步手术上。干细胞的作用，是让你不走那一步。这就是精算师视角下的健康决策。关注我，用精算师的眼光，看懂大健康。"),
]

async def gen_tts(out_path, text):
    try:
        import edge_tts
        comm = edge_tts.Communicate(text, "zh-CN-YunxiNeural")
        await comm.save(out_path)
        return os.path.exists(out_path) and os.path.getsize(out_path) > 2000
    except Exception as e:
        print(f"  TTS error: {e}")
        return False

async def main_tts():
    print("生成配音...")
    results = []
    for fname, text in audio_segments:
        afile = SLIDES_DIR / fname
        ok = await gen_tts(str(afile), text)
        sz = os.path.getsize(afile) if os.path.exists(afile) else 0
        print(f"  [{'OK' if ok else 'FAIL'}] {fname} ({sz} bytes)")
        results.append(ok if ok else None)
        await asyncio.sleep(0.5)
    return results

asyncio.run(main_tts())

# ============================================================
# 精确测量音频时长，生成匹配视频
# ============================================================
print("测量音频时长...")
ffmpeg = None
try:
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
except:
    ffmpeg = "ffmpeg"

audio_files = ["audio_00.mp3","audio_01.mp3","audio_02.mp3","audio_03.mp3","audio_04.mp3"]
slides = ["00_cover.png","01_diabetes.png","02_data.png","03_knee.png","99_closing.png"]

def get_duration(apath):
    r = subprocess.run(
        [ffmpeg, "-i", str(apath), "-hide_banner"],
        capture_output=True, text=True
    )
    for line in r.stderr.split("\n"):
        if "Duration:" in line:
            m = re.search(r"Duration: (\d+):(\d+):(\d+)\.(\d+)", line)
            if m:
                return int(m.group(1))*3600 + int(m.group(2))*60 + int(m.group(3)) + 0.5
    return None

clip_durations = []
for af in audio_files:
    ap = SLIDES_DIR / af
    dur = get_duration(ap)
    clip_durations.append(dur if dur else 10)
    print(f"  {af}: {dur}s")

# ============================================================
# 生成带音频的视频片段（时长精确匹配音频）
# ============================================================
print("生成视频片段...")
clips = []
for i, (sf, af, dur) in enumerate(zip(slides, audio_files, clip_durations)):
    sp = SLIDES_DIR / sf
    ap = SLIDES_DIR / af
    cp = SLIDES_DIR / f"clip_{i:02d}.mp4"
    
    if os.path.exists(ap) and os.path.getsize(ap) > 2000:
        cmd = [
            ffmpeg, "-loop", "1", "-i", str(sp),
            "-i", str(ap),
            "-filter_complex",
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fade=t=out:st={dur-1.5}:d=1.5,setsar=1[v];[1:a]afade=t=out:st={dur-0.5}:d=0.5[a]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(dur), "-r", "30",
            "-shortest", "-y", str(cp)
        ]
    else:
        cmd = [
            ffmpeg, "-loop", "1", "-i", str(sp),
            "-vf", f"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fade=t=out:st={dur-1.5}:d=1.5",
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-t", str(dur), "-r", "30", "-y", str(cp)
        ]
    
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(cp):
        clips.append(str(cp))
        print(f"  clip_{i:02d}.mp4 OK ({os.path.getsize(cp)} bytes)")
    else:
        print(f"  clip_{i:02d} error: {r.stderr[-200:] if r.stderr else 'unknown'}")

# ============================================================
# 合并（加淡入淡出）
# ============================================================
if clips:
    cl = SLIDES_DIR / "clips.txt"
    with open(cl, "w", encoding="utf-8") as f:
        for c in clips: f.write(f"file '{c}'\n")
    
    merge_cmd = [
        ffmpeg, "-f", "concat", "-safe", "0", "-i", str(cl),
        "-vf", "fade=t=in:st=0:d=0.5,fade=t=out:st=0:d=0.5",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-y", str(OUTPUT_VIDEO)
    ]
    r = subprocess.run(merge_cmd, capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(OUTPUT_VIDEO):
        sz = os.path.getsize(OUTPUT_VIDEO)
        print(f"DONE: {OUTPUT_VIDEO} ({sz} bytes)")
    else:
        print(f"merge error: {r.stderr[-200:] if r.stderr else 'unknown'}")

print("done")