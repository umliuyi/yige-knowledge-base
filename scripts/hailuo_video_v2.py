#!/usr/bin/env python3
"""
MiniMax 海螺AI 视频生成 - 完整自动化脚本 v2
用法: python hailuo_video_v2.py
"""
import urllib.request
import urllib.error
import json
import time
import os
import sys
import imageio_ffmpeg

# ============ 配置区 ============
API_KEY = "sk-api-UTv9N1XfUYjJLBWtHRhSnR45eCaRlTyqOBaf4QSV2zV5SZSfFksEihkHaqdkuH44WLHVwveZnPIJV0BwDGPVFeZcg6VQb0eJErx8T0uyhJdd_oISKuu4gBk"
BASE_URL = "https://api.minimaxi.com"
OUTPUT_DIR = r"C:\Users\Administrator\Downloads\videos"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
TTS_FILE = r"C:\Users\Administrator\Downloads\voiceover.mp3"
# ==============================

os.makedirs(OUTPUT_DIR, exist_ok=True)

PROMPTS = [
    # Shard 1: 开场揭秘 - 精算师办公室
    "A Chinese actuary in a dark modern office, cinematic documentary lighting, multiple data screens showing financial statistics, camera slowly pushing in towards a screen displaying the number 4.8 million, dramatic atmosphere, film grain",
    # Shard 2: 转折 - 海南乐城
    "Aerial drone view of tropical Hainan coastline at golden hour, modern medical buildings in Lecheng Pilot Zone, palm trees, golden sunlight, cinematic drone shot, documentary style, lush greenery",
    # Shard 3: 算账 - 数据可视化
    "Data visualization animation in dark space, giant glowing red numbers appearing one by one: 4.8 million, 30 percent, 5 to 10 times, heartbeat pulse animation, dramatic cinematic documentary style, music building",
    # Shard 4: 金句 - 健康的人不算账
    "Dark black background, elegant white Chinese text slowly fading in: '健康的人不算账，生病的人才算', minimalist cinematic typography, stark contrast, dramatic pause, minimalist art film style",
    # Shard 5: 升华 - 乐城医院
    "Modern medical facility in Lecheng Hainan, doctors in white coats working with advanced medical equipment, international pharmaceutical packaging with customs labels, patients receiving treatment in clean hospital rooms, cinematic documentary, hopeful atmosphere",
    # Shard 6: 钩子收尾
    "Dark cinematic background, minimalist ending card, elegant white Chinese text: '刘一 | 精算师聊健康', subtle glow effect, elegant fade to black, documentary style closing, minimalist",
]

def create_video(prompt, idx):
    """提交视频生成任务"""
    payload = {
        "prompt": prompt,
        "model": "MiniMax-Hailuo-2.3",
        "duration": 6,
        "resolution": "768P"
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/v1/video_generation",
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        task_id = result.get("task_id", "")
        print(f"  片段{idx+1}: task_id={task_id}")
        return task_id
    except Exception as e:
        print(f"  片段{idx+1}: 提交失败 {e}")
        return None

def wait_for_video(task_id, idx, timeout=180):
    """等待视频生成完成"""
    start = time.time()
    interval = 8
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(
                f"{BASE_URL}/v1/query/video_generation?task_id={task_id}",
                headers={"Authorization": f"Bearer {API_KEY}"},
                method="GET"
            )
            resp = urllib.request.urlopen(req, timeout=30)
            result = json.loads(resp.read())
            status = result.get("status", "")
            elapsed = int(time.time() - start)
            print(f"  片段{idx+1}: [{elapsed}s] {status}")
            if status == "Success":
                return result
            if status in ["FAIL", "ERROR"]:
                print(f"  片段{idx+1}: 生成失败 {result}")
                return None
        except Exception as e:
            print(f"  片段{idx+1}: 查询失败 {e}")
        time.sleep(interval)
    print(f"  片段{idx+1}: 超时")
    return None

def download_video(url, path):
    """下载视频"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=60)
        with open(path, "wb") as f:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                f.write(chunk)
        return os.path.getsize(path)
    except Exception as e:
        print(f"  下载失败: {e}")
        return None

def concat_videos(video_files, output_file, ffmpeg_path):
    """FFmpeg合并视频+音频"""
    import subprocess
    # Build concat list file
    list_file = output_file + ".list.txt"
    with open(list_file, "w") as f:
        for vf in video_files:
            f.write(f"file '{vf}'\n")
    # Run ffmpeg concat
    cmd = [
        ffmpeg_path, "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-i", TTS_FILE,
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac",
        "-shortest",
        "-y", output_file
    ]
    print(f"  合并中: {output_file}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("  FFmpeg错误:", result.stderr[-300:])
        return False
    os.remove(list_file)
    return True

def main():
    print("=" * 50)
    print("MiniMax 视频生成 - 6分镜自动化")
    print("=" * 50)
    
    video_files = []
    
    # Step 1: 批量提交6个任务
    print("\n[Step 1] 提交6个视频生成任务...")
    task_ids = []
    for i, prompt in enumerate(PROMPTS):
        print(f"\n--- 片段{i+1}/6 ---")
        tid = create_video(prompt, i)
        if tid:
            task_ids.append((i, tid))
        else:
            print(f"  片段{i+1} 提交失败，跳过")
    
    if not task_ids:
        print("没有任何任务提交成功，退出")
        return
    
    # Step 2: 等待所有任务完成
    print(f"\n[Step 2] 等待 {len(task_ids)} 个任务完成...")
    results = {}
    for idx, tid in task_ids:
        print(f"\n--- 查询片段{idx+1}: task_id={tid} ---")
        result = wait_for_video(tid, idx)
        if result:
            results[idx] = result
    
    # Step 3: 下载所有视频
    print(f"\n[Step 3] 下载 {len(results)} 个视频...")
    for idx, result in sorted(results.items()):
        file_id = result.get("file_id")
        if not file_id:
            print(f"  片段{idx+1}: 无file_id")
            continue
        out_path = os.path.join(OUTPUT_DIR, f"shard{idx+1}.mp4")
        print(f"  片段{idx+1}: file_id={file_id}")
        
        # Get download URL
        try:
            req = urllib.request.Request(
                f"{BASE_URL}/v1/files/retrieve?file_id={file_id}",
                headers={"Authorization": f"Bearer {API_KEY}"},
                method="GET"
            )
            resp = urllib.request.urlopen(req, timeout=30)
            dl_result = json.loads(resp.read())
            dl_url = dl_result.get("file", {}).get("download_url", "")
            print(f"  片段{idx+1}: 下载中...")
            size = download_video(dl_url, out_path)
            if size:
                print(f"  片段{idx+1}: 下载完成 {size:,} bytes")
                video_files.append(out_path)
            else:
                print(f"  片段{idx+1}: 下载失败")
        except Exception as e:
            print(f"  片段{idx+1}: 下载出错 {e}")
    
    if not video_files:
        print("没有视频下载成功，退出")
        return
    
    # Step 4: 合并视频+音频
    print(f"\n[Step 4] 合并 {len(video_files)} 个视频片段 + 音频...")
    final_output = os.path.join(OUTPUT_DIR, "final_video.mp4")
    if concat_videos(video_files, final_output, FFMPEG):
        size = os.path.getsize(final_output)
        print(f"\n✅ 成品完成: {final_output} ({size:,} bytes)")
    else:
        print("\n❌ 合并失败")

if __name__ == "__main__":
    main()
