# -*- coding: utf-8 -*-
"""Assemble daily news video - auto duration based on audio."""
import subprocess
import os

FFMPEG = "C:/Program Files/AutoClaw/resources/python/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
OUT = "C:/Users/Administrator/.openclaw-autoclaw/workspace/covers_v4"
AUDIO = OUT + "/audio"

SLIDES = [
    "slide_00_cover.png",
    "slide_01_content.png",
    "slide_02_content.png",
    "slide_03_content.png",
    "slide_99_end.png",
]
AUDIOS = [
    "narration_00.mp3",
    "narration_01.mp3",
    "narration_02.mp3",
    "narration_03.mp3",
    "narration_04.mp3",
]

def get_duration(path):
    cmd = [FFMPEG, "-i", path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    for line in r.stderr.split("\n"):
        if "Duration:" in line:
            # Parse HH:MM:SS.ms
            dur = line.split("Duration:")[1].split(",")[0].strip()
            parts = dur.split(":")
            seconds = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
            return seconds
    return 10

def main():
    segs = []
    durations = []

    for i in range(len(SLIDES)):
        sp = OUT + "/" + SLIDES[i]
        ap = AUDIO + "/" + AUDIOS[i]
        dur = get_duration(ap)
        durations.append(dur)
        out = OUT + "/seg_%02d.mp4" % i
        print("Process %d/%d | Audio duration: %.2fs" % (i+1, len(SLIDES), dur))

        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", sp,
            "-i", ap,
            "-c:v", "libx264",
            "-t", str(dur),
            "-pix_fmt", "yuv420p",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            "-c:a", "aac",
            "-preset", "fast",
            out
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0:
            print("  OK")
            segs.append(out)
        else:
            print("  FAIL")

    # Merge
    output = OUT + "/daily_news_20260512_v2.mp4"
    total = sum(durations)

    # Build filter_complex for concat with audio
    fc_in = ""
    for i in range(len(segs)):
        fc_in += "[" + str(i) + ":v][" + str(i) + ":a]"
    fc = fc_in + "concat=n=" + str(len(segs)) + ":v=1:a=1[v][a]"

    cmd = [FFMPEG, "-y"]
    for seg in segs:
        cmd += ["-i", seg]
    cmd += [
        "-filter_complex", fc,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "fast",
        output
    ]

    print("Merging %d segments (total %.0fs)..." % (len(segs), total))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        print("Done: " + output)
    else:
        print("FAIL: " + r.stderr[:300])

if __name__ == "__main__":
    main()
