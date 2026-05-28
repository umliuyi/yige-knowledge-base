# -*- coding: utf-8 -*-
import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://mp.weixin.qq.com/s/wlh_RGiptczx_h_aK2LMKA'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://mp.weixin.qq.com/'})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
html = resp.read().decode('utf-8', errors='ignore')

# Find biz
pat = r'var biz = "([^"]+)"'
m = re.search(pat, html)
if m:
    biz = m.group(1)
    print('Biz:', biz)
    path = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\.wechat_biz.txt'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(biz)
    print('Saved:', path)
else:
    # fallback
    for kw in ['biz', 'user_name']:
        idx = html.find(kw)
        if idx >= 0:
            print('Context:', html[max(0,idx-5:idx+80])
            break
    else:
        print('NOT FOUND')
