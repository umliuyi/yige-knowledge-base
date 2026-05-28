import subprocess, os, asyncio, edge_tts
from PIL import Image, ImageDraw, ImageFont

SOURCE = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\日报\2026-05-11-早报-乐城视角.md"
OUT = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v3"
FFMPEG = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
os.makedirs(OUT, exist_ok=True)

W, H = 1920, 1080
BG = (6,8,20); ORANGE = (255,107,30); WHITE = (255,255,255); GRAY = (140,145,160)

def fnt(size):
    for p in ["C:/Windows/Fonts/msyh.ttc","C:/Windows/Fonts/simhei.ttf"]:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def bg(img):
    d = ImageDraw.Draw(img)
    for y in range(H):
        r = int(6*(1-y/H)+2*y/H); g = int(8*(1-y/H)+4*y/H); b = int(20*(1-y/H)+12*y/H)
        d.line([(0,y),(W,y)], fill=(r,g,b))

def slide(title="", sub="", body=None, footer=""):
    img = Image.new("RGB",(W,H),BG); bg(img); d = ImageDraw.Draw(img)
    d.rectangle([(0,0),(W,4)],fill=ORANGE)
    y=80
    if title: d.text((80,y),title,font=fnt(52),fill=ORANGE); y+=90
    if sub: d.text((80,y),sub,font=fnt(26),fill=GRAY); y+=55
    if body:
        for ln in body: d.text((80,y),ln,font=fnt(24),fill=WHITE); y+=48
    if footer: d.text((80,H-60),footer,font=fnt(18),fill=GRAY)
    return img

def parse():
    with open(SOURCE, encoding="utf-8") as f: c = f.read()
    pages = []
    pages.append({"t":"乐城视角 · 大健康早报","s":"2026年5月11日","b":[],"f":"刘一 · 精算师聊健康","d":6})
    idx1=c.find("新闻一："); idx2=c.find("新闻二：")
    for a,b in [(idx1,idx2),(idx2,len(c))]:
        if a<0: continue
        sec=c[a:b]; lines=sec.split("\n"); title=""; body=[]; cap=False
        for ln in lines:
            if "新闻" in ln and "：" in ln:
                title=ln.split("：")[1].split("，")[0].split("（")[0].strip(); cap=True; continue
            if "**" in ln: cap=False; continue
            if ln.startswith("---"): continue
            if cap and ln.strip():
                cln=ln.strip().replace("**","").strip()
                if cln: body.append(cln[:90])
        if title:
            pages.append({"t":title,"s":"","b":body[:4],"f":"刘一 · 精算师聊健康","d":12})
    pages.append({"t":"感谢观看","s":"关注我，获取更多乐城医疗资讯","b":[],"f":"刘一 · 精算师聊健康","d":6})
    return pages

async def gen_audio(text, out, voice="zh-CN-YunxiNeural"):
    if len(text.strip())<3: return False
    try:
        await edge_tts.Communicate(text, voice).save(out)
        return True
    except: return False

async def all_audio(pages):
    results = []
    for i, pg in enumerate(pages):
        parts=[pg.get("t",""), pg.get("s","")]
        parts.extend(pg.get("b",[]))
        txt="，".join([p for p in parts if p])
        if not txt: txt="请观看"
        out=os.path.join(OUT, f"a{i}.wav")
        ok=await gen_audio(txt, out)
        results.append(out if ok else None)
        print(f"  Audio[{i}]: {'OK' if ok else 'SKIP'} ({len(txt)}chars)")
    return results

def dur(path):
    if not path or not os.path.exists(path): return 0
    cmd=[FFMPEG,"-i",path]; r=subprocess.run(cmd,capture_output=True,text=True)
    for ln in r.stderr.split("\n"):
        if "Duration:" in ln:
            try: return float(ln.split("Duration:")[1].split(",")[0].strip().split(":")[2])
            except: pass
    return 0

def make12s_slide_audio(slide_path, audio_path, duration, output):
    """生成12秒片段：图片循环12秒 + 音频完整播放"""
    aflag = ["-i", audio_path] if (audio_path and os.path.exists(audio_path)) else []
    
    # 用filter让图片持续12秒，音频完整播放
    if aflag:
        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", slide_path,
            "-i", audio_path,
            "-filter_complex",
            "[0:v]loop=loop=-1:size=1,setpts=N/FRAME_RATE/TB,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=000000,setsar=1[v];[1:a]apad=whole_dur=" + str(duration) + "[a]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-pix_fmt", "yuv420p", "-r", "25",
            "-t", str(duration),
            "-c:a", "aac", "-b:a", "128k",
            output
        ]
    else:
        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", slide_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-pix_fmt", "yuv420p", "-r", "25",
            "-t", str(duration),
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
            output
        ]
    
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0

def concat_final(seg_files, output):
    list_file = os.path.join(OUT, "flist.txt")
    with open(list_file, "w") as f:
        for s in seg_files:
            if s and os.path.exists(s):
                f.write("file '" + s.replace("\\", "/") + "'\n")
    
    cmd = [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", list_file,
           "-c", "copy", output]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("Concat err:", r.stderr[-400:])
    return r.returncode == 0

def main():
    print("=== Lecheng v6 ===")
    pages = parse()
    print(f"Pages: {len(pages)}, total ~{sum(p['d'] for p in pages)}s")
    
    # Slides
    slide_paths = []
    for i, pg in enumerate(pages):
        img = slide(pg["t"], pg["s"], pg["b"], pg["f"])
        p = os.path.join(OUT, f"sl{i}.png")
        img.save(p); slide_paths.append(p)
    
    # Audio - need to pad to full duration
    print("Audio...")
    audio_paths = asyncio.run(all_audio(pages))
    
    # Check audio durations
    for i, (ap, pg) in enumerate(zip(audio_paths, pages)):
        if ap: print(f"  Audio[{i}] dur={dur(ap):.1f}s, page dur={pg['d']}s")
    
    # Segments - each exactly page duration
    segs = []
    for i, (sp, ap, pg) in enumerate(zip(slide_paths, audio_paths, pages)):
        seg = os.path.join(OUT, f"segment_{i}.mp4")
        ok = make12s_slide_audio(sp, ap, pg["d"], seg)
        if ok and os.path.exists(seg):
            segs.append(seg)
            sz = os.path.getsize(seg) // 1024
            print(f"  Segment[{i}]: {pg['d']}s, {sz}KB")
        else:
            segs.append(None)
    
    # Concat
    final = os.path.join(OUT, "daily_news_20260511_v6.mp4")
    concat_final(segs, final)
    if os.path.exists(final):
        print(f"Final: {os.path.getsize(final)//1024}KB, {sum(p['d'] for p in pages)}s target")

if __name__ == "__main__":
    main()
