#!/usr/bin/env python3
"""幻灯片+配音 → 视频 v2"""
import imageio_ffmpeg, subprocess, os

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
slides_dir = r"C:\Users\Administrator\Downloads\videos\slides"
audio = r"C:\Users\Administrator\Downloads\voiceover.mp3"
output = r"C:\Users\Administrator\Downloads\videos\slideshow_test_v2.mp4"

# Step 1: convert each PNG to a short MP4 clip (8s each) then concat
slide_files = ["slide_cover.png", "slide_data.png", "slide_CAR-.png", "slide_closing.png"]
clip_files = []

for i, sf in enumerate(slide_files):
    sf_path = os.path.join(slides_dir, sf)
    clip_path = os.path.join(slides_dir, f"clip_{i}.mp4")
    if not os.path.exists(sf_path):
        print(f"Missing: {sf_path}")
        continue
    cmd = [
        ffmpeg, "-loop", "1", "-i", sf_path,
        "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
        "-t", "8", "-r", "24",
        "-y", clip_path
    ]
    print(f"Encoding clip {i+1}: {sf}...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  Error: {r.stderr[-200:]}")
    else:
        size = os.path.getsize(clip_path)
        print(f"  Done: {size:,} bytes")
        clip_files.append(clip_path)

if not clip_files:
    print("No clips created!")
    exit(1)

# Step 2: concat clips
list_file = os.path.join(slides_dir, "clips.txt")
with open(list_file, "w") as f:
    for cf in clip_files:
        f.write(f"file '{cf}'\n")

video_only = output.replace(".mp4", "_video.mp4")
cmd2 = [
    ffmpeg,
    "-f", "concat", "-safe", "0", "-i", list_file,
    "-c:v", "libx264", "-preset", "fast",
    "-y", video_only
]
print("Merging clips...")
r2 = subprocess.run(cmd2, capture_output=True, text=True)
if r2.returncode != 0:
    print("Merge error:", r2.stderr[-200:])
else:
    print(f"Video only: {os.path.getsize(video_only):,} bytes")

# Step 3: add audio
cmd3 = [
    ffmpeg, "-i", video_only,
    "-i", audio,
    "-c:v", "copy", "-c:a", "aac",
    "-shortest", "-y", output
]
print("Adding audio...")
r3 = subprocess.run(cmd3, capture_output=True, text=True)
if r3.returncode != 0:
    print("Audio error:", r3.stderr[-200:])
else:
    final_size = os.path.getsize(output)
    print(f"Final: {final_size:,} bytes ({final_size//1024}KB)")
    print("DONE!")
