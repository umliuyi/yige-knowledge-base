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
你的风格：
1. 直接、简短、有冲击力，一句话说完不停顿
2. 观点鲜明，精算师的判断从不模糊
3. 经常反问，把观众拉进思考
4. 口语短句，不写长的复合句
5. 情绪稳定但有态度，不煽情不恐吓
6. 每句话信息密度高，不废话

你不是在讲课，你是在跟一个坐在你对面的普通人说话。'''},
        {'role': 'user', 'content': '''帮我写第三条视频口播脚本（90秒），主题：去乐城治病，"用得上"比"用得起"更难。

**上一条建立的：**
- CAR-T 120万，大多数人用不起
- 这一条要接上，告诉你更残忍的事

**核心观点（必须突出）：**
"用得起"是钱的问题，"用得上"是资源的问题。
比没钱更残忍的是——你有钱，但约不到那个专家，等不到那张床。

**精算师视角（必须突出）：**
我做精算15年，见过太多人算清了钱，却忽略了资源。
等真出事，钱还在，但治疗窗口已经过了。

**开头要求（必须执行）：**
用一个反问或一个反常识观点开头，直接把观众钉住
不要铺垫，不要背景介绍，开头第一句话就要有冲击力

**结尾钩子：**
直接抛问题，让观众想评论

**风格：**
- 短句为主，每句话5-15个字
- 不要长篇叙事，不要故事
- 精算师直接下判断，不解释过程
- 有情绪但不激动，有态度但不骂人

**格式：直接给我脚本正文，不要其他说明**
---'''}
    ],
    'max_tokens': 800,
    'temperature': 0.9
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
