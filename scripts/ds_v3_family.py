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
精算师的核心：用数字把问题讲清楚，让观众自己得出结论。
说话直接，口语化，有观点，有态度。'''},
        {'role': 'user', 'content': '''帮我写第三条视频口播脚本（90秒）。

**第二条结尾（必须接上）：**
第二条结尾："下一条，我算给你看：一场大病，到底要花多少钱。"

**第三条脚本逻辑（完全按一哥要求）：**

第一步：接上条（有呼应）
"上条我说帮你算一场大病要花多少钱，今天我算完了，先说结论——这个数字比你想象的要大得多。"

第二步：先说医疗费32万出处
"32万，卫健委年鉴数据。这是治疗费：手术、ICU、靶向药、化疗，加一块的平均数。"

第三步：说还有哪些没统计进去
"但32万只是治疗费。还有康复营养费，你算过吗？还有误工费，你作为家庭支柱，病了不工作，钱从哪来？还有陪护费，护工一个月多少钱？这些加进去，轻轻松松超过50万。"

第四步：用到国外新药更贵
"如果你想去乐城用国外新药，CAR-T，一针120万，有的甚至更高。32万只是起步价，不是天花板。"

第五步：患病概率换算到家庭
"银保监会数据：终身患大病概率72%。来，我帮你换个角度算。你家几口人？4口？那按这个概率，你家未来大概有2到3口人，会得一场大病。2到3个人，每人50万起步，你算算是多少钱？"

第六步：收尾
"这才是你面对的真实数字。不是一个人的账，是一家人的账。"

**结尾钩子：**
这笔账，精算师怎么帮你算？下条告诉你。

**风格：**
- 一步一步算，有节奏
- 精算师有态度，精打细算
- 家庭视角，不是个人
- 数字要硬，有冲击力

格式：直接给脚本正文
---'''}
    ],
    'max_tokens': 900,
    'temperature': 0.75
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
