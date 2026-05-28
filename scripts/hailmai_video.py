#!/usr/bin/env python3
"""海螺MiniMax视频生成 - 发布级视频一键生成"""
import requests
import json
import os
import time
from datetime import datetime

API_KEY = "sk-api-UTv9N1XfUYjJLBWtHRhSnR45eCaRlTyqOBaf4QSV2zV5SZSfFksEihkHaqdkuH44WLHVwveZnPIJV0BwDGPVFeZcg6VQb0eJErx8T0uyhJdd_oISKuu4gBk"
API_URL = "https://api.minimax.chat/v1"
MODEL = "MiniMax-Hailuo-2.0-HD"

def generate_video(prompt, aspect_ratio="16:9", duration=6):
    """提交视频生成任务"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "duration": duration
    }
    resp = requests.post(
        f"{API_URL}/video_generation",
        headers=headers,
        json=payload,
        timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    if "data" not in data or "task_id" not in data.get("data", {}):
        raise Exception(f"API error: {data}")
    return data["data"]["task_id"]

def query_video(task_id):
    """查询视频生成状态"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    resp = requests.get(
        f"{API_URL}/query/video_generation",
        params={"task_id": task_id},
        headers=headers,
        timeout=10
    )
    resp.raise_for_status()
    return resp.json().get("data", {})

def download_video(file_id, output_path):
    """下载视频文件"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    resp = requests.get(
        f"{API_URL}/files/retrieve",
        params={"file_id": file_id},
        headers=headers,
        timeout=60
    )
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(resp.content)

def wait_for_video(task_id, timeout=120):
    """等待视频生成完成"""
    for _ in range(timeout // 5):
        status = query_video(task_id)
        state = status.get("status", "Unknown")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 状态: {state}")
        if state == "success":
            return status
        elif state in ("failed", "error"):
            raise Exception(f"生成失败: {status}")
        time.sleep(5)
    raise TimeoutError("等待超时")

def main():
    import sys
    if len(sys.argv) < 2:
        print("[用法] python hailmai_video.py '视频描述Prompt' [输出路径]")
        return
    prompt = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else f"video_{datetime.now().strftime('%H%M%S')}.mp4"
    output_dir = os.path.dirname(output) or os.getcwd()
    os.makedirs(output_dir, exist_ok=True)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 提交生成任务...")
    task_id = generate_video(prompt, aspect_ratio="16:9", duration=6)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 任务ID: {task_id}")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 等待生成...")
    status = wait_for_video(task_id)

    file_id = status.get("file_id")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 下载中: {file_id}")
    download_video(file_id, output)
    print(f"[OK] 视频已保存: {output}")

if __name__ == "__main__":
    main()
