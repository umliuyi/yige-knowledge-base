import sys, os, requests, json
sys.path.insert(0, r'C:\Users\Administrator\.openclaw-autoclaw\workspace\scripts')
import hailuo_video_v2 as hv

API_KEY = 'sk-api-UTv9N1XfUYjJLBWtHRhSnR45eCaRlTyqOBaf4QSV2zV5SZSfFksEihkHaqdkuH44WLHVwveZnPIJV0BwDGPVFeZcg6VQb0eJErx8T0uyhJdd_oISKuu4gBk'
TASK_ID = '750423112241001267'

# 查询任务
status = hv.query_task_status(TASK_ID, API_KEY)
print('Status:', status)

# 打印完整响应
print(json.dumps(status, ensure_ascii=False, indent=2))
