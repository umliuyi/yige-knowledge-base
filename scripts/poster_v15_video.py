"""v15视频 - 强制像素比9:16，不拉伸"""
import subprocess, os, asyncio, edge_tts

IMG   = r"C:\Users\Administrator\Downloads\daily_poster_v15.png"
AUDIO = r"C:\Users\Administrator\Downloads\daily_news_v15.mp3"
OUT   = r"C:\Users\Administrator\Downloads\daily_poster_v15_video.mp4"
FFMPEG = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

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

async def main():
    await edge_tts.Communicate(TEXT, voice="zh-CN-YunxiNeural", rate="-15%").save(AUDIO)
    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-i", IMG,
        "-i", AUDIO,
        "-vf", "scale=1080:1920,setsar=1:1",
        "-c:v", "libx264", "-tune", "stillimage",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", OUT
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("ERR:", r.stderr[-400:])
    else:
        print(f"Done: {os.path.getsize(OUT)//1024}KB")

asyncio.run(main())