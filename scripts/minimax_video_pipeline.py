"""
MiniMax 视频生成自动化流水线
===============================
完整流程：读取文本 → 提交视频生成任务 → 轮询状态 → 下载片段 → FFmpeg 合并 → 清理临时文件

用法：
    python minimax_video_pipeline.py <narration_file.txt> [output_video.mp4]

示例：
    python minimax_video_pipeline.py stories/episode1.txt
    python minimax_video_pipeline.py stories/episode1.txt output/final.mp4
"""

import sys
import os
import time
import requests
import tempfile
import shutil
from pathlib import Path

# ── API 配置 ────────────────────────────────────────────────────────────────
BASE_URL = "https://api.minimaxi.com"
API_KEY = "sk-api-UTv9N1XfUYjJLBWtHRhSnR45eCaRlTyqOBaf4QSV2zV5SZSfFksEihkHaqdkuH44WLHVwveZnPIJV0BwDGPVFeZcg6VQb0eJErx8T0uyhJdd_oISKuu4gBk"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# ── 工具函数 ────────────────────────────────────────────────────────────────

def submit_video_task(narration: str, duration: int = 6) -> str:
    """
    提交视频生成任务，返回 task_id
    POST /v1/video_generation
    """
    payload = {
        "model": "MiniMax-Hailuo-2.3",
        "text": narration,
        "duration": duration,
    }
    resp = requests.post(
        f"{BASE_URL}/v1/video_generation",
        headers=HEADERS,
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    task_id = data.get("task_id")
    if not task_id:
        raise RuntimeError(f"提交任务失败，响应缺少 task_id：{data}")
    return task_id


def query_task_status(task_id: str) -> dict:
    """
    查询任务状态，返回完整响应字典
    GET /v1/video_generation?task_id=xxx

    状态字段示例：
        status: "Pending" | "Processing" | "Success" | "Fail"
        file_id: 生成成功时有值，用于下载
    """
    resp = requests.get(
        f"{BASE_URL}/v1/video_generation",
        headers=HEADERS,
        params={"task_id": task_id},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def wait_for_completion(task_id: str, interval: int = 10, max_wait: int = 600) -> dict:
    """
    轮询直到任务完成（或超时）
    返回最终的 task 字典（含 file_id）
    """
    print(f"   等待任务完成，最长 {max_wait}s ...")
    elapsed = 0
    while elapsed < max_wait:
        result = query_task_status(task_id)
        status = result.get("status", "Unknown")
        print(f"   [{elapsed:>3}s] 状态: {status}")
        if status == "Success":
            return result
        if status == "Fail":
            raise RuntimeError(f"任务失败：{result}")
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(f"等待任务完成超时（{max_wait}s），task_id={task_id}")


def download_video(file_id: str, output_path: str) -> str:
    """
    下载视频到本地路径，返回保存的完整路径
    GET /v1/files/retrieve?file_id=xxx
    """
    resp = requests.get(
        f"{BASE_URL}/v1/files/retrieve",
        headers=HEADERS,
        params={"file_id": file_id},
        timeout=300,
        stream=True,
    )
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_path


def merge_videos_ffmpeg(clip_paths: list, output_path: str) -> str:
    """
    使用 FFmpeg concat 协议合并多个视频片段。
    concat 协议需要先创建临时文件列表。
    """
    if len(clip_paths) == 0:
        raise ValueError("没有视频片段可合并")
    if len(clip_paths) == 1:
        shutil.copy(clip_paths[0], output_path)
        return output_path

    # 创建临时目录存放片段列表文件
    tmpdir = tempfile.mkdtemp(prefix="minimax_concat_")
    list_file = os.path.join(tmpdir, "concat_list.txt")
    codec_copy = os.path.join(tmpdir, "merged_temp.mp4")

    # 生成安全文件名（不含特殊字符）
    safe_names = []
    for i, p in enumerate(clip_paths):
        safe = f"clip_{i:03d}{Path(p).suffix}"
        safe_names.append(safe)
        shutil.copy(p, os.path.join(tmpdir, safe))

    # 写入 FFmpeg concat 列表（使用绝对路径）
    with open(list_file, "w", encoding="utf-8") as f:
        for name in safe_names:
            abs_path = os.path.join(tmpdir, name).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")

    # FFmpeg concat
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        codec_copy,
    ]
    import subprocess
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg 合并失败：\n{proc.stderr}")

    # 复制最终结果
    shutil.copy(codec_copy, output_path)

    # 清理临时目录
    shutil.rmtree(tmpdir, ignore_errors=True)

    return output_path


# ── 主流程 ──────────────────────────────────────────────────────────────────

def run_pipeline(narration_file: str, output_video: str = None) -> str:
    """
    完整流水线：
    1. 读取文本文件（每行一段 narration）
    2. 逐行提交视频生成任务
    3. 轮询等待每个任务完成
    4. 下载所有片段
    5. 合并为完整视频
    6. 清理临时文件
    """
    # ── 读取 narration ───────────────────────────────────────────────────
    narration_file = Path(narration_file)
    if not narration_file.exists():
        raise FileNotFoundError(f"文件不存在：{narration_file}")

    narrations = [line.strip() for line in narration_file.read_text(encoding="utf-8").splitlines()]
    narrations = [n for n in narrations if n]  # 过滤空行
    total = len(narrations)
    if total == 0:
        raise ValueError("文件中没有任何有效的 narration")

    print(f"📖 读取到 {total} 段 narration：{narration_file.name}")
    for i, n in enumerate(narrations, 1):
        print(f"   [{i}/{total}] {n[:60]}{'...' if len(n) > 60 else ''}")

    # ── 创建临时目录 ─────────────────────────────────────────────────────
    tmpdir = tempfile.mkdtemp(prefix="minimax_clips_")
    print(f"\n📁 临时目录：{tmpdir}")

    clip_paths = []
    failed_tasks = []

    try:
        for i, narration in enumerate(narrations, 1):
            print(f"\n🎬 [{i}/{total}] 提交任务...")
            print(f"   文本：{narration[:60]}{'...' if len(narration) > 60 else ''}")

            # ① 提交任务
            task_id = submit_video_task(narration, duration=6)
            print(f"   ✅ 任务已提交，task_id = {task_id}")

            # ② 轮询状态
            try:
                result = wait_for_completion(task_id, interval=10, max_wait=600)
            except Exception as e:
                print(f"   ❌ 任务 [{i}/{total}] 等待失败：{e}")
                failed_tasks.append((i, task_id))
                continue

            file_id = result.get("file_id")
            if not file_id:
                print(f"   ⚠️ 任务完成但无 file_id：{result}")
                failed_tasks.append((i, task_id))
                continue

            # ③ 下载片段
            clip_path = os.path.join(tmpdir, f"clip_{i:03d}.mp4")
            print(f"   ⬇️  下载视频 file_id={file_id} ...")
            download_video(file_id, clip_path)
            clip_size = os.path.getsize(clip_path) / (1024 * 1024)
            print(f"   ✅ 下载完成，{clip_size:.1f} MB → {clip_path}")
            clip_paths.append(clip_path)

    except Exception as e:
        print(f"\n💥 主流程异常：{e}")
        raise

    finally:
        if not clip_paths:
            print("\n⚠️  没有成功下载任何视频片段，无法合并")
            shutil.rmtree(tmpdir, ignore_errors=True)
            raise RuntimeError("视频片段数量为 0，流水线失败")

        # ── 合并视频 ─────────────────────────────────────────────────────
        output_video = output_video or "minimax_output.mp4"
        output_video = str(Path(output_video).resolve())

        print(f"\n🎞️  合并 {len(clip_paths)} 个片段 → {output_video}")
        merge_videos_ffmpeg(clip_paths, output_video)

        final_size = os.path.getsize(output_video) / (1024 * 1024)
        print(f"   ✅ 合并完成，{final_size:.1f} MB")

        # ── 清理临时文件 ──────────────────────────────────────────────────
        print(f"\n🧹 清理临时目录：{tmpdir}")
        shutil.rmtree(tmpdir, ignore_errors=True)

        # ── 汇总 ──────────────────────────────────────────────────────────
        print("\n" + "=" * 60)
        print(f"✅ 流水线完成！")
        print(f"   输出视频：{output_video}")
        print(f"   片段数量：{len(clip_paths)}/{total}")
        if failed_tasks:
            print(f"   失败片段：{[f[0] for f in failed_tasks]}")
        print("=" * 60)

        return output_video


# ── CLI 入口 ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    narration_file = sys.argv[1]
    output_video = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result = run_pipeline(narration_file, output_video)
        print(f"\n输出路径：{result}")
    except Exception as e:
        print(f"\n💥 流水线执行失败：{e}")
        sys.exit(1)
