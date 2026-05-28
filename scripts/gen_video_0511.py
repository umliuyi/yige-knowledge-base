# -*- coding: utf-8 -*-
import os, wave, math, subprocess

OUTPUT_DIR = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11"
FFMPEG = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

files = os.listdir(OUTPUT_DIR)
png_files = sorted([f for f in files if f.endswith('.png')])
mp3_files = sorted([f for f in files if f.endswith('.mp3')])

print("PNG files:", png_files)
print("MP3 files:", mp3_files)

def get_duration(mp3_file):
    path = os.path.join(OUTPUT_DIR, mp3_file)
    try:
        with wave.open(path) as w:
            return w.getnframes() / w.getframerate()
    except:
        return 3.0

ordered_png = png_files  # 00_cover, 01_xxx, 02_xxx, ..., 99_closing
ordered_mp3 = ["cover.mp3", "01.mp3", "02.mp3", "03.mp3", "04.mp3", "05.mp3", "99.mp3"]

concat_path = os.path.join(OUTPUT_DIR, "concat.txt")
concat_f = open(concat_path, "w", encoding="utf-8")

for i, (png, mp3) in enumerate(zip(ordered_png, ordered_mp3)):
    dur = get_duration(mp3)
    img_dur = max(dur + 0.3, 3.5)
    seg_path = os.path.join(OUTPUT_DIR, f"seg_{i:02d}.mp4")
    
    png_path = os.path.join(OUTPUT_DIR, png)
    mp3_path = os.path.join(OUTPUT_DIR, mp3)
    
    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-i", png_path,
        "-i", mp3_path,
        "-t", f"{img_dur:.2f}",
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-shortest",
        seg_path
    ]
    
    print(f"\n--- 片段 {i+1}: {png} + {mp3} ({img_dur:.1f}s) ---")
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"  FFmpeg 错误: {result.stderr[-500:]}")
    else:
        print(f"  OK: {seg_path}")
    
    concat_f.write(f"file '{seg_path}'\n")

concat_f.close()

# 拼接最终视频
output = os.path.join(OUTPUT_DIR, "daily_news_20260511.mp4")
final_cmd = [
    FFMPEG, "-y",
    "-f", "concat", "-safe", "0", "-i", concat_path,
    "-c", "copy",
    output
]
print(f"\n=== 拼接最终视频 ===")
result = subprocess.run(final_cmd, capture_output=True)
if result.returncode != 0:
    print(f"错误: {result.stderr[-500:]}")
else:
    print(f"完成! 输出: {output}")