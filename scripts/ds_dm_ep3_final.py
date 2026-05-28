# -*- coding: utf-8 -*-
import urllib.request, ssl, json, sys
sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

API_KEY = 'sk-18a62cec69c54b7196803c7ecdcbef81'

payload3 = {
    'model': 'deepseek-chat',
    'messages': [
        {'role': 'system', 'content': '你是一个真实的精算师，不是老师，不是医生。你说话有三个特点：1. 你见过很多病人，有自己的经历和感受；2. 你看到普通人看不到的数字背后的东西；3. 你说的话和别人不一样，是说一个别人没想过的事实。'},
        {'role': 'user', 'content': '''写糖尿病系列第三集口播脚本（90秒）——“能不能让身体长出新的β细胞”

承接上集：上集说了β细胞被累死的机制，这集问：能不能补充新的β细胞？

内容要求：
1. 承接上集的逻辑
2. 通俗比喻讲清楚干细胞治疗糖尿病的原理（不是做医学科普，是让观众理解这个思路）
3. 乐城官方数据：2型糖尿病，5.98万/针×3≈18万（慈铭博鳌）
4. 精算师的判断：适合什么人，什么人不适合
5. 结尾铺垫下一集：18万值不值

风格：精算师视角，有判断

格式：直接给脚本正文'''}
    ],
    'max_tokens': 800,
    'temperature': 0.8
}

data = json.dumps(payload3).encode('utf-8')
req = urllib.request.Request(
    'https://api.deepseek.com/chat/completions',
    data=data,
    headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
)
resp = urllib.request.urlopen(req, timeout=60, context=ctx)
result = json.loads(resp.read().decode('utf-8'))
print('=== 第三集 ===')
print(result['choices'][0]['message']['content'])

payload4 = {
    'model': 'deepseek-chat',
    'messages': [
        {'role': 'system', 'content': '你是一个真实的精算师，不是老师，不是医生。你说话有三个特点：1. 你见过很多病人，有自己的经历和感受；2. 你看到普通人看不到的数字背后的东西；3. 你说的话和别人不一样，是说一个别人没想过的事实。'},
        {'role': 'user', 'content': '''写糖尿病系列第四集口播脚本（90秒）——“18万换一个选择，值不值”

承接上集：上集说了干细胞治疗糖尿病的原理，这集精算师算清楚这笔账。

内容要求：
1. 承接上集（原理讲完了，精算师算账）
2. 乐城官方数据：慈铭博鳌，18万/疗程；瑞金海南，36万/疗程
3. 精算师算账：18万和长期吃药的累计成本对比
4. 精算师的判断：这笔钱买的是什么（不是根治，是选择权）
5. 结尾：开放式收尾

风格：精算师算账，有数字有判断

格式：直接给脚本正文'''}
    ],
    'max_tokens': 800,
    'temperature': 0.8
}

data = json.dumps(payload4).encode('utf-8')
req = urllib.request.Request(
    'https://api.deepseek.com/chat/completions',
    data=data,
    headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
)
resp = urllib.request.urlopen(req, timeout=60, context=ctx)
result = json.loads(resp.read().decode('utf-8'))
print('=== 第四集 ===')
print(result['choices'][0]['message']['content'])
