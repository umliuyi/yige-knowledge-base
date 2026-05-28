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
        {'role': 'system', 'content': '''你是一个真实的精算师，不是老师，不是医生。你说话有三个特点：1. 你见过很多病人，有自己的经历和感受；2. 你看到普通人看不到的数字背后的东西；3. 你说的话和别人不一样，是说一个别人没想过的事实。'''},
        {'role': 'user', 'content': '''写糖尿病系列第一集口播脚本（90秒）——“1.4亿人，和一个你不知道的真相”

合并两个内容：
1. 糖尿病的现状有多可怕（并发症、心梗、肾衰）
2. 传统治疗为什么越来越不够用（药越吃越多是必然结果）

要求：
- 精算师视角，有经历、有洞察
- 有让观众"啊原来如此"的点
- 内容密度高，90秒讲透两个核心
- 不要铺垫，直接进入

格式：直接给脚本正文'''}
    ],
    'max_tokens': 800,
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
