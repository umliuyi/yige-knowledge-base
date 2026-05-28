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
        {'role': 'user', 'content': '''写糖尿病系列第一集口播脚本（90秒）——“9000万人，和一个你不知道的真相”

真实数据（IDF Diabetes Atlas 2024，可直接使用）：
- 中国现有糖尿病患者：9000万（全球第一）
- 糖尿病高危人群（糖耐量受损/IGT）：1.4亿
- 西太区约50%患者不知道自己患病
- 预计2050年中国患者将达1.68亿
- 数据来源：IDF Diabetes Atlas 2024，引用N Engl J Med/JAMA/BMJ

内容要求：
1. 开头用真实数据引入：9000万，地球第一
2. 核心洞察：1.4亿高危人群 + 50%未诊率——意味着大量人不知道自己在走向并发症
3. 精算师视角：算过大病保险的人，看这个数据是什么感受
4. 结尾铺垫下一集：糖尿病为什么并发症这么多，药越吃越多是必然结果

风格：
- 有精算师的真实感受和判断
- 数据要硬，但要有洞察
- 结尾让人想看下一集

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
