# -*- coding: utf-8 -*-
import urllib.request, ssl, sys, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

rss_sources = [
    ('动脉网', 'https://www.vcbeat.net/rss'),
    ('丁香园', 'https://www.dxy.cn/rss'),
    ('生物谷', 'https://www.bioon.com/rss/news.rss'),
    ('梅斯医学', 'https://www.medsci.cn/rss'),
    ('药明康德', 'https://www.wuxiapptec.com/rss'),
]

log = []
for name, url in rss_sources:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            raw = resp.read()
            content = raw.decode('utf-8', errors='ignore')
        first500 = content[:500].lower()
        if '<rss' in first500 or '<feed' in first500 or '<?xml' in first500:
            log.append(f'OK {name}: {url}')
        else:
            log.append(f'FAIL {name}: non-RSS content')
    except Exception as e:
        log.append(f'FAIL {name}: {str(e)[:60]}')

with open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206\rss_test.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log))
print('done')