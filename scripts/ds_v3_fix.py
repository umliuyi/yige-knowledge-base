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
精算师说话：精准、有观点、不糊弄。
你有一个重要原则：数字必须经得起专业质疑。
不能用错误的算法糊弄观众，精算师要对自己说的每个数字负责。
说话直接，口语化，有态度。'''},
        {'role': 'user', 'content': '''帮我写第三条视频口播脚本（90秒）。

**第二条结尾（必须接上）：**
"下一条，我算给你看：一场大病，到底要花多少钱。"
→ 第三条就是算这笔账

**精算师算账（必须准确）：**
1. 大病概率：72%（银保监会终身累计发病率）
2. 大病费用：70万（治疗32万+康复10万+误工24万+陪护6万）
3. 正确用法：不是用72%×70万算期望值，而是告诉你这两件事是独立的——
   - 72%是概率问题
   - 70万是费用问题
   - 两个问题都要解决

**脚本逻辑：**
1. 先说概率：72%的人这辈子会得大病（银保监会数据）
2. 再说费用：以为32万？漏了4项，实际70万
3. 精算师要告诉你的：概率和费用是两件事，都要算清楚
4. 结论：算清楚之后，你会发现你面对的是两个问题，不是一个

**重要提醒：**
不能把72%和70万直接相乘来算期望值，那是错误的算法。
可以说：72%的人要面对70万的损失，这两件事同时发生在你身上的交集，你扛得住吗？

**开头：**
直接接上："上条我说帮你算一场大病要花多少钱，今天把概率和费用一起算给你看。"

**结尾钩子：**
两个问题都算清楚了，怎么解决？下条告诉你。

**风格：**
- 精算师准确、严谨
- 不要错误算法
- 口语化，有冲击力

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
