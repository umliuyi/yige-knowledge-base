import hailuo_video_v2 as hv
import os, time

API_KEY = 'sk-api-UTv9N1XfUYjJLBWtHRhSnR45eCaRlTyqOBaf4QSV2zV5SZSfFksEihkHaqdkuH44WLHVwveZnPIJV0BwDGPVFeZcg6VQb0eJErx8T0uyhJdd_oISKuu4gBk'
TASK_ID = '750423112241001267'
OUTPUT = 'C:/Users/Administrator/Downloads/videos/daily_news/test_hailuo.mp4'

print('Waiting for task to complete...')
for i in range(20):  # poll up to 20 times
    status = hv.query_task_status(TASK_ID, API_KEY)
    state = status.get('data', {}).get('status', 'unknown')
    print(f'[{i+1}] Status: {state}')
    if state == 'success':
        print('Task complete!')
        break
    elif state in ('failed', 'error'):
        print('Task failed:', status)
        break
    time.sleep(10)  # wait 10 seconds between polls
else:
    print('Timeout waiting for task')

# Try to download regardless
print('Attempting download...')
try:
    out = hv.download_video(TASK_ID, API_KEY, OUTPUT)
    print(f'Downloaded to: {out}')
    import os
    if os.path.exists(out):
        print(f'File size: {os.path.getsize(out) / 1024 / 1024:.1f} MB')
except Exception as e:
    print(f'Download failed: {e}')
    # Fallback: try direct URLs
    import requests
    for url in [
        f'https://hailuo-video.xf-yun.com/video_upscaler/file/{TASK_ID}',
    ]:
        print(f'Trying: {url}')
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60, stream=True)
        print(f'Status: {r.status_code}')
