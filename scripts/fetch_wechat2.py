# -*- coding: utf-8 -*-
import urllib.request, ssl, re, os

DIR = r'C:\Users\Administrator\.openclaw-autoclaw\workspace'
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://mp.weixin.qq.com/s/jUT9zcatb4s0QX6bQjUhVQ'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://mp.weixin.qq.com/',
}

req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
html = resp.read().decode('utf-8', errors='ignore')

m = re.search(r'id="js_content"[^>]*>(.*?)</div>', html, re.DOTALL)
if m:
    raw = m.group(1)
    text = re.sub(r'<[^>]+>', '', raw)
    text = re.sub(r'\s+', ' ', text).strip()
    outpath = os.path.join(DIR, 'wechat_article.txt')
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(text)
    print('SAVED:', len(text), 'chars to', outpath)
else:
    print('NO CONTENT FOUND')
    # save debug
    outpath = os.path.join(DIR, 'wechat_debug.txt')
    with open(outpath, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(html[:3000])
    print('Saved debug to', outpath)
