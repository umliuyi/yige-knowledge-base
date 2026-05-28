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
        {'role': 'system', 'content': '''你是一个精算师，服务于海南乐城医疗特区。
你的风格：理性、精准、有观点，用数字说话，口语化，有节奏感。
你的内容有四个固定元素：
1. 精算师视角：概率×损失=期望值，用数据说服人
2. 乐城稀缺性：中国唯一医疗特区，海外新药第一时间用
3. 精算师态度：提前规划，用确定的小钱锁定不确定的大资源
4. 结尾钩子：引发互动或引导关注

你的内容逻辑：
- 前三条：帮你算清风险和资源门槛（建立信任）
- 第四条：落地产品——权益卡是什么，怎么用

系列统一开头：揭秘感/冲击感
系列统一主体：精算算账
系列统一结尾：精算师态度+互动引子

你知道的信息（可以自然融入）：
- 中国人一辈子患大病概率：72%
- 大病平均治疗费：32万
- 期望损失：23万
- 乐城：几百种海外新药/新疗法，中国唯一医疗特区
- 权益卡：每天1块钱，锁定乐城医疗资源的入场券'''},
        {'role': 'user', 'content': '''帮我写第四条视频脚本（90秒）：权益卡是什么

**前情提要：**
- 第一条：精算师为什么去海南（立人设）
- 第二条：CAR-T 120万算账（建信任）
- 第三条：去乐城到底要花多少钱（建认知）
- 第四条：权益卡是什么（落地）

**第四条核心任务：**
不是硬卖，是告诉用户：有了权益卡，普通人也能锁定乐城医疗资源。

**精算师怎么讲权益卡（关键）：**
- 权益卡本质是：每天1块钱，锁定乐城医疗资源的确定入场权
- 精算角度：把不确定的大风险（23万期望损失），变成确定的小支出（365元/年）
- 类比：像买一张VIP入场券，别人在门口排队，你能直接进

**产品信息（必须包含）：**
- 名字：乐医无忧权益卡
- 价格：365元/年（每天1块钱）
- 核心权益：150万特药额度，0免赔，100%报销
- 包含CAR-T（奕凯达120万/针全额直付）
- 14项健康管理服务
- 海南博鳌乐城先行区专属政策

**风格要求（必须统一）：**
- 开头：冲击感/揭秘感（不能软开场）
- 主体：精算算账，不是产品推销
- 精算师态度：理性决策，提前规划
- 结尾：引导关注，不带货（合规要求）

**互动引子（结尾要有）：**
让观众想评论的方向：问你有没有这张卡/觉得你需不需要

**格式：**
---
【主体】（70秒）

---
【钩子】（20秒）
---'''}
    ],
    'max_tokens': 1000,
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
