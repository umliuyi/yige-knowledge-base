# -*- coding: utf-8 -*-
"""
Lecheng Daily News AB Test v2 - pre-trim audio before video gen
"""
from PIL import Image, ImageDraw, ImageFont
import os, asyncio, edge_tts, subprocess, shutil

SRC    = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\日报\2026-05-11-早报-乐城视角.md"
BASE   = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v3"
FFMPEG = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

os.makedirs(os.path.join(BASE, "A_version"), exist_ok=True)
os.makedirs(os.path.join(BASE, "B_version"), exist_ok=True)

W, H = 1920, 1080
C_BG  = (6, 8, 20)
C_ORG = (255, 107, 30)
C_WHT = (255, 255, 255)
C_GRY = (140, 145, 160)

def fnt(size):
    for p in [r"C:/Windows/Fonts/msyh.ttc", r"C:/Windows/Fonts/simhei.ttf"]:
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
    if title:
        d.text((80, y), title, font=fnt(46), fill=C_ORG); y += 88
    if sub:
        d.text((80, y), sub, font=fnt(22), fill=C_GRY); y += 46
    if body_lines:
        for ln in body_lines:
            d.text((80, y), ln, font=fnt(21), fill=C_WHT); y += 43
    if footer:
        d.text((80, H-60), footer, font=fnt(15), fill=C_GRY)
    return img

SLIDES_DEF = [
    {
        "title": "乐城视角 · 大健康早报", "sub": "2026年5月11日",
        "body": [], "footer": "刘一 · 精算师聊健康", "dur": 5,
        "nar_A": "大家好，今天是5月11号，来看今天的乐城视角大健康早报。",
        "nar_B": "乐城视角，大健康早报，2026年5月11日。",
    },
    {
        "title": "正大天晴×GSK乙肝新药战略合作",
        "sub": "乐城先行区政策能否加速进口新药落地？",
        "body": ["正大天晴与GSK合作，推动乙肝新药bepirovirsen进入内地",
                 "乐城真实世界数据通道可为该药提供加速审评的桥梁",
                 "目标群体约300-500万人，年治疗费用6-8万元"],
        "footer": "刘一 · 精算师聊健康", "dur": 14,
        # ~130 chars at -30% rate ≈ 14s
        "nar_A": (
            "先说个大事。正大天晴和葛兰素史克搞了个战略合作，要把一款乙肝新药"
            "bepirovirsen引进中国内地。这药如果能进乐城，对那边的医疗机构和患者来说，"
            "都是个大机会。中国大概有7000万乙肝感染者，符合这药条件的大概300到500万人。"
            "假设乐城能承接其中1%，一年下来特药收入能有小几个亿。"
        ),
        # ~130 chars at -25% rate ≈ 14s
        "nar_B": (
            "正大天晴与葛兰素史克达成战略合作，共同推动乙肝新药bepirovirsen进入中国内地市场。"
            "这一合作意味着，乐城先行区的特许药械政策将有机会加速该药的落地应用。"
            "对乐城医疗机构而言，这是一个值得主动对接的商业机遇。"
            "从精算视角来看，乙肝患者群体庞大，乐城若能承接1%，特药收入相当可观。"
        ),
    },
    {
        "title": "进口化妆品电子标签新规落地海南",
        "sub": "跨境消费医疗产品合规门槛大幅提升",
        "body": ["12月1日起全国施行进口化妆品电子标签制度",
                 "海南离岛免税化妆品年销售额约80-120亿元",
                 "乐城可借医疗资质背书，打造医疗级消费护肤新定位"],
        "footer": "刘一 · 精算师聊健康", "dur": 14,
        # ~130 chars at -30% rate ≈ 14s
        "nar_A": (
            "再来看一条。进口化妆品要开始搞电子标签了，12月开始全国施行。"
            "海南作为自贸港，这一块本来就很活跃。对乐城来说，这既是压力也是机会。"
            "如果能借着医疗资质背书，把普通跨境购升级成医疗级消费护肤，"
            "对中高端客群的吸引力会更强。这一块潜在的增量市场一年能有几个亿。"
        ),
        # ~120 chars at -25% rate ≈ 14s
        "nar_B": (
            "进口化妆品电子标签新规落地海南，12月起全国施行。"
            "海南离岛免税化妆品年销售额巨大，新规对乐城消费医疗板块既是合规压力，也是差异化机会。"
            "若能通过医疗级溯源标签吸引中高端客群，年增收潜力显著。"
        ),
    },
    {
        "title": "感谢观看", "sub": "关注我，获取更多乐城医疗资讯",
        "body": [], "footer": "刘一 · 精算师聊健康", "dur": 5,
        "nar_A": "今天的早报就到哪里，关注我，获取更多乐城医疗资讯。",
        "nar_B": "感谢观看，关注我获取更多乐城医疗资讯。",
    },
]

async def gen_audio(text, out_path, voice, rate="-15%"):
    try:
        await edge_tts.Communicate(text, voice=voice, rate=rate).save(out_path)
        return True
    except Exception as e:
        print(f"  Audio error [{out_path}]: {e}")
        return False

async def gen_all_audio(slides, version, voice, rate):
    out_dir = os.path.join(BASE, f"{version}_version")
    tasks = []
    for i, sl in enumerate(slides):
        out = os.path.join(out_dir, f"raw_na{i}.wav")
        tasks.append(gen_audio(sl[f"nar_{version}"], out, voice, rate))
        print(f"  [{version}][{i}] {sl['nar_'+version][:50]}...")
    results = await asyncio.gather(*tasks)
    return [os.path.join(out_dir, f"raw_na{i}.wav") if r else None
            for i, r in enumerate(results)]

def get_duration(path):
    if not path or not os.path.exists(path): return 0
    r = subprocess.run([FFMPEG, "-i", path], capture_output=True, text=True)
    for ln in r.stderr.split("\n"):
        if "Duration:" in ln:
            try: return float(ln.split("Duration:")[1].split(",")[0].strip().split(":")[2])
            except: pass
    return 0

def trim_audio(in_path, out_path, target_dur):
    """Trim or pad audio to exactly target_dur seconds."""
    # First get actual duration
    actual = get_duration(in_path)
    if actual <= 0:
        print(f"  trim_audio: cannot read duration for {in_path}")
        return False

    if abs(actual - target_dur) < 0.5:
        # Close enough, just copy
        shutil.copy2(in_path, out_path)
        return True

    if actual > target_dur:
        # Trim: use atrim to cut to target_dur
        cmd = [
            FFMPEG, "-y", "-i", in_path,
            "-af", f"atrim=0:{target_dur}", "-vn",
            "-c:a", "pcm_s16le", "-ar", "44100", "-ac", "2",
            out_path
        ]
    else:
        # Pad: apad to extend to target_dur
        cmd = [
            FFMPEG, "-y", "-i", in_path,
            "-af", f"apad=whole_dur={target_dur}", "-vn",
            "-c:a", "pcm_s16le", "-ar", "44100", "-ac", "2",
            out_path
        ]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  trim_audio error: {r.stderr[-200:]}")
        return False
    dur = get_duration(out_path)
    print(f"  trimmed {actual:.1f}s -> {dur:.1f}s (target {target_dur}s)")
    return True

def make_segment(slide_path, audio_path, target_dur, out_path):
    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-i", slide_path,
        "-i", audio_path,
        "-filter_complex",
        "[0:v]loop=loop=-1:size=1,setpts=N/FRAME_RATE/TB,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v]",
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-pix_fmt", "yuv420p", "-r", "25",
        "-t", str(target_dur),
        "-c:a", "aac", "-b:a", "128k",
        out_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  FFmpeg error: {r.stderr[-300:]}")
        return False
    return True

def concat_segments(segment_paths, out_path):
    flist = os.path.join(BASE, "flist_ab.txt")
    with open(flist, "w", encoding="utf-8") as f:
        for p in segment_paths:
            if p and os.path.exists(p):
                f.write("file '" + p.replace("\\", "/") + "'\n")
    cmd = [FFMPEG, "-y", "-f", "concat", "-safe", "0",
           "-i", flist, "-c", "copy", out_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Concat error: {r.stderr[-300:]}")
        return False
    return True

def main():
    print("=" * 60)
    print("Lecheng Daily News AB Test v2")
    print("=" * 60)

    # Step 1: Slides
    print("\n[Step 1] Generating slides...")
    for i, sl in enumerate(SLIDES_DEF):
        img = make_slide(sl["title"], sl["sub"], sl["body"], sl["footer"])
        for version in ["A", "B"]:
            img.save(os.path.join(BASE, f"{version}_version", f"sl{i}.png"))
        print(f"  Slide[{i}]: {sl['title'][:45]}")

    # Step 2: Raw audio generation
    print("\n[Step 2] Generating raw audio...")
    print("  A: zh-CN-YunxiNeural @ -30% (slower, chatty)")
    print("  B: zh-CN-YunyangNeural @ -25% (normal, professional)")
    raw_A = asyncio.run(gen_all_audio(SLIDES_DEF, "A", "zh-CN-YunxiNeural", "-30%"))
    raw_B = asyncio.run(gen_all_audio(SLIDES_DEF, "B", "zh-CN-YunyangNeural", "-25%"))

    # Report raw durations
    print("\n  Raw audio durations:")
    for i, sl in enumerate(SLIDES_DEF):
        dA = get_duration(raw_A[i]) if raw_A[i] else 0
        dB = get_duration(raw_B[i]) if raw_B[i] else 0
        print(f"  [{i}] A={dA:.1f}s B={dB:.1f}s / target={sl['dur']}s")

    # Step 3: Trim audio to target duration
    print("\n[Step 3] Trimming audio to target durations...")
    trim_A = []
    trim_B = []
    for i, sl in enumerate(SLIDES_DEF):
        out_A = os.path.join(BASE, "A_version", f"na{i}.wav")
        out_B = os.path.join(BASE, "B_version", f"na{i}.wav")
        ok_A = trim_audio(raw_A[i], out_A, sl["dur"]) if raw_A[i] else False
        ok_B = trim_audio(raw_B[i], out_B, sl["dur"]) if raw_B[i] else False
        trim_A.append(out_A if ok_A else None)
        trim_B.append(out_B if ok_B else None)
        print(f"  [{i}] A:{ok_A} B:{ok_B}")

    # Step 4: Generate video segments
    print("\n[Step 4] Generating video segments...")
    segs_A = []
    for i, sl in enumerate(SLIDES_DEF):
        sp = os.path.join(BASE, "A_version", f"sl{i}.png")
        ap = trim_A[i]
        seg = os.path.join(BASE, "A_version", f"seg_{i}.mp4")
        ok = make_segment(sp, ap, sl["dur"], seg) if ap else False
        if ok and os.path.exists(seg):
            segs_A.append(seg)
            sz = os.path.getsize(seg)
            print(f"  [A][{i}] OK {sz//1024}KB ({sz//1024//1024}MB)")
        else:
            segs_A.append(None)

    segs_B = []
    for i, sl in enumerate(SLIDES_DEF):
        sp = os.path.join(BASE, "B_version", f"sl{i}.png")
        ap = trim_B[i]
        seg = os.path.join(BASE, "B_version", f"seg_{i}.mp4")
        ok = make_segment(sp, ap, sl["dur"], seg) if ap else False
        if ok and os.path.exists(seg):
            segs_B.append(seg)
            sz = os.path.getsize(seg)
            print(f"  [B][{i}] OK {sz//1024}KB ({sz//1024//1024}MB)")
        else:
            segs_B.append(None)

    # Step 5: Concat
    print("\n[Step 5] Concatenating...")
    final_A = os.path.join(BASE, "A_version", "daily_news_20260511_A.mp4")
    final_B = os.path.join(BASE, "B_version", "daily_news_20260511_B.mp4")

    ok_A = concat_segments(segs_A, final_A)
    ok_B = concat_segments(segs_B, final_B)

    print("\n" + "=" * 60)
    if ok_A and os.path.exists(final_A):
        sz = os.path.getsize(final_A)
        print(f"A版 OK: {final_A}  ({sz//1024//1024}MB)")
    else:
        print("A版 FAILED")
    if ok_B and os.path.exists(final_B):
        sz = os.path.getsize(final_B)
        print(f"B版 OK: {final_B}  ({sz//1024//1024}MB)")
    else:
        print("B版 FAILED")
    print("=" * 60)

if __name__ == "__main__":
    main()
