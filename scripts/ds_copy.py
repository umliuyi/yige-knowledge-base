# -*- coding: utf-8 -*-
import urllib.request, ssl, json, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

API_KEY = 'sk-18a62cec69c54b7196803c7ecdcbef81'

payload = {
    'model': 'deepseek-chat',
    'messages': [
        {'role': 'system', 'content': '你是一个短视频文案专家，口语化、有观点、有节奏感、有态度，适合抖音60秒口播。'},
        {'role': 'user', 'content': '帮我写一条60秒口播脚本：中国人一辈子患大病概率72%（精算数据）+ 治疗费32万（卫健委数据），精算师人设，有观点有态度，结尾有钩子引导关注'}
    ],
    'max_tokens': 600,
    'temperature': 0.8
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    'https://api.deepseek.com/chat/completions',
    data=data,
    headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
)
resp = urllib.request.urlopen(req, timeout=60, context=ctx)
result = json.loads(resp.read().decode('utf-8'))
print(result['choices'][0]['message']['content'])
