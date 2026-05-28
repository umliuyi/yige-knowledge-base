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
        {'role': 'system', 'content': '''你是一个真实的精算师，在抖音做口播。说话直接，口语化，有观点，有态度。'''},
        {'role': 'user', 'content': '''帮我写第四条视频口播脚本（90秒）。

**前情（第三条结尾钩子）：**
"这笔账，精算师怎么帮算？下条告诉你。"
→ 第四条要接上，告诉观众怎么解决

**第四条核心任务：**
不是硬卖，是告诉观众：怎么把这笔账算清楚，怎么提前锁定乐城医疗资源。
引出权益卡，但不能太硬，要让观众觉得是自己得出的结论。

**产品信息（必须准确）：**
- 产品名：乐医无忧权益卡
- 价格：365元/年（每天1块钱）
- 核心权益：
  * 150万特药额度，0免赔，100%报销
  * CAR-T（奕凯达120万/针）全额直付
  * 14项健康管理服务
- 乐城背景：海南博鳌乐城先行区，中国唯一医疗特区

**脚本逻辑（按一哥要求）：**
1. 接上条钩子：150万账单，精算师怎么帮你算？（引出解决方案）
2. 精算师告诉你：这道题有解法
3. 引出权益卡：不是保险，是入场券
4. 核心卖点：365元/年，每天1块钱，锁定150万特药额度+CAR-T直付+14项服务
5. 精算师表态：用确定的小钱，锁不确定的大资源，这叫风险转移

**开头：**
直接接上条："上条算完了，150万的账单，精算师告诉你这道题有解法。"

**结尾钩子：**
引导评论：你觉得这道题，划不划算？

**风格：**
- 接上条有呼应
- 精算师有态度，精打细算
- 不能硬卖，要让观众觉得是自己得出的结论
- 口语化，有节奏

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
