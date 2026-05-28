# -*- coding: utf-8 -*-
"""Assemble daily news video from slides and audio."""
import subprocess
import os

FFMPEG = "C:/Program Files/AutoClaw/resources/python/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
OUT = "C:/Users/Administrator/.openclaw-autoclaw/workspace/covers_v4"
AUDIO = OUT + "/audio"

SLIDES = [
    ("slide_00_cover.png", "narration_00.mp3"),
    ("slide_01_content.png", "narration_01.mp3"),
    ("slide_02_content.png", "narration_02.mp3"),
    ("slide_03_content.png", "narration_03.mp3"),
    ("slide_99_end.png", "narration_04.mp3"),
]

DUR = [10, 10, 10, 10, 10]

def run_cmd(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0, r.stderr

def main():
    segs = []
    for i, (slide, audio) in enumerate(SLIDES):
        sp = OUT + "/" + slide
        ap = AUDIO + "/" + audio
        out = OUT + "/seg_%02d.mp4" % i
        print("Process %d/%d" % (i+1, len(SLIDES)))
        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", sp,
            "-i", ap,
            "-c:v", "libx264",
            "-t", str(DUR[i]),
            "-pix_fmt", "yuv420p",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            "-c:a", "aac", "-shortest",
            "-preset", "fast",
            out
        ]
        ok, err = run_cmd(cmd)
        if ok:
            print("  OK")
            segs.append(out)
        else:
            print("  FAIL: " + err[:100])
    
    if len(segs) < 2:
        print("Not enough segments")
        return
    
    output = OUT + "/daily_news_20260512.mp4"
    
    # Build filter_complex
    fc_in = ""
    for i in range(len(segs)):
        fc_in += "[" + str(i) + ":v][" + str(i) + ":a]"
    fc = fc_in + "concat=n=" + str(len(segs)) + ":v=1:a=1[v][a]"
    
    cmd = [FFMPEG, "-y"]
    for seg in segs:
        cmd += ["-i", seg]
    cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", output]
    
    print("Merging " + str(len(segs)) + " segments...")
    ok, err = run_cmd(cmd)
    if ok:
        print("Done: " + output)
    else:
        print("Merge FAIL: " + err[:300])

if __name__ == "__main__":
    main()
