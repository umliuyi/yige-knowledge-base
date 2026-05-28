# -*- coding: utf-8 -*-
import urllib.request, ssl, sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

rss_sources = [
    ('丁香园-论坛', 'https://www.dxy.cn/bbs/rss'),
    ('丁香园-专题', 'https://www.dxy.cn/special/rss'),
    ('中国医学论坛报', 'https://www.cmt.com.cn/rss'),
    ('搜狐健康', 'https://health.sohu.com/rss/'),
    ('新浪健康', 'https://health.sina.com.cn/rss/health.xml'),
    ('凤凰健康', 'https://health.ifeng.com/rss/'),
    ('腾讯健康', 'https://health.qq.com/rss/'),
    ('人民日报健康', 'https://www.jksb.com.cn/rss'),
    ('中国科学报', 'https://news.sciencenet.cn/rss.aspx'),
    ('观察者网-健康', 'https://www.guancha.cn/rss'),
    ('医学微视', 'https://www.mlylg.com/rss'),
    ('AIP', 'https://www.aip.org/rss'),
    ('Frontiers', 'https://www.frontiersin.org/rss'),
    ('MediLive', 'https://www.medilive.cn/rss'),
    ('MedSci', 'https://www.medsci.cn/sci/rss'),
]

log = []
for name, url in rss_sources:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            raw = resp.read()
            content = raw.decode('utf-8', errors='ignore')
        first500 = content[:500].lower()
        if '<rss' in first500 or '<feed' in first500 or '<?xml' in first500:
            log.append(f'OK {name}: {url}')
        else:
            log.append(f'FAIL {name}: non-RSS')
    except Exception as e:
        log.append(f'FAIL {name}: {str(e)[:60]}')

with open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206\rss_test3.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log))
print('done')