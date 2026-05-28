# -*- coding: utf-8 -*-
import urllib.request, ssl, re, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://mp.weixin.qq.com/s/wlh_RGiptczx_h_aK2LMKA'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://mp.weixin.qq.com/',
}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
html = resp.read().decode('utf-8', errors='ignore')

# Extract content
m = re.search(r'id="js_content"[^>]*>(.*?)</div>', html, re.DOTALL)
if m:
    raw = m.group(1)
    text = re.sub(r'<[^>]+>', '', raw)
    text = re.sub(r'\s+', ' ', text).strip()
    out = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_article_wlhr.txt'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'TEXT SAVED: {len(text)} chars')
    print('Preview:', text[:300])
else:
    print('NO CONTENT FOUND')
