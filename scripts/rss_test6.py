# -*- coding: utf-8 -*-
import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

rss_sources = [
    ('中华健康网2', 'https://www.cnk2009.com/rss/news'),
    ('名医网', 'https://www.ews telemedicine.com/rss'),
    ('爱爱医', 'https://www.iiyi.com/rss'),
    ('医梦园', 'https://www.imetal.com.cn/rss'),
    ('医学生网', 'https://www.med999.com/rss'),
    ('华厦医讯', 'https://www.huaxia.com/rss'),
    ('康健网', 'https://www.kangjian.net/rss'),
    ('健康网', 'https://www.gzsw.cc/rss'),
    ('健康网2', 'http://www.gzsw.cc/rss/'),
    ('健康网3', 'http://www.gzsw.cc/rss/health.xml'),
    ('健康网4', 'https://www.gzsw.cc/rss/health.xml'),
    ('医网', 'https://www.i-sw.cn/rss'),
    ('中华网健康', 'https://health.china.com/rss/'),
    ('凤凰健康', 'https://ishare.iclient.ifeng.com/rss/'),
    ('新民健康', 'https://health.xinmin.cn/rss'),
    ('生命时报', 'https://www.lifetimes.cn/rss'),
]

log = []
for name, url in rss_sources:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            raw = resp.read()
            for enc in ['utf-8', 'gbk', 'gb2312']:
                try:
                    content = raw.decode(enc); break
                except:
                    content = raw.decode('utf-8', errors='ignore')
        first500 = content[:500].lower()
        if '<rss' in first500 or '<feed' in first500 or '<?xml' in first500:
            log.append(f'OK {name}: {url}')
        else:
            log.append(f'FAIL {name}')
    except Exception as e:
        log.append(f'FAIL {name}: {str(e)[:50]}')

with open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206\rss_test6.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log))
print('done')