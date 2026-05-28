# -*- coding: utf-8 -*-
import urllib.request
import json

# Get token
token_req = urllib.request.Request('http://127.0.0.1:18432/get_token')
with urllib.request.urlopen(token_req, timeout=5) as r:
    response_text = r.read().decode('utf-8')
    # Response is "Bearer <token>"
    token = response_text.strip()
    if token.startswith('Bearer '):
        token = token[7:]
    print(f'Token: {token[:30]}...')

# Generate image - 封面图
prompt = (
    "A modern medical illustration showing Hainan Boao Lecheng International Medical Tourism Pilot Zone, "
    "featuring a sleek hospital building with tropical palm trees, "
    "clean medical interior with international doctors, "
    "warm sunlight, professional medical aesthetic, high quality, 16:9 aspect ratio"
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
    with urllib.request.urlopen(req, timeout=90) as r:
        result = json.loads(r.read().decode('utf-8'))
        print('Image result:', json.dumps(result, ensure_ascii=False, indent=2)[:2000])
except Exception as e:
    print(f'Image generation error: {e}')
