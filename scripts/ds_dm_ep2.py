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
        {'role': 'user', 'content': '''写糖尿病系列第二集口播脚本（90秒）——“药越吃越多，针越打越多"

主题：传统糖尿病治疗的困境

内容要求：
1. 承接上集：上集说了糖尿病现状，这集说"为什么传统治疗越来越不够用"
2. 核心：降糖药从1种→2种→3种，剂量越来越大，血糖越来越难控——胰岛细胞在衰退，这个过程不可逆
3. 精算师视角：这不是"控制不好"，是底层逻辑——胰岛β细胞功能持续恶化
4. 结尾：铺垫下一集——"那有没有新办法？下一集说"

风格要求：
- 承接上集自然
- 有画面感（"药越吃越多"的痛苦）
- 精算师下判断
- 结尾让人想看下一集

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
