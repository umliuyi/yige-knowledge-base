# -*- coding: utf-8 -*-
import urllib.request, ssl, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

payload = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "请回复OK"}],
    "max_tokens": 50
}
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    'https://api.deepseek.com/chat/completions',
    data=data,
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk-18a62cec69c54b7196803c7ecdcbef81'
    }
)
try:
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    result = json.loads(resp.read().decode('utf-8'))
    print('OK:', result['choices'][0]['message']['content'])
except Exception as e:
    print('ERROR:', str(e))
