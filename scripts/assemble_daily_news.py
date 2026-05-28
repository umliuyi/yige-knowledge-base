#!/usr/bin/env python3
"""早报幻灯片 → 完整视频（7页版）"""
import asyncio, edge_tts, os, imageio_ffmpeg, subprocess, shutil

# ============ 配置 ============
SLIDES_DIR = r"C:\Users\Administrator\Downloads\videos\daily_news"
OUTPUT_DIR = SLIDES_DIR
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
# ============================

# 每张幻灯片的配音文本（与幻灯片内容匹配）
SLIDES_AUDIO = ["""关注我，每天早八点半，帮你算清楚大健康这笔账。刘一，精算师聊健康。"""]

SLIDE_DURATION = [8, 10, 10, 10, 10, 10, 8]  # 每页秒数

async def generate_tts(text, output_path, voice="zh-CN-YunxiNeural"):
    """生成单段配音"""
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        size = os.path.getsize(output_path)
        print(f"  TTS: {output_path} ({size} bytes)")
        return True
    except Exception as e:
        print(f"  TTS error: {e}")
        return False

async def main():
    print("=" * 50)
    print("Step 1: 生成7段配音...")
    audio_files = []
    for i, text in enumerate(SLIDES_AUDIO):
        out = os.path.join(SLIDES_DIR, f"audio_{i:02d}.mp3")
        ok = await generate_tts(text, out)
        if ok:
            audio_files.append(out)
        else:
            # Fallback: silent placeholder
            audio_files.append(None)
        await asyncio.sleep(0.3)

    print(f"\nStep 2: 生成视频片段...")
    clip_files = []
    slide_pngs = sorted([f for f in os.listdir(SLIDES_DIR) if f.endswith(".png")])
    print(f"  找到 {len(slide_pngs)} 张幻灯片: {slide_pngs}")

    for i, (png_file, dur) in enumerate(zip(slide_pngs, SLIDE_DURATION)):
        png_path = os.path.join(SLIDES_DIR, png_file)
        clip_path = os.path.join(SLIDES_DIR, f"clip_{i:02d}.mp4")
        print(f"  [{i+1}/{len(slide_pngs)}] {png_file} -> {dur}s")
        cmd = [
            FFMPEG, "-loop", "1", "-i", png_path,
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-t", str(dur), "-r", "24",
            "-y", clip_path
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"    Error: {r.stderr[-150:]}")
        else:
            size = os.path.getsize(clip_path)
            print(f"    Done: {size:,} bytes")
            clip_files.append(clip_path)

    if not clip_files:
        print("没有生成任何视频片段！")
        return

    print(f"\nStep 3: 拼接视频片段...")
    list_file = os.path.join(SLIDES_DIR, "clips.txt")
    with open(list_file, "w") as f:
        for cf in clip_files:
            f.write(f"file '{cf}'\n")

    video_only = os.path.join(OUTPUT_DIR, "daily_news_no_audio.mp4")
    cmd2 = [
        FFMPEG,
        "-f", "concat", "-safe", "0", "-i", list_file,
        "-c:v", "libx264", "-preset", "fast",
        "-y", video_only
    ]
    r2 = subprocess.run(cmd2, capture_output=True, text=True)
    if r2.returncode != 0:
        print(f"  拼接失败: {r2.stderr[-200:]}")
        return
    print(f"  视频: {os.path.getsize(video_only):,} bytes")

    print(f"\nStep 4: 合并所有配音音频...")
    # 先拼接所有音频
    concat_list = os.path.join(SLIDES_DIR, "audio_concat.txt")
    valid_audios = [af for af in audio_files if af and os.path.exists(af)]
    if valid_audios:
        with open(concat_list, "w") as f:
            for af in valid_audios:
                f.write(f"file '{af}'\n")
        combined_audio = os.path.join(OUTPUT_DIR, "combined_audio.mp3")
        cmd3 = [
            FFMPEG, "-f", "concat", "-safe", "0", "-i", concat_list,
            "-c:a", "mp3", "-y", combined_audio
        ]
        r3 = subprocess.run(cmd3, capture_output=True, text=True)
        if r3.returncode != 0:
            print(f"  音频拼接失败: {r3.stderr[-200:]}")
            # Use first audio as fallback
            audio_to_use = valid_audios[0]
        else:
            audio_to_use = combined_audio
            print(f"  音频合并: {os.path.getsize(combined_audio):,} bytes")
    else:
        print("  没有可用音频，跳过")
        audio_to_use = None

    print(f"\nStep 5: 最终合成...")
    final_output = os.path.join(OUTPUT_DIR, "daily_news_20260514.mp4")
    if audio_to_use and os.path.exists(audio_to_use):
        cmd4 = [
            FFMPEG, "-i", video_only,
            "-i", audio_to_use,
            "-c:v", "copy", "-c:a", "aac",
            "-shortest", "-y", final_output
        ]
    else:
        cmd4 = [
            FFMPEG, "-i", video_only,
            "-c:v", "copy",
            "-y", final_output
        ]
    r4 = subprocess.run(cmd4, capture_output=True, text=True)
    if r4.returncode != 0:
        print(f"  最终合成失败: {r4.stderr[-200:]}")
    else:
        size = os.path.getsize(final_output)
        print(f"\n{'='*50}")
        print(f"成品完成!")
        print(f"文件: {final_output}")
        print(f"大小: {size:,} bytes ({size//1024}KB)")

if __name__ == "__main__":
    asyncio.run(main())
