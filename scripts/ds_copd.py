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
        {'role': 'system', 'content': '你是一个精算师，服务于海南乐城医疗特区。风格：理性、精准、有观点，口语化，有态度。每条视频要有精算师视角：用数字说话，有观点，有判断。不煽情，不恐吓，用数据说服人。'},
        {'role': 'user', 'content': '''帮我写第四期视频口播脚本（90秒）——"慢阻肺干细胞，乐城能让你的肺重获新生吗"

**这条视频的核心任务：**
- 介绍乐城的慢阻肺（COPD）干细胞项目，让观众了解这个选项
- 不是卖保险，是讲清楚乐城有什么、适合谁、价格多少

**内容逻辑（四段式）：**
1. 【开场】慢阻肺在中国有多常见，痛苦程度如何
2. 【项目是什么】干细胞治疗COPD的原理（通俗版）
3. 【适合人群】哪些COPD患者适合
4. 【乐城价格】乐城官方价格：15万/针（瑞金医院海南医院）
5. 【结尾】留钩子

**关键信息（必须准确）：**
- 气道基底层干细胞治疗COPD：15万/针（瑞金医院海南医院）
- 间质性肺病：15万/针（瑞金医院海南医院）
- 支气管扩张症：15万/针（瑞金医院海南医院）

**风格要求：**
- 精算师视角，用数字说事
- 不要恐吓，要理性讲清价值
- 口语化，有节奏感

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