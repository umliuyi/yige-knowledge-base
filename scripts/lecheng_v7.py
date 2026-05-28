#!/usr/bin/env python3
"""
Lecheng Daily News v7 - 完整内容配音版
每条新闻：热点事件(2-3句) + 乐城影响(2句) + 精算视角(1句) → 作为配音全文
"""
from PIL import Image, ImageDraw, ImageFont
import os, asyncio, edge_tts, subprocess

SOURCE = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\日报\2026-05-11-早报-乐城视角.md"
OUT = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v3"
FFMPEG = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
os.makedirs(OUT, exist_ok=True)

W, H = 1920, 1080
BG=(6,8,20); ORG=(255,107,30); WHT=(255,255,255); GRY=(140,145,160)

def fnt(size):
    for p in ["C:/Windows/Fonts/msyh.ttc","C:/Windows/Fonts/simhei.ttf"]:
        try: return ImageFont.truetype(p,size)
        except: pass
    return ImageFont.load_default()

def grad(img):
    d=ImageDraw.Draw(img)
    for y in range(H):
        r=int(6*(1-y/H)+2*y/H); g=int(8*(1-y/H)+4*y/H); b=int(20*(1-y/H)+12*y/H)
        d.line([(0,y),(W,y)],fill=(r,g,b))

def page(title="", sub="", body=None, footer="", page_dur=12):
    img=Image.new("RGB",(W,H),BG); grad(img); d=ImageDraw.Draw(img)
    d.rectangle([(0,0),(W,4)],fill=ORG)
    y=80
    if title: d.text((80,y),title,font=fnt(48),fill=ORG); y+=88
    if sub: d.text((80,y),sub,font=fnt(24),fill=GRY); y+=48
    if body:
        for ln in body: d.text((80,y),ln,font=fnt(22),fill=WHT); y+=44
    if footer: d.text((80,H-60),footer,font=fnt(16),fill=GRY)
    return img

def parse_full():
    """解析完整新闻内容用于配音"""
    with open(SOURCE, encoding="utf-8") as f: c=f.read()
    
    pages = []
    # 封面
    pages.append({
        "t": "乐城视角 · 大健康早报",
        "s": "2026年5月11日",
        "b": [],
        "f": "刘一 · 精算师聊健康",
        "dur": 5,
        "nar": "乐城视角，大健康早报，2026年5月11日。关注我，获取更多乐城医疗资讯。"
    })
    
    # 提取两条新闻
    idx1 = c.find("新闻一："); idx2 = c.find("新闻二：")
    
    news_blocks = [
        ("新闻一", c[idx1:idx2] if idx1>=0 and idx2>=0 else ""),
        ("新闻二", c[idx2:] if idx2>=0 else "")
    ]
    
    for name, block in news_blocks:
        if not block: continue
        lines = block.split("\n")
        
        title = ""; event = ""; impact = ""; actuary = ""
        section = ""
        
        for ln in lines:
            ln = ln.strip()
            if not ln or ln.startswith("---") or ln.startswith("#"):
                continue
            if "新闻" in ln and "：" in ln:
                title = ln.split("：")[1].split("，")[0].split("（")[0].strip()
            elif "**热点事件**" in ln:
                section = "event"
            elif "**对乐城的影响**" in ln:
                section = "impact"
            elif "**精算视角**" in ln:
                section = "actuary"
            elif section == "event" and ln:
                event += ln.replace("**","").strip() + "。"
            elif section == "impact" and ln:
                impact += ln.replace("**","").strip() + "。"
            elif section == "actuary" and ln:
                actuary += ln.replace("**","").strip()
        
        if not title: continue
        
        # 完整配音文本：标题 + 热点 + 影响 + 精算
        nar_parts = [title + "。"]
        if event: nar_parts.append(event)
        if impact: nar_parts.append("对乐城的影响。" + impact)
        if actuary: nar_parts.append("精算视角。" + actuary)
        narration = "".join(nar_parts)
        
        # 显示在幻灯片上的body（截取精华，2-3行）
        display_body = []
        if event: display_body.append(event[:60])
        if impact: display_body.append(impact[:60])
        if len(display_body) > 3: display_body = display_body[:3]
        
        pages.append({
            "title": title,
            "sub": "",
            "body": display_body,
            "footer": "刘一 · 精算师聊健康",
            "dur": 12,
            "narration": narration
        })
    
    # 结尾
    pages.append({
        "title": "感谢观看",
        "sub": "关注我，获取更多乐城医疗资讯",
        "body": [],
        "footer": "刘一 · 精算师聊健康",
        "dur": 5,
        "narration": "感谢观看。关注我，获取更多乐城医疗资讯。"
    })
    
    return pages

async def gen_audio(text, out):
    if len(text.strip()) < 5: return False
    try:
        await edge_tts.Communicate(text, voice="zh-CN-YunxiNeural").save(out)
        return True
    except Exception as e:
        print(f"  Audio err: {e}")
        return False

async def gen_all(pages):
    results = []
    for i, pg in enumerate(pages):
        txt = pg.get("narration","")
        out = os.path.join(OUT, f"na{i}.wav")
        ok = await gen_audio(txt, out)
        char_count = len(txt)
        results.append((out if ok else None, char_count))
        print(f"  [{i}] {'OK' if ok else 'SKIP'} {char_count}chars: {txt[:40]}...")
    return results

def get_dur(path):
    if not path or not os.path.exists(path): return 0
    r = subprocess.run([FFMPEG,"-i",path], capture_output=True, text=True)
    for ln in r.stderr.split("\n"):
        if "Duration:" in ln:
            try: return float(ln.split("Duration:")[1].split(",")[0].strip().split(":")[2])
            except: pass
    return 0

def make_seg(slide_path, audio_path, target_dur, out_path):
    has_audio = audio_path and os.path.exists(audio_path)
    
    if has_audio:
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
        print(f"  Seg[{out_path}] FFmpeg err: {r.stderr[-200:]}")
        return False
    return True

def concat(segs, out):
    flist = os.path.join(OUT, "flist2.txt")
    with open(flist, "w") as f:
        for s in segs:
            if s and os.path.exists(s):
                f.write("file '" + s.replace("\\","/") + "'\n")
    
    cmd = [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", flist, "-c", "copy", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Concat err: {r.stderr[-200:]}")
        return False
    return True

def main():
    print("=== Lecheng v7 (full narration) ===")
    pages = parse_full()
    print(f"Pages: {len(pages)}, target: {sum(pg['dur'] for pg in pages)}s")
    
    # Generate slides
    slides = []
    for i, pg in enumerate(pages):
        img = page(pg["t"], pg["s"], pg["b"], pg["f"])
        p = os.path.join(OUT, f"pg{i}.png")
        img.save(p); slides.append(p)
        print(f"  Slide[{i}]: {pg['t'][:30]}")
    
    # Generate full narration audio
    print("Generating narration audio...")
    audio_results = asyncio.run(gen_all(pages))
    
    # Check durations
    print("Checking audio vs target durations:")
    for i, ((ap, chars), pg) in enumerate(zip(audio_results, pages)):
        ad = get_dur(ap) if ap else 0
        print(f"  [{i}] audio={ad:.1f}s target={pg['d']}s chars={chars}")
    
    # Make segments
    segs = []
    for i, ((ap, chars), pg) in enumerate(zip(audio_results, pages)):
        seg = os.path.join(OUT, f"seg7_{i}.mp4")
        ok = make_seg(slides[i], ap if ap else None, pg["d"], seg)
        if ok and os.path.exists(seg):
            segs.append(seg)
            print(f"  Seg[{i}]: {os.path.getsize(seg)//1024}KB")
        else:
            segs.append(None)
    
    # Concat
    final = os.path.join(OUT, "daily_news_20260511_v7.mp4")
    concat(segs, final)
    if os.path.exists(final):
        total_dur = sum(pg["dur"] for pg in pages)
        print(f"Done: {os.path.getsize(final)//1024}KB, target={total_dur}s")

if __name__ == "__main__":
    main()
