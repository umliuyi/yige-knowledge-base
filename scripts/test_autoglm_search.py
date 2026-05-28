import urllib.request
import json
import hashlib
import time
import ssl

def do_search(query):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Get token
    token_resp = urllib.request.urlopen('http://127.0.0.1:18432/get_token', timeout=5)
    token = token_resp.read().decode().strip()

    # Sign
    appid = '100003'
    ts = str(int(time.time()))
    secret = '38d2391985e2369a5fb8227d8e6cd5e5'
    sig = hashlib.md5((appid + '&' + ts + '&' + secret).encode()).hexdigest()

    # Search
    payload = json.dumps({'queries': [{'query': query}]}).encode()
    req = urllib.request.Request(
        'https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/web-search',
        data=payload, method='POST',
        headers={
            'Authorization': token,
            'X-Auth-Appid': appid,
            'X-Auth-TimeStamp': ts,
            'X-Auth-Sign': sig,
            'Content-Type': 'application/json'
        }
    )
    resp = urllib.request.urlopen(req, timeout=20, context=ctx)
    result = json.loads(resp.read())
    return result

# Test 1: basic search
print('=== Test 1: 干细胞糖尿病最新 2026 ===')
r = do_search('干细胞糖尿病最新 2026')
code = r.get('code')
msg = r.get('msg')
print('code:', code, '| msg:', msg)
data = r.get('data')
if data and data.get('results') and data['results'][0]:
    webp = data['results'][0].get('webPages', {})
    items = webp.get('value', [])
    print('返回结果条数:', len(items))
    for it in items[:3]:
        print('  -', it.get('name', ''))
        snippet = it.get('snippet', '')
        print('   ', snippet[:100])
else:
    print('data:', str(data)[:200])

# Test 2: second search to check quota
print()
print('=== Test 2: 乐城特许医疗最新进展 ===')
r2 = do_search('乐城特许医疗最新进展')
code2 = r2.get('code')
msg2 = r2.get('msg')
print('code:', code2, '| msg:', msg2)