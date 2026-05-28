# -*- coding: utf-8 -*-
import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://mp.weixin.qq.com/s/wlh_RGiptczx_h_aK2LMKA'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://mp.weixin.qq.com/',
})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
html = resp.read().decode('utf-8', errors='ignore')

# Find biz in script vars
patterns = [
    r'var biz = "([^"]+)"',
    r"var biz = '([^']+)'",
    r'__biz[:=]([^&"\';\s]+)',
    r'biz_str[:=]([^&"\';\s]+)',
    r'"biz"\s*:\s*"([^"]+)"',
]

for pat in patterns:
    m = re.search(pat, html)
    if m:
        print(f'FOUND pattern: {pat[:30]} -> {m.group(1)[:50]}')
        break
else:
    # fallback: search raw
    idx = html.find('biz')
    if idx > 0:
        print('biz context:', html[idx-5:idx+60])
    else:
        print('NOT FOUND anywhere in page')
