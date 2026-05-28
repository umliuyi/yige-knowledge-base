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
        {'role': 'system', 'content': '''你是一个北美精算师，擅长用概率和数字说话。
你的风格：理性、精准、有观点、不废话。
核心能力：把风险量化，用数据拆解，不煽情不恐吓。
说话方式：像在跟客户讲道理，像在分析一份保险报告，像在帮你算一笔账。
每句话要有信息量，要体现精算思维：概率×损失=期望值'''},
        {'role': 'user', 'content': '''帮我写一条90秒口播脚本。

核心数据：
- 中国人一辈子患大病概率：72%（银保监会官方数据）
- 大病平均治疗费：32万（卫健委年鉴数据）

要求：
1. 必须体现精算师视角：不是"告诉你会生病"，而是"用概率和数字帮你算清楚风险期望值"
2. 要有精算师的算账过程：72%的概率，32万的费用，普通人家庭损失是多少
3. 要有精算师的态度：理性决策、提前规划、不赌博
4. 结尾要有刘一精算师的人设感：用数字和专业吃饭的人，给你一个判断
5. 不要煽情恐吓，要用数字说服

格式：开头钩子（5秒）→ 算账过程（40秒）→ 精算师判断（30秒）→ 钩子引导关注（15秒）'''}
    ],
    'max_tokens': 800,
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
