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
        {'role': 'system', 'content': '''你是一个真实的精算师，不是讲课，是在说话。
你说话的特点：
1. 直接、敢说、有观点，不废话
2. 经常反问听众，把他们拉进思考
3. 精算视角：你帮他们算账，不是卖东西
4. 口语化，像在跟朋友喝酒聊天，不是做报告
5. 有态度，精算师的判断，不模棱两可

最重要的：你是在跟一个普通人说话，不是在讲课。'''},
        {'role': 'user', 'content': '''帮我写第三条视频脚本（90秒）。

上一条我说过：CAR-T 120万，大多数人"用不起"。
今天我要告诉你一件更残忍的事。

**精算师要说的核心：**
就算你有钱，也不一定能用上乐城。
为什么？因为乐城专家号、床位、治疗通道都是稀缺资源。你排队，病情等不了。

**"用得上"vs"用得起"是两条线：**
- 用得起：钱的问题，算账能解决
- 用得上：资源的问题，有钱也买不到

**精算师立场（必须突出）：**
我做精算15年，见过太多人算清了钱，却没算清资源。
到最后，有钱也住不进那张床，约不到那个专家。
这是比没钱更残忍的事。

**互动引子：**
问观众：你身边有没有那种"有钱但找不到好医生"的例子？

**结尾钩子：**
下期告诉你：怎么锁定乐城医疗资源的入场券。

**要求：**
- 要像在说话，不是在讲逻辑
- 精算师有态度，不模棱两可
- 有反问，有情绪，不要平铺直叙
- 开头要抓人

格式：
---
【主体】（70秒，口语化）

---
【钩子】（20秒）
---'''}
    ],
    'max_tokens': 1000,
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
