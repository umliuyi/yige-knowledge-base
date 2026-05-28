import subprocess, os

ffmpeg = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
base = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v3"

segs = [os.path.join(base, f"seg_{i}.mp4") for i in range(4)]
seg_files = [s for s in segs if os.path.exists(s)]

# Check each segment
for s in seg_files:
    info = subprocess.run([ffmpeg, "-i", s], capture_output=True, text=True)
    # Extract duration line
    for line in info.stderr.split("\n"):
        if "Duration" in line:
            print(f"{os.path.basename(s)}: {line.strip()}")
            break

# Use filter_complex for high-quality re-encode concat
list_file = os.path.join(base, "segments3.txt")
with open(list_file, "w") as f:
    for s in seg_files:
        f.write(f"file '{s}'\n".replace("\\", "/"))

out = os.path.join(base, "daily_news_20260511_v7.mp4")

# Method: use concat with re-encode at higher quality
cmd = [
    ffmpeg, "-y",
    "-f", "concat", "-safe", "0", "-i", list_file,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart",
    out
]
print("Running FFmpeg concat (re-encode)...")
r = subprocess.run(cmd, capture_output=True, text=True)
print("RC:", r.returncode)
if r.returncode != 0:
    print("Stderr:", r.stderr[-800:] if r.stderr else "")
if os.path.exists(out):
    sz = os.path.getsize(out)
    print(f"Output: {sz//1024}KB ({sz//1024//1024}MB)")
else:
    print("FAILED - output not created")
