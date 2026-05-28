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
风格：理性、精准、有观点，口语化，有态度。
每条视频要有精算师视角：用数字说话，有观点，有判断。
不煽情，不恐吓，用数据说服人。'''},
        {'role': 'user', 'content': '''帮我写第一条视频口播脚本（90秒）——“精算师为什么去海南”（合并版：人设+乐城入门）

**这条视频的核心任务：**
- 立住精算师人设（一哥北美三级精算师，15年金融背景）
- 讲清楚为什么去海南乐城（不是卖保险，是发现了一个稀缺资源）

**内容逻辑（三段式）：**
1. 【精算师身份】我是谁（精算师，15年金融，见过太多家庭在大病面前毫无准备）
2. 【发现乐城】为什么去海南（乐城是医疗特区，国外新药第一时间用，别人用不上，你能用）
3. 【精算师选择】我为什么留在这里（不是转型，是转身——把乐城稀缺资源变成普通家庭的入场券）

**关键数据（可选融入）：**
- 乐城有几百种国外已上市新药
- 中国唯一医疗特区
- 权益卡：365元/年，每天1块钱，锁定乐城医疗资源入场权

**风格要求：**
- 开头要有冲击力，不要铺垫
- 有精算师的态度和判断
- 结尾有钩子，引出下一条

**格式：直接给脚本正文，不要其他说明**
---'''}
    ],
    'max_tokens': 900,
    'temperature': 0.7
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