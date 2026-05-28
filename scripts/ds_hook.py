# -*- coding: utf-8 -*-
import urllib.request, ssl, json, sys
sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

API_KEY = 'sk-18a62cec69c54b7196803c7ecdcbef81'

payload = {
    'model': 'deepseek-chat',
    'messages': [
        {'role': 'system', 'content': '你是精算师，帮用户写有冲击力的抖音视频结尾钩子。要短促有力，让人想关注。'},
        {'role': 'user', 'content': '''为一条口播视频写3个不同风格的结尾钩子（每个15秒以内）。

背景：精算师刘一，刚讲完"大病风险期望值23万"的算账过程。
人设：用数字吃饭的精算师，理性、有观点、不卖焦虑。
目标：引导观众关注账号。

要求每个钩子：
1. 要有精算师的判断感或号召感
2. 要让人看完想关注
3. 口语化、直接、有力量
4. 避免"感谢关注"这类套话

格式：直接给我3条钩子文本，不需要解释。'''}
    ],
    'max_tokens': 400,
    'temperature': 0.9
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
