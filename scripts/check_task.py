import sys
sys.path.insert(0, r'C:\Users\Administrator\.openclaw-autoclaw\workspace\scripts')
import hailuo_video_v2 as hv

API_KEY = 'sk-api-UTv9N1XfUYjJLBWtHRhSnR45eCaRlTyqOBaf4QSV2zV5SZSfFksEihkHaqdkuH44WLHVwveZnPIJV0BwDGPVFeZcg6VQb0eJErx8T0uyhJdd_oISKuu4gBk'
TASK_ID = '750423112241001267'

# 用hailuo_video_v2的request_with_token查询
# 尝试GET /video_generations/{task_id}
url = f'https://api.minimaxi.com/mb_api/v1/video_generations/{TASK_ID}'
try:
    r = hv.request_with_token('GET', url, api_key=API_KEY, json_body={})
    print('Status:', r.status_code)
    print('Response:', r.text[:500])
except Exception as e:
    print('Error:', e)

# 也尝试POST查询
try:
    r2 = hv.request_with_token('POST', url, api_key=API_KEY, json_body={})
    print('POST Status:', r2.status_code)
    print('POST Response:', r2.text[:300])
except Exception as e:
    print('POST Error:', e)
