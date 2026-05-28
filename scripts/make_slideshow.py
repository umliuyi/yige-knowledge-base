#!/usr/bin/env python3
"""幻灯片+配音 → 视频"""
import imageio_ffmpeg, subprocess, os

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
slides_dir = r"C:\Users\Administrator\Downloads\videos\slides"
audio = r"C:\Users\Administrator\Downloads\voiceover.mp3"
output = r"C:\Users\Administrator\Downloads\videos\slideshow_test.mp4"

slide_order = ["slide_cover.png", "slide_data.png", "slide_CAR-.png", "slide_closing.png"]

list_file = os.path.join(slides_dir, "concat_list.txt")
with open(list_file, "w") as f:
    for s in slide_order:
        path = os.path.join(slides_dir, s)
        if os.path.exists(path):
            f.write(f"file '{path}'\n")
            print(f"Added: {s}")

# Step 1: slides → video (1 frame every 8 seconds per slide)
cmd = [
    ffmpeg,
    "-f", "concat", "-safe", "0",
    "-i", list_file,
    "-framerate", "1/8",
    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
    "-y", output
]
print("Building video from slides...")
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("FFmpeg error:", result.stderr[-400:])
else:
    size = os.path.getsize(output)
    print(f"Slideshow created: {size:,} bytes ({size//1024}KB)")

# Step 2: add audio
output2 = output.replace(".mp4", "_with_audio.mp4")
cmd2 = [
    ffmpeg, "-i", output,
    "-i", audio,
    "-c:v", "copy", "-c:a", "aac",
    "-shortest", "-y", output2
]
print("Adding audio...")
result2 = subprocess.run(cmd2, capture_output=True, text=True)
if result2.returncode != 0:
    print("Audio merge error:", result2.stderr[-200:])
else:
    size2 = os.path.getsize(output2)
    print(f"With audio: {size2:,} bytes ({size2//1024}KB)")
    print("DONE!")
