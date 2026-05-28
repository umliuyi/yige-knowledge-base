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
你说话直接、有观点、用数字算账。
精算风格：把复杂问题变成一道数学题，让观众自己得出结论。
你不是在讲故事，你是在帮观众算账。'''},
        {'role': 'user', 'content': '''帮我写第三条视频口播脚本（90秒）。

**前情（第二条结尾）：**
"下一条，我算给你看：一场大病，到底要花多少钱。"
→ 第三条要接着这个"算账"的承诺往下走

**第三条核心（接上算账）：**
上一条算了"用得起"这笔账（120万CAR-T）。
这一条告诉你：就算你算清了"用得起"，你还得算清"用得上"。
因为"用得上"是一道更难的算术题。

**精算师算账内容：**
- 全国有CAR-T资质的医院：不到20家
- 能开CAR-T方案的专家：全国几十位
- 排队等待的患者：几万人
- 等待时间：几个月到一年
- 而治疗窗口：可能就是3-6个月

这道算术题说明什么？
说明你有钱，也得排队。排不上队，钱等于白算。

**精算师结论：**
"用得起"是可以用钱解决的问题。
"用得上"是需要提前锁定资源才能解决的问题。
两个都得算，不能只算一个。

**开头：**
直接接着上一条说，不用铺垫："上条我帮你算了120万的账，但今天我要告诉你一道更难的算术题。"

**结尾钩子：**
抛问题引发评论：你有没有算过，你的医疗资源排在第几位？

**风格：**
- 全程算账，数字要硬
- 精算师直接给结论，不废话
- 口语化、有节奏

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
