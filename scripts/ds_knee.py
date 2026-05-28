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
        {'role': 'user', 'content': '''帮我写第三期视频口播脚本（90秒）——"膝关节干细胞，不用换关节的新选择"

**这条视频的核心任务：**
- 介绍乐城的膝关节干细胞项目，让观众了解这个选项
- 不是卖保险，是讲清楚乐城有什么、适合谁、价格多少

**内容逻辑（四段式）：**
1. 【开场】膝关节问题有多普遍（骨关节炎/半月板损伤的痛苦）
2. 【项目是什么】干细胞修复软骨的原理（通俗版，不需要懂医学）
3. 【适合人群】哪些膝关节患者适合（骨关节炎、半月板损伤）
4. 【乐城价格+对比】乐城官方价格：
   - 髋骨关节炎：3.635万/针（海南帝诺医院）
   - 膝骨关节炎：3.635万/针（海南帝湾医院）
   - 半月板损伤：8万/单膝（博鳌超级医院）
   和关节置换手术对比（费用、恢复期、风险）

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