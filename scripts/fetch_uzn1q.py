# -*- coding: utf-8 -*-
import urllib.request, ssl, re, sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://mp.weixin.qq.com/s/uZN1QGDjT4_vKYJz5ej7iw'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://mp.weixin.qq.com/',
}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=20, context=ctx)
html = resp.read().decode('utf-8', errors='ignore')

# Extract biz
m = re.search(r'var biz = "([^"]+)"', html)
biz = m.group(1) if m else 'NOT FOUND'

# Extract content
m2 = re.search(r'id="js_content"[^>]*>(.*?)</div>', html, re.DOTALL)
if m2:
    raw = m2.group(1)
    text = re.sub(r'<[^>]+>', '', raw)
    text = re.sub(r'\s+', ' ', text).strip()
    out = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_uZN1Q.txt'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(f'Biz: {biz}\n\n')
        f.write(text)
    print(f'TEXT SAVED: {len(text)} chars')
    print('Preview:', text[:300])
else:
    print('NO CONTENT')
    print('Biz:', biz)