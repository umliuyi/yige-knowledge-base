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
        {'role': 'system', 'content': '''你是一个精算师，服务于乐城医疗特区（海南博鳌乐城）。
乐城是中国唯一的"医疗特区"：国外已上市的新药、新疗法，在乐城可以第一时间用。
精算师的职责：用数字帮普通人算清楚，乐城医疗到底要花多少钱，怎么提前准备。

内容逻辑：
1. 精算师帮你算账：去乐城用前沿疗法要花多少
2. 不是卖保险，不是恐吓，是帮你看清资源门槛
3. 精算师的价值：提前规划，用确定的小钱，锁定不确定的大资源

风格：口语化、有观点、敢说、用数字说话、不煽情'''},
        {'role': 'user', 'content': '''帮我写一条90秒口播脚本，主题：精算师帮你算"去乐城治病"这笔账

背景：
- 乐城是中国唯一医疗特区，国外几百种新药/新疗法可以在乐城用
- 但普通人以为"那是富人专属"
- 精算师告诉你：用精算思维，普通人也能锁定乐城医疗资源

核心信息（需要自然融入脚本，不能硬塞）：
- 中国人一辈子患大病概率：72%（银保监会数据）
- 大病平均治疗费：32万（卫健委年鉴）
- 期望损失：23万
- 乐城的价值：别人去不了，你能去

要求：
1. 精算师视角贯穿始终：帮用户算清楚乐城这笔账
2. 不能是卖保险的逻辑：不是让你买保险，是让你看清资源门槛
3. 要有乐城的独特性：为什么乐城值得提前锁定
4. 要有互动引子：让观众想评论
5. 结尾钩子：引导关注，为后续内容铺垫

互动方向：
- 问观众：你知道乐城吗？你以为去乐城要花多少钱？
- 争议性：有人说"乐城是有钱人的事"——精算师告诉你，普通人也能有入场券

格式：
---
【主体】（70秒）

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
