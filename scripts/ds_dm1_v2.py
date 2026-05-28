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
        {'role': 'system', 'content': '''你是一个真实的精算师，不是老师，不是医生。
你说话有这三个特点，缺一不可：
1. 你见过很多病人，你有自己的经历和感受
2. 你看到普通人看不到的数字背后的东西
3. 你说的话和别人的不一样，不是重复常识，是说一个别人没想过的事实

如果你只是讲道理，你就不配当这个精算师。'''},
        {'role': 'user', 'content': '''写糖尿病系列第一集口播脚本（90秒）——“中国1.4亿人得了这个病”

这集要回答一个问题：糖尿病真正的可怕是什么？

不要讲道理，要讲故事，要有精算师才有的洞察。
可以用的素材：
- 精算师见过的案例
- 精算师才看得到的数据
- 普通人想不到的角度

举一个精算师视角的例子：
"我见过一个客户，血糖8点，他觉得没什么。8年后，心梗放了2个支架。他算过账吗？没算过。他算过如果心梗，成本是多少吗？没算过。"

内容要求：
1. 开头要抓人，有精算师的独特视角
2. 核心讲清楚：糖尿病真正的危险不是血糖高，而是并发症
3. 要有让观众"啊原来如此"的洞察
4. 结尾自然引出下一集

风格：有精算师的态度和经历，不要只是在陈述事实

格式：直接给脚本正文，不要其他说明'''}
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
