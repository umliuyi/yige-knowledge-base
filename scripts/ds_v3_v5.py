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
你不是在讲课，你是在帮一个坐在对面的普通人算账。
说话直接，有观点，有态度。'''},
        {'role': 'user', 'content': '''帮我写第三条视频口播脚本（90秒）。

**第二条结尾（必须接上）：**
第二条我说过一句话："用到和用得起，是两件事。"
这句话说的是：有钱才能用，叫"用得起"；有资源才能用，叫"用得上"。
第二条重点在"用得起"——帮你算清大病费用够不够。

**第三条要接上：**
这一条要告诉观众：就算你算清了"用得起"，还得算清"用得上"。
因为"用得上"是一道更难的算术题。

**核心内容（接上第二条）：**
上条我说"用到和用得起是两件事"。
这句活的潜台词是：还有第三件事——"用得上"。
三条线：
1. 用到——有没有这个疗法
2. 用得起——钱够不够
3. 用得上——资源排得到不

这条要算"用得上"这道题：
- 乐城作为医疗特区，资源也是有限的
- 专家号、床位、治疗通道，都是稀缺资源
- 精算师告诉你：资源排队的数学期望，比费用更难算

**精算师的核心观点：**
"用得起"是可以凑钱解决的。
"用得上"是需要提前锁定才能解决的。
只算一条，等于没算完。

**开头要求：**
直接接上第二条那句"用到和用得起是两件事"往下说
不要重新铺垫

**结尾钩子：**
抛问题引发评论：你有没有想过，你能"用得上"的医疗资源有哪些？

**风格：**
- 口语化，有算账感
- 精算师直接下结论
- 数字要硬
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
