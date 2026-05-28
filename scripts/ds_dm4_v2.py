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
        {'role': 'user', 'content': '''写糖尿病系列第四集口播脚本（90秒）——“18万换一个选择，值不值”

这集要回答一个问题：花18万用干细胞治疗糖尿病，精算师怎么算这笔账？

不要讲道理，要讲故事，要有精算师才有的洞察。

素材方向：
- 精算师算过的账：18万和一辈子吃药的累计成本
- 精算师才有的判断：这个东西不是买根治，是买什么
- 精算师见过的案例：（可以用假设性的）
- 精算师的结论：值不值，要看什么

精算师的特点：算账算得很清楚，但不是让你花钱，是让你知道钱花得明不明。

内容要求：
1. 承接上集（原理讲完了，这集讲价格和选择）
2. 官方数据：慈铭博鳌18万/疗程；瑞金海南36万/疗程
3. 精算师要算清楚这笔账，同时要给判断
4. 结尾可以是这一集的收尾，也可以有对整个系列的回顾，但不要太重

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
