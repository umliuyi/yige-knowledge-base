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
        {'role': 'system', 'content': '''你是一个真实的精算师，在抖音做口播。
精算师风格：用数字算账，让观众自己得出结论。
说话直接，有观点，有态度，口语化，不废话。'''},
        {'role': 'user', 'content': '''帮我写第三条视频口播脚本（90秒）。

**第二条结尾钩子（必须接上）：**
"下一条，我算给你看：一场大病，到底要花多少钱。"
→ 第三条就是算这笔账

**第三条核心：**
帮观众算清楚一场大病的完整账单。
不是只算治疗费，是算综合成本。

**精算师算账内容（真实数据）：**
- 大病治疗费：32万（卫健委年鉴）
- 康复期营养费：5-10万
- 误工损失（家庭支柱）：按月薪1万×24个月 = 24万
- 陪护费（护工或家人误工）：按5000/月×12个月 = 6万
- 综合成本：32万 + 10万 + 24万 + 6万 = 约70万

**精算师的核心结论：**
你以为大病花了32万，实际上你的损失是70万。
这70万，有一半不在医院账单里，在你的生活里。

**开头：**
直接接上："上条我说帮你算一场大病要花多少钱，今天我算完了，结果超出你想象。"

**结尾钩子：**
抛问题：你以为准备好32万就够了？评论区告诉我，你家能拿出多少？

**风格：**
- 口语化，有算账感
- 精算师直接给结论
- 数字要硬，要震撼
- 不要故事，不要长叙事

格式：直接给脚本正文
---'''}
    ],
    'max_tokens': 800,
    'temperature': 0.8
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
