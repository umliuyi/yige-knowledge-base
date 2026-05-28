# -*- coding: utf-8 -*-
"""用biz监控乐城先行区最新文章"""
import urllib.request, ssl, re, os, json
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BIZ = 'MzA3MTIwNQ=='
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://mp.weixin.qq.com/',
}

# 抓文章
url = 'https://mp.weixin.qq.com/s/wlh_RGiptczx_h_aK2LMKA'
req = urllib.request.Request(url, headers=HEADERS)
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
html = resp.read().decode('utf-8', errors='ignore')

m = re.search(r'id="js_content"[^>]*>(.*?)</div>', html, re.DOTALL)
if m:
    text = re.sub(r'<[^>]+>', '', m.group(1))
    text = re.sub(r'\s+', ' ', text).strip()
    out = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_lecheng_latest.txt'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(text)
    print('SAVED:', len(text), 'chars')
    print('Preview:', text[:200])
else:
    print('NO CONTENT')

# biz已保存到 .wechat_biz.txt
biz_path = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\.wechat_biz.txt'
with open(biz_path, 'w') as f:
    f.write(BIZ)
print('Biz saved:', BIZ)
