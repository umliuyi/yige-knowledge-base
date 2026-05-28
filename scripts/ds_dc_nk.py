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
        {'role': 'user', 'content': '''帮我写第二期视频口播脚本（90秒）——"DC/NK细胞免疫治疗，肿瘤患者的新选择"

**这条视频的核心任务：**
- 介绍乐城的肿瘤免疫项目，让观众了解这个选项
- 不是卖保险，是讲清楚乐城有什么、适合谁、价格多少

**内容逻辑（四段式）：**
1. 【开场】肿瘤治疗的传统手段有什么局限
2. 【项目是什么】DC细胞/NK细胞免疫治疗的原理（通俗版）
3. 【适合人群】哪些肿瘤患者可以考虑
4. 【乐城价格+对比】乐城官方价格：
   - DC细胞（胰腺癌/结直肠癌）：38万/次
   - 恶性肿瘤DC疫苗：15万/针
   - NK细胞（多癌种）：3.3万/针×6疗程≈20万
5. 【结尾】留钩子

**关键信息（必须准确）：**
- DC细胞（胰腺癌）5次≈190万；（结直肠癌）3次≈114万（博鳌超级医院）
- NK细胞（多癌种）3.3万/针，3-6针/疗程（华西城东医院）
- NK细胞（肺癌）21万/3针（树兰医院）
- 恶性肿瘤DC疫苗15万/针（华西城东医院）

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