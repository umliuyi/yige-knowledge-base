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
        {'role': 'user', 'content': '''写糖尿病系列第四集口播脚本（90秒）——“18万换一个选择，值不值"

主题：乐城干细胞治疗糖尿病的价格和选择

内容要求：
1. 承接上集：上集说了原理，这集说价格和适合人群
2. 价格（官方数据）：慈铭博鳌，5.98万/针×3≈18万/疗程；瑞金海南，GLP-1双因子，36万/疗程
3. 精算师算账：和一辈子吃药的累计成本对比
4. 结尾：结尾可以是这一集的收尾，也可以预告下一系列——不强行续，但要有"还有更多"的感觉

风格要求：
- 精算师算账，数字要硬
- 不要恐吓，要理性
- 有判断感

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
