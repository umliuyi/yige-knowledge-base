# -*- coding: utf-8 -*-
import urllib.request, ssl, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://api.deepseek.com/chat/completions'
payload = {
    'model': 'deepseek-chat',
    'messages': [{'role': 'user', 'content': 'Hi, reply with OK'}],
    'max_tokens': 50
}
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    url,
    data=data,
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk-18a62cec69c54b7196803c7ecdcbef81'
    }
)
try:
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    result = json.loads(resp.read().decode('utf-8'))
    print('SUCCESS:', result['choices'][0]['message']['content'])
except Exception as e:
    print('ERROR:', str(e))
