# -*- coding: utf-8 -*-
import urllib.request, ssl, sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

rss_sources = [
    ('丁香园-资讯', 'https://www.dxy.cn/rss/news'),
    ('丁香园-期刊', 'https://www.dxy.cn/rss/journal'),
    ('医脉通', 'https://www.medlive.cn/rss'),
    ('医学界', 'https://www.yxj.org.cn/rss'),
    ('健康界', 'https://www.cn-healthcare.com/rss'),
    ('新芽', 'https://xinyao.com.cn/feed'),
    ('药渡', 'https://www.yaodu.com.cn/rss'),
    ('佰黎妥', 'https://bailitop.com/feed'),
    ('生物探索', 'https://www.biodiscover.com/rss'),
    ('基因', 'https://www.genecards.cn/rss'),
    ('医药魔方', 'https://www.pharmcube.com/rss'),
    ('NEJM', 'https://www.nejm.org/rss'),
    (' Lancet', 'https://www.thelancet.com/rss'),
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
            log.append(f'FAIL {name}: non-RSS ({content[:100]})')
    except Exception as e:
        log.append(f'FAIL {name}: {str(e)[:80]}')

with open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206\rss_test2.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log))
print('done')