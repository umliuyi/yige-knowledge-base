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
        {'role': 'system', 'content': '''你是一个精算师，擅长用概率和数字说话。
风格：理性、精准、有观点、不废话。
核心：用风险期望值说服人，不煽情不恐吓。
精算思维：概率×损失=期望值。
结尾钩子要短促有力，让人想关注。'''},
        {'role': 'user', 'content': '''帮我写一条90秒口播脚本，分两部分：

【主体内容】（约70秒）
- 概率：72%（银保监会官方数据）
- 费用：32万（卫健委年鉴）
- 期望损失：72%×32万=23.04万
- 精算师判断：理性决策是把不确定损失变成确定的保费支出，这叫风险转移

【结尾钩子】（约20秒）
要求：
1. 要有精算师的判断感，不是客套话
2. 要有冲击力，让人想关注
3. 口语化、直接、有力量
4. 要和刘一人设一致：用数字说话、理性、有观点
5. 不要"喜欢请关注"这类抖音套话

格式：
---
【主体】
（70秒口播正文）

---
【钩子】
（20秒结尾）
---'''}
    ],
    'max_tokens': 900,
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
