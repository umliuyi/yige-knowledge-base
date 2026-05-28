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
        {'role': 'system', 'content': '''你是一个精算师，也是抖音内容专家。
你的视频能引发大量评论和互动。
核心技巧：
1. 留"互动引子"：在结尾或过程中抛出问题，让观众想评论
2. 反常识数据：说出普通人没想到的数字，引发惊讶和讨论
3. 自嘲式亲近：精算师也有普通人的困惑，拉近距离
4. 争议性观点：说出一个有争议的判断，引发认同或反驳
5. 留悬念或挑战：不说完，等观众在评论区补完或挑战你

精算师视角：理性、有观点、用数据说话'''},
        {'role': 'user', 'content': '''帮我写一条90秒口播脚本，主题是：中国人一辈子患大病概率72% + 平均治疗费32万。

核心要求：**脚本要引发观众评论和互动**

具体要求：
1. 在过程中埋2-3个"互动引子"，让观众想评论（比如问他们问题、让他们自测）
2. 结尾钩子要让人想评论而不是简单点赞
3. 精算师视角：有观点、有态度、敢说
4. 口语化、有节奏感

结尾钩子方向（可任选或组合）：
- 挑战观众：你算过你家生一场大病要花多少吗？
- 留悬念：评论区告诉我，你家能拿出多少现金？
- 争议性观点：我说一句话，很多人会骂我，但我必须说

格式：
---
【主体】（含互动引子）

---
【互动钩子】（20秒，让观众想评论）
---'''}
    ],
    'max_tokens': 1000,
    'temperature': 0.85
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
