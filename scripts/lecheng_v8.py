#!/usr/bin/env python3
"""Lecheng Daily News v8 - clean, complete narration"""
from PIL import Image, ImageDraw, ImageFont
import os, asyncio, edge_tts, subprocess

SRC = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\日报\2026-05-11-早报-乐城视角.md"
OUT = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v3"
FFMPEG = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
os.makedirs(OUT, exist_ok=True)

W, H = 1920, 1080
C_BG = (6, 8, 20); C_ORG = (255, 107, 30); C_WHT = (255, 255, 255); C_GRY = (140, 145, 160)

def fnt(size):
    for p in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def draw_bg(img):
    d = ImageDraw.Draw(img)
    for y in range(H):
        r = int(6*(1-y/H) + 2*y/H)
        g = int(8*(1-y/H) + 4*y/H)
        b = int(20*(1-y/H) + 12*y/H)
        d.line([(0, y), (W, y)], fill=(r, g, b))

def make_slide(title, sub, body_lines, footer):
    img = Image.new("RGB", (W, H), C_BG)
    draw_bg(img)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 4)], fill=C_ORG)
    y = 80
    if title: d.text((80, y), title, font=fnt(46), fill=C_ORG); y += 88
    if sub: d.text((80, y), sub, font=fnt(22), fill=C_GRY); y += 46
    if body_lines:
        for ln in body_lines:
            d.text((80, y), ln, font=fnt(21), fill=C_WHT); y += 43
    if footer: d.text((80, H-60), footer, font=fnt(15), fill=C_GRY)
    return img

def parse_news():
    with open(SRC, encoding="utf-8") as f:
        content = f.read()

    slides_data = []

    # 0: Cover
    slides_data.append({
        "title": "乐城视角 · 大健康早报",
        "sub": "2026年5月11日",
        "body": [],
        "footer": "刘一 · 精算师聊健康",
        "dur": 6,
        "nar": "乐城视角，大健康早报，2026年5月11日。"
    })

    # Find news sections
    pos1 = content.find("新闻一：")
    pos2 = content.find("新闻二：")

    for start, end in [(pos1, pos2), (pos2, len(content))]:
        if start < 0: continue
        block = content[start:end]
        lines = block.split("\n")

        title = ""
        section = ""
        event_text = ""
        impact_text = ""
        actuary_text = ""

        for ln in lines:
            ln = ln.strip()
            if not ln or ln.startswith("---"): continue
            if "新闻" in ln and "：" in ln:
                title = ln.split("：")[1].split("，")[0].split("（")[0].strip()
            elif "**热点事件**" in ln:
                section = "event"
            elif "**对乐城的影响**" in ln:
                section = "impact"
            elif "**精算视角**" in ln:
                section = "actuary"
            elif "**" in ln:
                section = ""
            else:
                clean = ln.replace("**", "")
                if section == "event" and clean:
                    event_text += clean + "。"
                elif section == "impact" and clean:
                    impact_text += clean + "。"
                elif section == "actuary" and clean:
                    actuary_text += clean

        if not title: continue

        # Build narration: title + event + impact + actuary
        nar_parts = [title + "。"]
        if event_text: nar_parts.append(event_text)
        if impact_text: nar_parts.append("对乐城的影响。" + impact_text)
        if actuary_text: nar_parts.append("精算视角。" + actuary_text)
        narration = "".join(nar_parts)

        # Build slide body: first lines of each section
        body = []
        if event_text: body.append(event_text[:65])
        if impact_text: body.append(impact_text[:65])
        if actuary_text: body.append(actuary_text[:65])
        body = body[:3]

        slides_data.append({
            "title": title,
            "sub": "",
            "body": body,
            "footer": "刘一 · 精算师聊健康",
            "dur": 14,
            "nar": narration
        })

    # End slide
    slides_data.append({
        "title": "感谢观看",
        "sub": "关注我，获取更多乐城医疗资讯",
        "body": [],
        "footer": "刘一 · 精算师聊健康",
        "dur": 6,
        "nar": "感谢观看。关注我，获取更多乐城医疗资讯。"
    })

    return slides_data

async def gen_audio(text, out_path):
    if len(text.strip()) < 5:
        return False
    try:
        await edge_tts.Communicate(text, voice="zh-CN-YunxiNeural").save(out_path)
        return True
    except Exception as e:
        print(f"Audio error: {e}")
        return False

async def gen_all_audio(slides):
    tasks = []
    for i, sl in enumerate(slides):
        out = os.path.join(OUT, f"na{i}.wav")
        tasks.append(gen_audio(sl["nar"], out))
        print(f"  [{i}] Generating: {sl['nar'][:50]}...")
    results = await asyncio.gather(*tasks)
    return [os.path.join(OUT, f"na{i}.wav") if r else None
            for i, r in enumerate(results)]

def get_audio_duration(path):
    if not path or not os.path.exists(path): return 0
    r = subprocess.run([FFMPEG, "-i", path], capture_output=True, text=True)
    for ln in r.stderr.split("\n"):
        if "Duration:" in ln:
            try:
                t = ln.split("Duration:")[1].split(",")[0].strip()
                return float(t.split(":")[2])
            except: pass
    return 0

def make_segment(slide_path, audio_path, target_dur, out_path):
    if audio_path and os.path.exists(audio_path):
        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", slide_path,
            "-i", audio_path,
            "-filter_complex",
            "[0:v]loop=loop=-1:size=1,setpts=N/FRAME_RATE/TB,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v];[1:a]apad=whole_dur=" + str(target_dur) + "[a]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-pix_fmt", "yuv420p", "-r", "25",
            "-t", str(target_dur),
            "-c:a", "aac", "-b:a", "128k",
            out_path
        ]
    else:
        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", slide_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-pix_fmt", "yuv420p", "-r", "25",
            "-t", str(target_dur),
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
            out_path
        ]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  FFmpeg error: {r.stderr[-200:]}")
        return False
    return True

def concat_segments(segment_paths, out_path):
    flist = os.path.join(OUT, "flist3.txt")
    with open(flist, "w") as f:
        for p in segment_paths:
            if p and os.path.exists(p):
                f.write("file '" + p.replace("\\", "/") + "'\n")

    cmd = [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", flist, "-c", "copy", out_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Concat error: {r.stderr[-200:]}")
        return False
    return True

def main():
    print("=== Lecheng v8 ===")
    slides = parse_news()
    total_target = sum(s["dur"] for s in slides)
    print(f"Slides: {len(slides)}, target: {total_target}s")

    # 1. Make slides
    slide_paths = []
    for i, sl in enumerate(slides):
        img = make_slide(sl["title"], sl["sub"], sl["body"], sl["footer"])
        p = os.path.join(OUT, f"sl{i}.png")
        img.save(p)
        slide_paths.append(p)
        print(f"  Slide[{i}]: {sl['title'][:40]}")

    # 2. Generate audio
    print("Generating audio...")
    audio_paths = asyncio.run(gen_all_audio(slides))

    # 3. Report audio durations
    for i, (ap, sl) in enumerate(zip(audio_paths, slides)):
        ad = get_audio_duration(ap) if ap else 0
        print(f"  Audio[{i}]: {ad:.1f}s / target {sl['dur']}s ({len(sl['nar'])}chars)")

    # 4. Make segments
    segs = []
    for i, (sp, ap, sl) in enumerate(zip(slide_paths, audio_paths, slides)):
        seg = os.path.join(OUT, f"seg8_{i}.mp4")
        ok = make_segment(sp, ap, sl["dur"], seg)
        if ok and os.path.exists(seg):
            segs.append(seg)
            print(f"  Segment[{i}]: {os.path.getsize(seg)//1024}KB")
        else:
            segs.append(None)

    # 5. Concat
    final = os.path.join(OUT, "daily_news_20260511_v8.mp4")
    concat_segments(segs, final)
    if os.path.exists(final):
        sz = os.path.getsize(final)
        print(f"Final: {sz//1024}KB ({sz//1024//1024}MB)")
    else:
        print("FAILED - final video not created")

if __name__ == "__main__":
    main()
