# -*- coding: utf-8 -*-
import json, os, sys

# Fix encoding for Windows stdout
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

path = r'C:\Users\Administrator\.openclaw-autoclaw\cron\jobs.json'
with open(path, encoding='utf-8') as f:
    data = json.load(f)

fixed = 0
for job in data['jobs']:
    try:
        old = job['payload']['timeoutSeconds']
        if isinstance(old, int) and old < 900:
            job['payload']['timeoutSeconds'] = 900
            job['state']['consecutiveErrors'] = 0
            job['state']['lastStatus'] = 'ok'
            job['state']['lastRunStatus'] = 'ok'
            name = job.get('name', '?')
            print(f'Fixed: {name} ({old}s->900s)')
            fixed += 1
    except (KeyError, TypeError):
        pass

print(f'Total: {fixed} jobs fixed')
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('Saved.')
