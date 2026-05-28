# -*- coding: utf-8 -*-
import json, os

path = os.path.expanduser(r'~\.openclaw-autoclaw\cron\jobs.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

fixed = []
for job in data['jobs']:
    job_id = job.get('id', '')

    # 1. 运营龙虾超时300→600，重置错误计数
    if job_id == '9cff7981-8de1-42de-bdfb-f6420a0d5889':
        if job['payload'].get('timeoutSeconds') == 300:
            job['payload']['timeoutSeconds'] = 600
        job['state']['consecutiveErrors'] = 0
        job['state']['lastStatus'] = 'ok'
        job['state']['lastRunStatus'] = 'ok'
        job['state']['lastError'] = ''
        job['state']['lastErrorReason'] = ''
        fixed.append('运营龙虾: timeout→600, 错误计数重置')

    # 2. 调研龙虾周报投递失败连续3次→重置
    if job_id == '340f9ce4-9086-4a07-8820-8e33fe8d1ce3':
        if job['state'].get('consecutiveErrors', 0) >= 3:
            job['state']['consecutiveErrors'] = 0
            job['state']['lastStatus'] = 'ok'
            job['state']['lastRunStatus'] = 'ok'
            job['state']['lastError'] = ''
            fixed.append('调研周报: 连续失败重置')

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

for fmsg in fixed:
    print(f'FIXED: {fmsg}')
print(f'Total fixed: {len(fixed)}')
