# -*- coding: utf-8 -*-
"""
Kling API 完整自动化脚本
基于官方文档 v2026-05-26

API基础配置
- Base URL: https://api-beijing.klingai.com
- 鉴权: JWT Token (HS256)
- Access Key: ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT
- Secret Key: 8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9
"""
import jwt, time, urllib.request, json, urllib.parse, ssl

# ============================================================
# 配置
# ============================================================
AK = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
SK = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
BASE_URL = 'https://api-beijing.klingai.com'

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

# ============================================================
# JWT Token 生成
# ============================================================
def make_token():
    payload = {
        "iss": AK,
        "exp": int(time.time()) + 1800,
        "nbf": int(time.time()) - 5
    }
    return jwt.encode(payload, SK, algorithm="HS256")

def make_headers(body=''):
    token = make_token()
    return {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

# ============================================================
# HTTP 请求
# ============================================================
def api_get(path):
    url = BASE_URL + path
    h = make_headers()
    req = urllib.request.Request(url, headers=h, method="GET")
    try:
        resp = urllib.request.urlopen(req, timeout=30, context=CTX)
        return resp.status, json.loads(resp.read().decode())
    except Exception as e:
        try:
            err = e.read().decode() if hasattr(e, 'read') else str(e)
        except:
            err = str(e)
        return 'err', {"error": err}

def api_post(path, body_dict):
    url = BASE_URL + path
    body = json.dumps(body_dict, ensure_ascii=False)
    h = make_headers()
    req = urllib.request.Request(url, data=body.encode('utf-8'), headers=h, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=30, context=CTX)
        return resp.status, json.loads(resp.read().decode())
    except Exception as e:
        try:
            err_body = e.read().decode() if hasattr(e, 'read') else str(e)
            err_json = json.loads(err_body) if err_body.startswith('{') else {"raw": err_body}
        except:
            err_json = {"raw": str(e)}
        return 'err', err_json

# ============================================================
# 轮询任务状态
# ============================================================
def wait_task(path_template, task_id, interval=5, timeout=300):
    """轮询直到任务完成或超时"""
    start = time.time()
    while time.time() - start < timeout:
        status, resp = api_get(path_template.format(task_id))
        if status != 200:
            return status, resp
        data = resp.get('data', {})
        task_status = data.get('task_status', '')
        print(f"  [{int(time.time()-start)}s] status={task_status}")
        if task_status in ('succeed', 'failed'):
            return 200, resp
        time.sleep(interval)
    return 'timeout', {"message": "Task polling timeout"}

# ============================================================
# API 1: 文生视频 (Text-to-Video)
# POST /v1/videos/text2video
# ============================================================
def create_video_text2video(prompt, model_name='kling-v2-6', duration='5',
                          mode='pro', aspect_ratio='1:1',
                          negative_prompt='', sound='off',
                          external_task_id=''):
    body = {
        "model_name": model_name,
        "prompt": prompt,
        "duration": str(duration),
        "mode": mode,
        "aspect_ratio": aspect_ratio,
        "negative_prompt": negative_prompt,
        "sound": sound,
    }
    if external_task_id:
        body["external_task_id"] = external_task_id
    return api_post('/v1/videos/text2video', body)

def query_video_text2video(task_id):
    return api_get(f'/v1/videos/text2video/{task_id}')

# ============================================================
# API 2: 图生视频 (Image-to-Video)
# POST /v1/videos/image2video
# ============================================================
def create_video_image2video(image_url, prompt='',
                          model_name='kling-v2-6',
                          duration='5', mode='pro',
                          negative_prompt='',
                          image_tail_url='',
                          external_task_id=''):
    body = {
        "model_name": model_name,
        "image": image_url,
        "duration": str(duration),
        "mode": mode,
        "negative_prompt": negative_prompt,
    }
    if prompt:
        body["prompt"] = prompt
    if image_tail_url:
        body["image_tail"] = image_tail_url
    if external_task_id:
        body["external_task_id"] = external_task_id
    return api_post('/v1/videos/image2video', body)

def query_video_image2video(task_id):
    return api_get(f'/v1/videos/image2video/{task_id}')

# ============================================================
# API 3: Omni视频 (Omni-Video) - 最强模型
# POST /v1/videos/omni-video
# ============================================================
def create_video_omni(prompt, model_name='kling-video-o1',
                    duration='5', mode='pro',
                    aspect_ratio='1:1',
                    multi_shot=False,
                    external_task_id=''):
    body = {
        "model_name": model_name,
        "prompt": prompt,
        "duration": str(duration),
        "mode": mode,
        "aspect_ratio": aspect_ratio,
        "multi_shot": multi_shot,
    }
    if external_task_id:
        body["external_task_id"] = external_task_id
    return api_post('/v1/videos/omni-video', body)

def query_video_omni(task_id):
    return api_get(f'/v1/videos/omni-video/{task_id}')

# ============================================================
# API 4: 多图生视频 (Multi-Image-to-Video)
# POST /v1/videos/multi-image2video
# ============================================================
def create_video_multi_image(image_list, prompt,
                           model_name='kling-v1-6',
                           duration='5', mode='std',
                           aspect_ratio='16:9',
                           negative_prompt='',
                           external_task_id=''):
    """image_list: [{'image': 'url_or_base64'}, ...]"""
    body = {
        "model_name": model_name,
        "image_list": image_list,
        "prompt": prompt,
        "duration": str(duration),
        "mode": mode,
        "aspect_ratio": aspect_ratio,
        "negative_prompt": negative_prompt,
    }
    if external_task_id:
        body["external_task_id"] = external_task_id
    return api_post('/v1/videos/multi-image2video', body)

def query_video_multi_image(task_id):
    return api_get(f'/v1/videos/multi-image2video/{task_id}')

# ============================================================
# API 5: 数字人 (Avatar / Digital Human)
# POST /v1/videos/avatar/image2video
# ============================================================
def create_avatar_video(image, prompt='',
                       sound_file='',
                       audio_id='',
                       mode='std',
                       external_task_id=''):
    body = {
        "image": image,
        "mode": mode,
    }
    if prompt:
        body["prompt"] = prompt
    if sound_file:
        body["sound_file"] = sound_file
    if audio_id:
        body["audio_id"] = audio_id
    if external_task_id:
        body["external_task_id"] = external_task_id
    return api_post('/v1/videos/avatar/image2video', body)

def query_avatar_video(task_id):
    return api_get(f'/v1/videos/avatar/image2video/{task_id}')

# ============================================================
# API 6: 对口型 (Lip Sync)
# POST /v1/videos/advanced-lip-sync
# ============================================================
def create_lipsync(session_id, face_choose,
                  external_task_id=''):
    """face_choose: [{'face_id': 'xxx', 'sound_file': 'url', ...}]"""
    body = {
        "session_id": session_id,
        "face_choose": face_choose,
    }
    if external_task_id:
        body["external_task_id"] = external_task_id
    return api_post('/v1/videos/advanced-lip-sync', body)

def identify_face(video_url='', video_id=''):
    body = {}
    if video_url:
        body["video_url"] = video_url
    if video_id:
        body["video_id"] = video_id
    return api_post('/v1/videos/identify-face', body)

def query_lipsync(task_id):
    return api_get(f'/v1/videos/advanced-lip-sync/{task_id}')

# ============================================================
# API 7: 视频延长 (Video Extend)
# POST /v1/videos/video-extend
# ============================================================
def extend_video(video_id, prompt='',
                negative_prompt='',
                external_task_id=''):
    body = {
        "video_id": video_id,
    }
    if prompt:
        body["prompt"] = prompt
    if negative_prompt:
        body["negative_prompt"] = negative_prompt
    if external_task_id:
        body["external_task_id"] = external_task_id
    return api_post('/v1/videos/video-extend', body)

def query_video_extend(task_id):
    return api_get(f'/v1/videos/video-extend/{task_id}')

# ============================================================
# 完整流程示例: 文生视频 -> 轮询 -> 获取结果URL
# ============================================================
def full_video_pipeline(prompt, model_name='kling-v2-6',
                        duration='5', mode='pro',
                        aspect_ratio='1:1'):
    print(f"[Kling API] 创建文生视频任务...")
    status, resp = create_video_text2video(
        prompt=prompt,
        model_name=model_name,
        duration=duration,
        mode=mode,
        aspect_ratio=aspect_ratio
    )
    print(f"  创建结果: status={status}")
    print(f"  响应: {json.dumps(resp, ensure_ascii=False)[:200]}")

    if status != 200:
        return resp

    task_id = resp.get('data', {}).get('task_id', '')
    if not task_id:
        return resp

    print(f"  task_id={task_id}  轮询中...")
    status2, resp2 = wait_task('/v1/videos/text2video/{}', task_id)
    print(f"  最终结果: {json.dumps(resp2, ensure_ascii=False)[:300]}")

    if status2 == 200:
        videos = resp2.get('data', {}).get('task_result', {}).get('videos', [])
        if videos:
            print(f"  视频URL: {videos[0].get('url')}")
    return resp2


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("用法: python kling_video_api.py <prompt>")
        print("示例: python kling_video_api.py '一只可爱的小兔子在草地上奔跑'")
        sys.exit(0)
    prompt = sys.argv[1]
    result = full_video_pipeline(prompt)
    print("完成")
