# 精算师视角早报视频生成器
import os, re, asyncio, subprocess, sys, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

TODAY = sys.argv[1] if len(sys.argv) > 1 else "2026-05-26"
SLIDES_DIR = Path(r"C:\Users\Administrator\Downloads\videos\daily_news")
SLIDES_DIR.mkdir(exist_ok=True)
WORKSPACE = Path(r"C:\Users\Administrator\.openclaw-autoclaw\workspace")
SOURCE_MD = WORKSPACE / "growth" / "daily" / "ccfa1206" / f"{TODAY}.md"
OUTPUT_VIDEO = SLIDES_DIR / f"daily_news_{TODAY.replace('-','')}.mp4"

BG = (8, 8, 18)
ORANGE = (255, 87, 34)
WHITE = (255, 255, 255)
GRAY = (160, 160, 170)
W, H = 1920, 1080

def font(size, bold=False):
    for p in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/simsun.ttc"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def draw_slide(title=None, body_lines=None, footer=None, tag=None):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 6)], fill=ORANGE)
    if title:
        d.text((80, 50), title, font=font(38, True), fill=ORANGE)
    if body_lines:
        y = 130
        for line in body_lines:
            for chunk in [line[i:i+45] for i in range(0, len(line), 45)]:
                d.text((80, y), chunk, font=font(26), fill=WHITE)
                y += 46
    if footer:
        d.text((80, H-70), footer, font=font(20), fill=GRAY)
    if tag:
        tw = d.textlength(tag, font=font(20)) if hasattr(d, 'textlength') else len(tag)*20
        d.text((W - tw - 80, H-70), tag, font=font(20), fill=GRAY)
    return img

with open(SOURCE_MD, "r", encoding="utf-8") as f:
    content = f.read()

# 解析章节
sections = []
for block in re.split(r"## 【(.+?)】", content):
    block = block.strip()
    if not block: continue
    parts = block.split("\n", 1)
    if len(parts) == 2:
        title, body = parts
        body = re.sub(r"来源：.*", "", body).strip()
        body = "。".join([p.strip() for p in body.split("。") if p.strip()])
        sections.append((title, body))
    elif len(parts) == 1 and sections:
        # continuation of previous body
        sections[-1] = (sections[-1][0], sections[-1][1] + body)

print(f"[INFO] 章节数: {len(sections)}")

# 生成封面
cover = draw_slide(
    title="精算师视角 · 早报",
    body_lines=["2026年5月26日", "糖尿病 · 膝关节 · 干细胞"],
    footer="刘一｜精算师聊健康",
    tag="#乐城医疗 #精算师视角"
)
cover.save(SLIDES_DIR / "00_cover.png")
print("[OK] 封面")

# 生成内容页
slide_files = ["00_cover.png"]
audio_texts = []

for i, (title, body) in enumerate(sections):
    chars_per = 44
    lines = []
    for para in re.split(r"[。；]", body):
        para = para.strip()
        if not para: continue
        while len(para) > chars_per:
            lines.append(para[:chars_per])
            para = para[chars_per:]
        if para: lines.append(para)
    
    img = draw_slide(
        title=f"  {title}",
        body_lines=lines[:9],
        footer="刘一｜精算师聊健康",
        tag=f"第{i+1}条/共{len(sections)}条"
    )
    fname = f"0{i+1}_content.png"
    img.save(SLIDES_DIR / fname)
    slide_files.append(fname)
    audio_texts.append(body)
    print(f"[OK] {fname}")

# 结尾页
end_img = draw_slide(
    title="关注我",
    body_lines=["用精算师的眼光", "看懂大健康"],
    footer="刘一｜精算师聊健康",
    tag="#订阅"
)
end_img.save(SLIDES_DIR / "99_closing.png")
slide_files.append("99_closing.png")
audio_texts.append("关注我，用精算师的眼光，看懂大健康。刘一，精算师聊健康。")
print("[OK] 结尾")

# TTS配音
async def gen_tts(text, out_path):
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, "zh-CN-YunxiNeural")
        await communicate.save(out_path)
        return os.path.exists(out_path)
    except Exception as e:
        print(f"  TTS error: {e}")
        return False

async def main_tts():
    print("生成配音...")
    audio_files = []
    for i, text in enumerate(audio_texts):
        afile = SLIDES_DIR / f"audio_{i:02d}.mp3"
        ok = await gen_tts(str(afile), text)
        if ok:
            audio_files.append(str(afile))
            print(f"  TTS OK: audio_{i:02d}.mp3")
        else:
            audio_files.append(None)
        await asyncio.sleep(0.3)
    return audio_files

audio_files = asyncio.run(main_tts())

# 视频合成
print("合成视频...")
ffmpeg = None
try:
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
except:
    ffmpeg = "ffmpeg"

durations = [8] + [12]*len(sections) + [8]  # 封面8s 内容12s 结尾8s

clips = []
for i, (sf, dur) in enumerate(zip(slide_files, durations)):
    spath = SLIDES_DIR / sf
    clip_path = SLIDES_DIR / f"clip_{i:02d}.mp4"
    cmd = [
        ffmpeg, "-loop", "1", "-i", str(spath),
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
        "-t", str(dur), "-r", "30", "-y", str(clip_path)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(clip_path):
        clips.append(str(clip_path))
        print(f"  clip_{i:02d}.mp4 OK")
    else:
        print(f"  clip error: {r.stderr[-150:] if r.stderr else 'unknown'}")

if clips:
    cl = SLIDES_DIR / "clips.txt"
    with open(cl, "w") as f:
        for c in clips: f.write(f"file '{c}'\n")
    merge_cmd = [ffmpeg, "-f", "concat", "-safe", "0", "-i", str(cl), "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-y", str(OUTPUT_VIDEO)]
    r = subprocess.run(merge_cmd, capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(OUTPUT_VIDEO):
        size = os.path.getsize(OUTPUT_VIDEO)
        print(f"✅ 完成: {OUTPUT_VIDEO} ({size} bytes)")
    else:
        print(f"merge error: {r.stderr[-200:] if r.stderr else 'unknown'}")
else:
    print("❌ 没有生成任何clip")

print("done")