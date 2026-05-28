# -*- coding: utf-8 -*-
import urllib.request, ssl, json, sys
sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

API_KEY = 'sk-18a62cec69c54b7196803c7ecdcbef81'

# 糖尿病
payload1 = {
    'model': 'deepseek-chat',
    'messages': [
        {'role': 'system', 'content': '你是一个精算师，服务于海南乐城医疗特区。风格：理性、精准、有观点，口语化，有态度。每条视频要有精算师视角：用数字说话，有观点，有判断。不煽情，不恐吓，用数据说服人。'},
        {'role': 'user', 'content': '''写第一期视频口播脚本（90秒），主题：干细胞治疗糖尿病，乐城有什么不一样。

内容要求：
1. 开场：糖尿病数据引入（1.4亿患者）
2. 项目是什么：干细胞修复胰岛细胞原理（通俗版）
3. 适合人群：2型糖尿病，用≥3种降糖药控制不佳者
4. 价格：5.98万/针×3≈18万疗程（慈铭）；GLP-1双因子36万/疗程（瑞金海南）
5. 结尾钩子：引出下一期（免疫细胞治疗和干细胞有什么区别？）

格式：直接给脚本正文'''}
    ],
    'max_tokens': 700,
    'temperature': 0.7
}

# DC/NK
payload2 = {
    'model': 'deepseek-chat',
    'messages': [
        {'role': 'system', 'content': '你是一个精算师，服务于海南乐城医疗特区。风格：理性、精准、有观点，口语化，有态度。每条视频要有精算师视角：用数字说话，有观点，有判断。不煽情，不恐吓，用数据说服人。'},
        {'role': 'user', 'content': '''写第二期视频口播脚本（90秒），主题：DC/NK细胞免疫治疗，肿瘤患者的新选择。

内容要求：
1. 开场：传统肿瘤治疗五年生存率低（胰腺癌<10%，肺癌<20%）
2. 项目是什么：DC细胞（情报员）+NK细胞（杀手）通俗原理
3. 适合人群：晚期实体瘤标准治疗失败者；术后防复发
4. 价格：胰腺癌DC 38万/次（博鳌超级）；NK 20万/6针（华西城东）
5. 结尾钩子：引出下一期（干细胞不只是治糖尿病，骨关节也能用，下一期说膝关节）

格式：直接给脚本正文'''}
    ],
    'max_tokens': 700,
    'temperature': 0.7
}

# 膝关节
payload3 = {
    'model': 'deepseek-chat',
    'messages': [
        {'role': 'system', 'content': '你是一个精算师，服务于海南乐城医疗特区。风格：理性、精准、有观点，口语化，有态度。每条视频要有精算师视角：用数字说话，有观点，有判断。不煽情，不恐吓，用数据说服人。'},
        {'role': 'user', 'content': '''写第三期视频口播脚本（90秒），主题：膝关节干细胞，不用换关节的新选择。

内容要求：
1. 开场：膝关节问题普遍性（60岁以上发病率50%）
2. 项目是什么：干细胞修复软骨（"修零件"vs"换零件"）
3. 适合人群：骨关节炎早中期；半月板损伤不想开刀者
4. 价格：髋骨关节炎 3.635万/针；膝骨关节炎 3.635万/针；半月板 8万/单膝（乐城官方）
5. 结尾钩子：引出下一期（干细胞还能治呼吸系统，下一期说慢阻肺）

格式：直接给脚本正文'''}
    ],
    'max_tokens': 700,
    'temperature': 0.7
}

# 慢阻肺
payload4 = {
    'model': 'deepseek-chat',
    'messages': [
        {'role': 'system', 'content': '你是一个精算师，服务于海南乐城医疗特区。风格：理性、精准、有观点，口语化，有态度。每条视频要有精算师视角：用数字说话，有观点，有判断。不煽情，不恐吓，用数据说服人。'},
        {'role': 'user', 'content': '''写第四期视频口播脚本（90秒），主题：慢阻肺干细胞，让你的肺重获新生。

内容要求：
1. 开场：中国1亿慢阻肺患者，每年100万人死亡
2. 项目是什么：气道基底层干细胞修复肺泡（"修肺"vs"换肺"）
3. 适合人群：中重度COPD，药物控制不佳，无严重合并症
4. 价格：15万/针（瑞金医院海南医院）
5. 结尾：总结四期内容，引出后续——这些都只是开始，乐城还有更多前沿疗法，关注我，慢慢告诉你

格式：直接给脚本正文'''}
    ],
    'max_tokens': 700,
    'temperature': 0.7
}

def ds_call(payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        'https://api.deepseek.com/chat/completions',
        data=data,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
    )
    resp = urllib.request.urlopen(req, timeout=60, context=ctx)
    result = json.loads(resp.read().decode('utf-8'))
    return result['choices'][0]['message']['content']

print('=== 第一期：糖尿病干细胞 ===')
print(ds_call(payload1))
print()
print('=== 第二期：DC/NK细胞免疫 ===')
print(ds_call(payload2))
print()
print('=== 第三期：膝关节干细胞 ===')
print(ds_call(payload3))
print()
print('=== 第四期：慢阻肺干细胞 ===')
print(ds_call(payload4))