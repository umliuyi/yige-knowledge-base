# -*- coding: utf-8 -*-
"""Check audio durations."""
import subprocess

FFMPEG = "C:/Program Files/AutoClaw/resources/python/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
AUDIO_DIR = "C:/Users/Administrator/.openclaw-autoclaw/workspace/covers_v4/audio"

files = [
    "narration_00.mp3",
    "narration_01.mp3",
    "narration_02.mp3",
    "narration_03.mp3",
    "narration_04.mp3",
]

for f in files:
    path = AUDIO_DIR + "/" + f
    cmd = [FFMPEG, "-i", path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    # Parse duration from stderr
    for line in r.stderr.split("\n"):
        if "Duration:" in line:
            print(f + ": " + line.strip())
            break
