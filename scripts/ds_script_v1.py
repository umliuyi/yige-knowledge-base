# -*- coding: utf-8 -*-
"""DeepSeek文案生成脚本"""
import urllib.request, ssl, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

API_KEY = 'sk-18a62cec69c54b7196803c7ecdcbef81'
MODEL = 'deepseek-chat'

def ds_chat(system, user_prompt, max_tokens=800):
    payload = {
        'model': MODEL,
        'messages': [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': user_prompt}
        ],
        'max_tokens': max_tokens,
        'temperature': 0.7
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        'https://api.deepseek.com/chat/completions',
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }
    )
    resp = urllib.request.urlopen(req, timeout=30, context=ctx)
    result = json.loads(resp.read().decode('utf-8'))
    return result['choices'][0]['message']['content']

SYSTEM = '''你是一个短视频文案专家，帮用户生成60-90秒的口播脚本。
风格：口语化、自然、有观点、直接、有传播性、符合抖音算法偏好。
要求：每条30-60字，有节奏感，适合真人出镜口播'''

USER = '''帮我写一条60秒口播脚本，主题是：中国人一辈子患大病的概率（72%，银保监会数据）和治疗费用（32万，卫健委数据），精算师人设，有观点有态度，结尾有钩子引导关注'''

print(ds_chat(SYSTEM, USER))
