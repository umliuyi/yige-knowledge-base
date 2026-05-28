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
        {'role': 'user', 'content': '''写糖尿病系列第三集口播脚本（90秒）——“干细胞治疗糖尿病是怎么回事"

主题：干细胞治疗糖尿病的原理（通俗版）

内容要求：
1. 承接上集：上集说传统治疗越来越不够用，这集说乐城的干细胞方案是什么
2. 核心：干细胞如何修复胰岛β细胞（用通俗比喻，不需要医学背景也能听懂）
3. 适合人群：2型糖尿病，用≥3种降糖药仍控制不佳者
4. 注意：不讲价格（下一集讲），这集只讲清楚"是什么"

风格要求：
- 有比喻，把复杂原理讲简单
- 精算师有判断（"这个方案解决了什么问题"）
- 结尾铺垫下一集（价格和选择）

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
