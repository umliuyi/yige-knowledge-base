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
        {'role': 'system', 'content': '你是一个真实的精算师，在抖音做口播。说话直接，口语化，有观点，有态度。'},
        {'role': 'user', 'content': '''把下面这段话改顺，只改一处，不要加括号注释：

"银保监会数据：终身患大病概率72%。来，换个角度算。假如一个四口之家，按这个概率，未来大概有2到3口人，会得一场大病。2到3个人，每人50万起步，算算是多少钱？"

问题："假如一个四口之家，按这个概率，未来大概有2到3口人"这句逻辑有点乱。

要求：改成假如一个家庭四口人，按72%的概率，得大病的人数怎么算，然后乘以费用。

只改这一句，其他不变。
直接给我修改后的完整脚本，不需要解释。'''}
    ],
    'max_tokens': 800,
    'temperature': 0.5
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
