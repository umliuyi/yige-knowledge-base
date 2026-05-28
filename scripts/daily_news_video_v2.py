#!/usr/bin/env python3
"""
早报视频生成 - 乐城视角 v2
"""
import os, asyncio, subprocess

SLIDES_DIR = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v2"
TEMP_AUDIO = os.path.join(SLIDES_DIR, "audio_temp")
os.makedirs(TEMP_AUDIO, exist_ok=True)

FFMPEG = r"C:\Program Files\AutoClaw\resources\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

VOICE = "zh-CN-YunxiNeural"
RATE = "-10%"
PITCH = "+0Hz"

SLIDE_DUR = {
    "00_cover.png":  4,
    "01_正大天晴GSK战.png": 10,
    "02_进口化妆品电子标.png": 10,
    "03_data.png":  8,
    "04_data.png":  8,
    "99_closing.png": 4,
}

slide_info = [
    ("00_cover.png",  None),
    ("01_正大天晴GSK战.png",  "01"),
    ("02_进口化妆品电子标.png", "02"),
    ("03_data.png",   "03"),
    ("04_data.png",   "04"),
    ("99_closing.png", "05"),
]

narration = {
    "01": "正大天晴与GSK达成战略合作，推动乙肝新药bepirovirsen入华。乐城先行区特许药械政策，正好适用这类境外已上市新药。乐城真实世界数据通道可为该药提供加速审评。从精算视角看，7000万感染者中目标群体约300到500万人，按人均年治疗费6到8万元测算，乐城承接1%即可带来1.8到4亿元年收入，净利率25%到35%。",
    "02": "海关总署修订进出口化妆品检验检疫办法，上海率先试点电子标签，12月1号起全国施行。乐城若率先建立先行区特供化妆品追溯体系，可将普通跨境购升级为医疗级消费护肤。海南离岛免税化妆品年销售额80到120亿元，若乐城获取5%到10%的中高端客群增量，对应年增收4到12亿元。",
    "03": "中国现有约7000万乙肝病毒感染者。目标人群约300到500万，年治疗费6到8万元。乐城若承接1%，年新增特药收入1.8到4亿元，净利率25%到35%。",
    "04": "海南离岛免税化妆品年销售额约80到120亿元。乐城若获5%到10%的中高端客群增量，对应年增收4到12亿元。",
    "05": "感谢观看。刘一，精算师聊健康，乐城视角，每早8点30分更新。",
}

def safe_decode(data):
    if data is None:
        return ""
    try:
        return data.decode("utf-8", errors="replace")
    except Exception:
        return str(data)

async def generate_audio(seg_id, text):
    from edge_tts import Communicate
    wav = os.path.join(TEMP_AUDIO, f"seg_{seg_id}.wav")
    cm = Communicate(text, voice=VOICE, rate=RATE, pitch=PITCH)
    await cm.save(wav)
    print(f"  配音: seg_{seg_id}.wav")
    return wav

async def main():
    print("="*50)
    print("Step 1: 生成配音...")

    # 逐个生成，失败重试1次
    for fname, seg_id in slide_info:
        if seg_id and seg_id in narration:
            for attempt in range(2):
                try:
                    await generate_audio(seg_id, narration[seg_id])
                    break
                except Exception as e:
                    if attempt == 0:
                        print(f"  seg_{seg_id} 失败，重试: {e}")
                        await asyncio.sleep(2)
                    else:
                        print(f"  seg_{seg_id} 最终失败: {e}")
            await asyncio.sleep(0.3)
    print("配音完成\n")

    print("Step 2: 生成视频片段...")
    concat_entries = []

    for fname, seg_id in slide_info:
        img_path = os.path.join(SLIDES_DIR, fname)
        target_dur = SLIDE_DUR[fname]
        seg_out = os.path.join(TEMP_AUDIO, f"seg_{seg_id}.mp4")
        wav_path = os.path.join(TEMP_AUDIO, f"seg_{seg_id}.wav") if seg_id and seg_id in narration else None

        if wav_path and os.path.exists(wav_path):
            cmd = [
                FFMPEG, "-y",
                "-loop", "1", "-i", img_path,
                "-stream_loop", "-1", "-i", wav_path,
                "-c:v", "libx264", "-preset", "fast", "-crf", "22",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
                "-t", str(target_dur),
                "-shortest",
                "-tune", "stillimage",
                seg_out
            ]
        else:
            cmd = [
                FFMPEG, "-y",
                "-loop", "1", "-i", img_path,
                "-c:v", "libx264", "-preset", "fast", "-crf", "22",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
                "-t", str(target_dur),
                "-tune", "stillimage",
                seg_out
            ]

        print(f"  {fname} ({target_dur}s)...", end=" ")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"OK")
            concat_entries.append(seg_out)
        else:
            err = safe_decode(result.stderr)[-150:]
            print(f"失败: {err}")

    if not concat_entries:
        print("没有可用片段!")
        return

    print("\nStep 3: 拼接最终视频...")
    concat_list = os.path.join(TEMP_AUDIO, "concat_list3.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for seg in concat_entries:
            f.write(f"file '{seg}'\n")

    OUTPUT_MP4 = os.path.join(SLIDES_DIR, "daily_news_20260511_v2.mp4")
    cmd = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        OUTPUT_MP4
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        size = os.path.getsize(OUTPUT_MP4)
        total_dur = sum(SLIDE_DUR[f] for f, _ in slide_info)
        print(f"\n✅ 完成!")
        print(f"   {OUTPUT_MP4}")
        print(f"   大小: {size/1024/1024:.1f} MB | 预计时长: {total_dur}s ({total_dur/60:.1f}min)")
    else:
        print(f"❌ 拼接失败")

if __name__ == "__main__":
    asyncio.run(main())