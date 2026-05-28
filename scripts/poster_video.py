"""
用海报图生成视频：静态图 + TTS配音
"""
import subprocess, os

IMG  = r"C:\Users\Administrator\Downloads\daily_poster_1of5.png"
AUDIO = r"C:\Users\Administrator\Downloads\daily_news.mp3"
OUT  = r"C:\Users\Administrator\Downloads\daily_poster_video.mp4"

FFMPEG = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

# Step 1: generate TTS
import edge_tts
import asyncio

TEXT = """
乐城早报，2026年5月14日。我是刘一，北美精算师。

480万，中国人每年新发癌症。其中不到30%能用上新药。

原因一，海外新药国内未批。
原因二，普通家庭无力承担。
结果，等不起，也用不起。

健康的人不算账。
关注我，用精算师的眼睛，看懂大健康。
海南博鳌乐城先行区。
"""

async def gen_audio():
    tts = edge_tts.Communicate(TEXT, voice="zh-CN-YunxiNeural", rate="-15%")
    await tts.save(AUDIO)
    print(f"Audio saved: {os.path.getsize(AUDIO)//1024}KB")

asyncio.run(gen_audio())

# Step 2: build video (loop image to audio duration)
cmd = [
    FFMPEG, "-y",
    "-loop", "1", "-i", IMG,
    "-i", AUDIO,
    "-c:v", "libx264", "-tune", "stillimage",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    "-movflags", "+faststart",
    OUT
]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("FFmpeg error:", r.stderr[-500:])
else:
    print(f"Done: {os.path.getsize(OUT)//1024}KB")