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
        {'role': 'user', 'content': '''写糖尿病系列第二集口播脚本（90秒）——“药越吃越多，针越打越多”

这集要回答一个问题：为什么传统治疗越来越不够用？

不要讲道理，要讲故事，要有精算师才有的洞察。

素材方向：
- 精算师见过的案例：客户从1种药吃到7种的
- 精算师才有的洞察：降糖药本质是什么（强迫β细胞工作），为什么这条路走不通
- 精算师的判断：这个过程不可逆，药物在短期内控制指标，长期在加重病情

不要只是陈述事实，要让观众看完后有"原来如此"的感觉。

内容要求：
1. 承接上集自然（不要重复上集内容）
2. 核心：为什么药越吃越多是必然结果，不是"控制不好"
3. 要有精算师才有的洞察
4. 结尾铺垫下一集

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
