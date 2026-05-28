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
        {'role': 'user', 'content': '''修改下面这个脚本的一处：

把"你家""你作为家庭支柱""你算算"这类称呼全部改成"假如一个家庭""假如作为家庭支柱""假如一个四口之家"这样的虚拟假设语气。不要直接称呼观众"你"。

脚本原文：
上条我说帮你算一场大病要花多少钱，今天我算完了，先说结论——这个数字比你想象的要大得多。

32万。卫健委年鉴数据。这是治疗费：手术、ICU、靶向药、化疗，加一块的平均数。

但32万只是治疗费。还有康复营养费，你算过吗？还有误工费，你作为家庭支柱，病了不工作，钱从哪来？还有陪护费，护工一个月多少钱？这些加进去，轻轻松松超过50万。

如果你想去乐城用国外新药，CAR-T，一针120万，有的甚至更高。32万只是起步价，不是天花板。

银保监会数据：终身患大病概率72%。来，我帮你换个角度算。你家几口人？4口？那按这个概率，你家未来大概有2到3口人，会得一场大病。2到3个人，每人50万起步，你算算是多少钱？

这才是你面对的真实数字。不是一个人的账，是一家人的账。

这笔账，精算师怎么帮你算？下条告诉你。'''}
    ],
    'max_tokens': 800,
    'temperature': 0.6
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
