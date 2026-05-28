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
        {'role': 'system', 'content': '你是一个精算师，服务于海南乐城医疗特区。风格：理性、精准、有观点，口语化，有态度。'},
        {'role': 'user', 'content': '''写糖尿病干细胞系列第一集口播脚本（90秒）——“中国1.4亿人得了这个病”

主题：中国糖尿病的现状有多严重

内容要求：
1. 开场：1.4亿患者数据，惊人但不被重视
2. 核心：糖尿病不是"血糖高"那么简单，并发症才是真正的危险（心梗、脑梗、失明、肾衰）
3. 精算师视角：精算师天天和数字打交道，这个病的"隐性成本"比表面看起来高得多
4. 结尾：不直接给答案，而是铺垫——"那治疗呢？下一集会详细讲"

风格要求：
- 开头用数字冲击，不要铺垫
- 精算师有判断，有态度
- 结尾自然过渡到下一集，不生硬（不是说"下期预告"，而是让观众自然期待"那然后呢"）
- 口语化，有节奏感

格式：直接给脚本正文'''}
    ],
    'max_tokens': 700,
    'temperature': 0.7
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
