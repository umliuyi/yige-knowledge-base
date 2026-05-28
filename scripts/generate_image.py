# -*- coding: utf-8 -*-
import urllib.request
import json

# Get token
try:
    token_req = urllib.request.Request('http://127.0.0.1:18432/get_token')
    with urllib.request.urlopen(token_req, timeout=5) as r:
        token_data = json.loads(r.read().decode())
        token = token_data.get('token', '')
        print(f'Token: {token[:20]}...' if token else 'No token')
except Exception as e:
    print(f'Token error: {e}')
    token = ''

if not token:
    print('No token available, exiting')
    exit(1)

# Generate image - 封面图：乐城医疗特区概念图
prompt = (
    "A modern medical illustration showing Hainan Boao Lecheng International Medical Tourism Pilot Zone, "
    "featuring a sleek hospital building with tropical palm trees, "
    "clean medical interior with international doctors, "
    "text overlay space on left side for Chinese text '乐城看病指南', "
    "warm sunlight, professional medical aesthetic, "
    "no Chinese characters in image body, high quality, 16:9 aspect ratio"
)

url = 'http://127.0.0.1:18432/autoglm_generate_image'
payload = json.dumps({
    'prompt': prompt,
    'resolution': '16:9'
}).encode('utf-8')

req = urllib.request.Request(url, data=payload, headers={
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
})

try:
    with urllib.request.urlopen(req, timeout=60) as r:
        result = json.loads(r.read().decode('utf-8'))
        print('Result:', json.dumps(result, ensure_ascii=False, indent=2))
except Exception as e:
    print(f'Image generation error: {e}')
