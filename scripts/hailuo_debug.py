import urllib.request, json, time, os

API_KEY = "sk-api-UTv9N1XfUYjJLBWtHRhSnR45eCaRlTyqOBaf4QSV2zV5SZSfFksEihkHaqdkuH44WLHVwveZnPIJV0BwDGPVFeZcg6VQb0eJErx8T0uyhJdd_oISKuu4gBk"

# 先查一下当前任务状态
task_id = "397754191458849"

endpoints_to_try = [
    f"https://api.minimaxi.com/v1/video_generation/{task_id}",
    f"https://api.minimaxi.com/v1/video_generation/query/{task_id}",
    f"https://api.minimaxi.com/v1/text_to_video/{task_id}",
]

for ep in endpoints_to_try:
    print(f"Trying: {ep}")
    try:
        req = urllib.request.Request(
            ep,
            headers={"Authorization": "Bearer " + API_KEY}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            r = json.loads(resp.read())
            print(f"  SUCCESS: {json.dumps(r)[:300]}")
    except Exception as e:
        print(f"  ERROR: {e}")
