import subprocess, os
from pathlib import Path

SLIDES_DIR = Path(r"C:\Users\Administrator\Downloads\videos\daily_news")
OUTPUT = SLIDES_DIR / "daily_news_20260526.mp4"
FFMPEG = None
try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except:
    FFMPEG = "ffmpeg"

slides = ["00_cover.png", "01_diabetes.png", "02_data.png", "03_knee.png", "99_closing.png"]
audio_files = ["audio_00.mp3", "audio_01.mp3", "audio_02.mp3", "audio_03.mp3", "audio_04.mp3"]
durations = [8, 15, 15, 15, 8]

clips = []
for i, (sf, af, dur) in enumerate(zip(slides, audio_files, durations)):
    spath = SLIDES_DIR / sf
    apath = SLIDES_DIR / af
    clip_path = SLIDES_DIR / f"clip_{i:02d}.mp4"
    
    if os.path.exists(apath) and os.path.getsize(apath) > 5000:
        cmd = [
            FFMPEG, "-loop", "1", "-i", str(spath),
            "-i", str(apath),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-t", str(dur), "-r", "30",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-y", str(clip_path)
        ]
    else:
        cmd = [
            FFMPEG, "-loop", "1", "-i", str(spath),
            "-vf", f"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-t", str(dur), "-r", "30", "-y", str(clip_path)
        ]
    
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(clip_path):
        clips.append(str(clip_path))
        print(f"clip_{i:02d}.mp4 OK ({os.path.getsize(clip_path)} bytes)")
    else:
        print(f"clip_{i:02d} error: {r.stderr[-150:] if r.stderr else 'unknown'}")

if clips:
    cl = SLIDES_DIR / "clips_final.txt"
    with open(cl, "w", encoding="utf-8") as f:
        for c in clips: f.write(f"file '{c}'\n")
    merge_cmd = [FFMPEG, "-f", "concat", "-safe", "0", "-i", str(cl),
                 "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                 "-pix_fmt", "yuv420p", "-y", str(OUTPUT)]
    r = subprocess.run(merge_cmd, capture_output=True, text=True)
    if r.returncode == 0 and os.path.exists(OUTPUT):
        print(f"DONE: {OUTPUT} ({os.path.getsize(OUTPUT)} bytes)")
    else:
        print(f"merge error: {r.stderr[-200:] if r.stderr else 'unknown'}")

print("done")