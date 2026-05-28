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
        {'role': 'system', 'content': '''你是一个真实的精算师，不是老师，不是医生。
你说话有这三个特点，缺一不可：
1. 你见过很多病人，你有自己的经历和感受
2. 你看到普通人看不到的数字背后的东西
3. 你说的话和别人的不一样，不是重复常识，是说一个别人没想过的事实

如果你只是讲道理，你就不配当这个精算师。'''},
        {'role': 'user', 'content': '''写糖尿病系列第三集口播脚本（90秒）——“干细胞治疗糖尿病是怎么回事”

这集要回答一个问题：干细胞为什么可能是解决糖尿病的新思路？

不要讲道理，要讲故事，要有精算师才有的洞察。

素材方向：
- 精算师见过的案例：（可以用假设性的案例）
- 精算师才有的洞察：干细胞解决的是什么问题，药物解决的是什么问题，为什么本质不同
- 精算师的判断：这个东西解决了什么，没解决什么，适合什么样的人

这集讲原理，但不要做医学科普。要让观众听完觉得：这个思路和以前的方法不一样。

内容要求：
1. 承接上集（药越吃越多的困境）
2. 用通俗比喻讲清原理（不用专业术语）
3. 要有精算师对"这个问题本质上是什么"的判断
4. 结尾铺垫下一集（价格和选择）

格式：直接给脚本正文，不要其他说明'''}
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
