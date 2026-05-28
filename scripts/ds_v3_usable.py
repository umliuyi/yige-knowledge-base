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
        {'role': 'system', 'content': '''你是一个精算师，服务于海南乐城医疗特区。
精算师风格：理性、精准、用数字说话，口语化，有观点。
核心能力：把复杂问题用普通人能理解的数字讲清楚。
你的每条视频都有精算师视角贯穿，有观点，有态度。'''},
        {'role': 'user', 'content': '''帮我写第三条视频脚本（90秒）：精算师告诉你，去乐城治病，"用得上"和"用得起"是两件事

**前情（第二条视频已建立的概念）：**
上一条我告诉你：CAR-T疗法120万，大多数普通家庭"用不起"。
但这一条，我要告诉你一个更残忍的真相：
**就算你有钱，也不一定能"用得上"。**

**本条核心概念（必须贯穿）：**
- "用得上" = 有医疗资源，知道去哪用，能排上队
- "用得起" = 承担得起费用，提前规划好
- 乐城的核心价值：让你从"用不上"变成"用得上"

**精算师算账要体现：**
- 普通人一辈子大病期望损失：23万
- 但比费用更残酷的是：你有钱，也约不上乐城的专家
- 精算师的价值：提前锁定"用得上"这个资源

**产品信息（可以融入）：**
- 权益卡（不是保险，是入场券）
- 14项健康管理服务（挂号绿通、专业陪诊、优先安排）
- 作用：解决"用得上"的问题

**风格要求：**
- 开头：揭秘感，用"更残忍的真相"开场
- 主体：用数字+故事，区分"用得上"vs"用得起"
- 精算师态度：理性决策，提前锁定稀缺资源
- 结尾：引导关注，预告下期权益卡落地

**格式：**
---
【主体】（70秒）

---
【钩子】（20秒）
---'''}
    ],
    'max_tokens': 1000,
    'temperature': 0.75
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
