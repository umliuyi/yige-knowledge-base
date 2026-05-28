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
        {'role': 'user', 'content': '''写糖尿病系列第三集口播脚本（90秒）——“能不能让身体长出新的β细胞”

这一集的核心任务：
承接上集（β细胞累死了，能不能有新的）——讲清楚干细胞为什么可能是解决思路。

内容要求：
- 承接上集的逻辑（既然β细胞累死了，能不能补充新的）
- 用通俗比喻讲清楚干细胞的治疗逻辑
- 精算师的判断：这个东西解决了什么，没解决什么，适合什么人
- 结尾铺垫下一集（价格和选择）

风格：精算师视角，有判断，不是纯科普

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
