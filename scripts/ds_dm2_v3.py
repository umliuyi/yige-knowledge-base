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
        {'role': 'user', 'content': '''写糖尿病系列第二集口播脚本（90秒）——“你的身体每天怎么降血糖的，为什么越来越不灵了”

这一集的核心任务：
用通俗的方式讲清楚人体调节血糖的生理机制——胰岛素是怎么工作的，β细胞是怎么慢慢累死的。
不是做医学科普，是让观众理解一个核心洞察：糖尿病的本质是β细胞功能衰竭，而药物只能刺激残余β细胞工作，这条路越来越窄。

内容要求：
- 先讲清楚人体正常的血糖调节机制（通俗比喻）
- 然后讲清楚为什么2型糖尿病人的β细胞越来越累，功能越来越差
- 结尾要自然引出下一集：既然β细胞累死了，能不能有新的β细胞来代替？（引出干细胞）

风格：
- 有生理机制的讲解，但要非常通俗
- 有精算师的洞察（为什么这条路走不通）
- 结尾的钩子是"新β细胞"这个概念，自然带出下一集

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
