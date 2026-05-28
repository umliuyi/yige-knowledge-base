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
精算师核心武器：概率×损失=期望值
用这个公式说服人，不是恐吓，是让你看清数字背后的真相。
说话直接，有观点，有态度，口语化，不废话。'''},
        {'role': 'user', 'content': '''帮我写第三条视频口播脚本（90秒）。

**第二条结尾（必须接上）：**
"下一条，我算给你看：一场大病，到底要花多少钱。"
→ 第三条就是算这笔账，加上概率

**精算师算账核心（必须有）：**
- 大病概率：72%（银保监会官方数据）
- 大病综合费用：70万（治疗32万+康复10万+误工24万+陪护6万）
- 期望损失：72% × 70万 = 约50万

**脚本逻辑：**
1. 先说概率：72%的人这辈子会得大病，不是吓你，是数据
2. 再说费用：以为32万？漏了4项，实际70万
3. 最后算期望值：72% × 70万 = 50万
4. 精算师结论：这50万是你的期望损失，不是可能，是数学期望

**开头：**
直接接上："上条我说帮你算一场大病要花多少钱，今天加上概率一起算，结果你不一定能承受。"

**结尾钩子：**
这50万的期望损失，精算师有没有办法转移？下条告诉你。

**风格：**
- 精算师用概率和数字说话
- 期望值公式要完整展示
- 口语化，有冲击力
- 不要故事

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
