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
风格：理性、精准、有观点，口语化，有态度。
每条视频要有精算师视角：用数字说话，有观点，有判断。
不煽情，不恐吓，用数据说服人。'''},
        {'role': 'user', 'content': '''帮我写第三条视频口播脚本（90秒）——“去乐城治病，要花多少钱”

**这条视频的核心任务：**
- 帮观众算清楚去乐城治病的真实成本
- 不是卖保险，是告诉观众"乐城的入场成本到底是什么"
- 引出权益卡作为解决方案

**内容逻辑：**
1. 【接上条】上条说了乐城的门槛不是钱，是信息差。那到底要花多少钱？
2. 【算账】去乐城用一次前沿疗法，实际费用构成：
   - 治疗费（看具体项目，从几万到几十万）
   - 交通住宿
   - 时间成本
3. 【精算师判断】这笔账，算清楚值不值
4. 【引出权益卡】但有一个更划算的方式

**关键数据（可融入）：**
- 具体项目价格区间
- 权益卡：365元/年，锁定150万特药额度

**风格要求：**
- 精算师算账风格，数字要硬
- 不要恐吓，要理性
- 结尾有钩子，为第四条铺垫

**格式：直接给脚本正文，不要其他说明**
---'''}
    ],
    'max_tokens': 900,
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