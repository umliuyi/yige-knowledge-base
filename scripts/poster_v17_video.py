"""v17视频"""
import subprocess, os, asyncio, edge_tts

IMG   = r"C:\Users\Administrator\Downloads\daily_poster_v17.png"
AUDIO = r"C:\Users\Administrator\Downloads\daily_news_v17.mp3"
OUT   = r"C:\Users\Administrator\Downloads\daily_poster_v17_video.mp4"
FFMPEG = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

TEXT = """乐城早报，2026年5月14日。我是刘一，北美精算师。

药品管理法实施条例，明天正式施行。市场独占期制度落地，进口新药加速进入乐城。

精算师视角：15款国产一类新药，1到4月密集获批。29个乐城生物医学新技术已批准，收费体系建立中。818号令正式施行，细胞治疗进入监管时代。ADC赛道爆发，中国进入全面爆发期。

关注我，用精算师的眼睛，看懂大健康。海南博鳌乐城先行区。
"""

async def main():
    await edge_tts.Communicate(TEXT, voice="zh-CN-YunxiNeural", rate="-15%").save(AUDIO)
    cmd = [FFMPEG, "-y", "-loop", "1", "-i", IMG, "-i", AUDIO,
           "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
           "-c:v", "libx264", "-tune", "stillimage",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-shortest", "-movflags", "+faststart", OUT]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("ERR:", r.stderr[-400:])
    else:
        print(f"Done: {os.path.getsize(OUT)//1024}KB")

asyncio.run(main())