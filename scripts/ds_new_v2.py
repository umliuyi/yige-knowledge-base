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
        {'role': 'user', 'content': '''帮我写第二条视频口播脚本（90秒）——“乐城的医疗资源，为什么别人用不上”

**这条视频的核心任务：**
- 种草乐城稀缺性，让观众觉得"这个东西我必须了解"
- 不是讲保险，是讲"为什么乐城是独特的"

**内容逻辑：**
1. 【反常识开场】你以为乐城是"有钱人去的地方"？错
2. 【揭示真相】乐城真正的门槛不是钱，是信息差+资源差
3. 【精算师视角】我见过的案例——有人的了病，拿着钱找不到乐城的门路

**关键信息：**
- 乐城是中国唯一医疗特区
- 国外几百种新药在乐城可以用，但内地要等3-5年审批
- 真正的门槛：不知道有这个选项，不知道怎么去，不知道找谁

**风格要求：**
- 开头用反问，直接挑战观众认知
- 有故事感，精算师见过的真实案例
- 结尾留悬念，为第三条铺垫

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