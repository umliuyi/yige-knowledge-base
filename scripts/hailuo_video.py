#!/usr/bin/env python3
"""
MiniMax 海螺AI 视频生成自动化脚本
用法: python hailuo_video.py
"""
import urllib.request
import urllib.error
import json
import time
import os
import sys

# ============ 配置区 ============
API_KEY = "sk-api-6UprnKT6vp6gFgoquJtFx3FKcC-03AJ3E8wv6BRZNiDPh9VwWoWOmer_L-F14JtIsTghCbhEcKDK1jQpKlpnoeLOoTmXW46Z7P5AJ5UaKdKvIl9wRuaNJzU"
BASE_URL = "https://api.minimax.io"
OUTPUT_DIR = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\videos"
# ==============================

os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_video(prompt, filename):
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
        task_id = result.get("task_id")
        print(f"  提交成功: task_id={task_id}")
        return task_id
    except Exception as e:
        print(f"  提交失败: {e}")
        return None

def query_video(task_id):
    """查询视频生成状态"""
    req = urllib.request.Request(
        f"{BASE_URL}/v1/video_generation/{task_id}",
        headers={"Authorization": f"Bearer {API_KEY}"},
        method="GET"
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        return result
    except Exception as e:
        print(f"  查询失败: {e}")
        return None

def get_download_url(file_id):
    """获取视频下载链接"""
    req = urllib.request.Request(
        f"{BASE_URL}/v1/files/retrieve?file_id={file_id}",
        headers={"Authorization": f"Bearer {API_KEY}"},
        method="GET"
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        return result
    except Exception as e:
        print(f"  获取下载链接失败: {e}")
        return None

def wait_for_video(task_id, timeout=120, interval=10):
    """等待视频生成完成"""
    start = time.time()
    while time.time() - start < timeout:
        result = query_video(task_id)
        if result:
            status = result.get("status", "")
            print(f"  状态: {status}")
            if status == "SUCCESS":
                file_id = result.get("file_id")
                if file_id:
                    dl_result = get_download_url(file_id)
                    if dl_result:
                        download_url = dl_result.get("download_url")
                        return download_url
                # 尝试从result直接拿URL
                if "video_url" in result:
                    return result["video_url"]
                return file_id
            elif status in ["FAIL", "ERROR"]:
                print(f"  生成失败: {result}")
                return None
        time.sleep(interval)
    print("  超时")
    return None

def download_file(url, filepath):
    """下载文件"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0"
        })
        resp = urllib.request.urlopen(req, timeout=60)
        with open(filepath, "wb") as f:
            f.write(resp.read())
        print(f"  下载完成: {filepath}")
        return True
    except Exception as e:
        print(f"  下载失败: {e}")
        return False

if __name__ == "__main__":
    # 测试连接
    print("测试API连接...")
    test_req = urllib.request.Request(
        f"{BASE_URL}/v1/models",
        headers={"Authorization": f"Bearer {API_KEY}"},
        method="GET"
    )
    try:
        resp = urllib.request.urlopen(test_req, timeout=15)
        print("API连接正常")
    except Exception as e:
        print(f"API连接失败: {e}")
