import subprocess, os

ffmpeg = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
base = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v3"
out = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v3\daily_news_20260511_v8.mp4"

segs = [os.path.join(base, f"seg_{i}.mp4") for i in range(4)]

# Write concat list with forward slashes
list_file = os.path.join(base, "segments5.txt")
with open(list_file, "w") as f:
    for s in segs:
        f.write("file '" + s.replace("\\", "/") + "'\n")

print("List:", open(list_file).read())

# Method: stream copy (fast, no re-encode)
cmd = [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", out]
print("Running stream copy concat...")
r = subprocess.run(cmd, capture_output=True, text=True)
print("RC:", r.returncode)
if r.returncode != 0:
    print("Stderr:", r.stderr[-500:] if r.stderr else "")
if os.path.exists(out):
    print("Size:", os.path.getsize(out) // 1024, "KB")
