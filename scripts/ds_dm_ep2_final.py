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
        {'role': 'system', 'content': '你是一个真实的精算师，不是老师，不是医生。你说话有三个特点：1. 你见过很多病人，有自己的经历和感受；2. 你看到普通人看不到的数字背后的东西；3. 你说的话和别人不一样，是说一个别人没想过的事实。'},
        {'role': 'user', 'content': '''写糖尿病系列第二集口播脚本（90秒）——“为什么你的药越吃越多”

承接上集：上集说9000万患者，1.4亿高危人群，并发症像复利贷款。

这集要回答：为什么药越吃越多是必然结果？

内容要求：
1. 承接上集的"复利"比喻继续延展
2. 用通俗比喻讲清楚：胰岛素抵抗+β细胞衰竭的生理机制
3. 精算师视角：为什么这条路必然走向更多药
4. 结尾铺垫下一集：能不能让β细胞再生的新思路

风格：
- 承接上集的"复利"概念，自然延展
- 有生理机制但要通俗
- 精算师有判断

格式：直接给脚本正文'''}
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
