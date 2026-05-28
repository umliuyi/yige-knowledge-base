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
        {'role': 'user', 'content': '''重新写糖尿病系列第一集开头（90秒）——“1.4亿人，和一个你不知道的真相”

之前版本的问题：开头说"我见过1.4亿份糖尿病理赔单"，这个太假了，精算师不可能见过所有理赔单，观众会觉得假。

请重新写一个真实的、有说服力的开头。

要求：
- 开头要有冲击力，但不能用夸张的"我见过X亿"这种不真实的说法
- 可以用：精算师的工作中常见什么类型的糖尿病案例；精算师算过多少个大病家庭的账；见过的最冲击的案例是什么
- 核心内容不变：糖尿病可怕的不是血糖高，而是并发症；药越吃越多是必然结果
- 要有精算师的真实感受和判断
- 90秒内容量：糖尿病现状（并发症）+ 传统治疗的困境

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
