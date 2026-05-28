# -*- coding: utf-8 -*-
import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

rss_sources = [
    ('39健康网', 'https://www.39.net/rss/'),
    ('飞华健康网', 'https://www.fh21.com.cn/rss/'),
    ('99健康网', 'https://www.99.com.cn/rss/'),
    ('有问必答健康网', 'https://www.120.net/rss'),
    ('中华健康网', 'https://www.cnk2009.com/rss'),
    ('健康网', 'https://www.gzsw.cc/rss/'),
    ('健康报网', 'https://www.jkb.com.cn/rss'),
    ('人人健康网', 'https://www.rrjk.net/rss'),
    ('百姓健康网', 'https://www.bxjb.net/rss'),
    ('大众健康网', 'https://www.dzjk.cn/rss'),
    ('医学论坛网', 'https://www.cmt.com.cn/rss'),
    ('39健康网资讯', 'https://news.39.net/rss/'),
    ('中国健康网', 'https://www.cn69.com/rss'),
    ('放心医苑', 'https://www.fangxin.com/rss/'),
    ('飞华健康网2', 'https://www.fh21.com.cn/rss/health.xml'),
]

log = []
for name, url in rss_sources:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            raw = resp.read()
            # 尝试多种编码
            for enc in ['utf-8', 'gbk', 'gb2312']:
                try:
                    content = raw.decode(enc)
                    break
                except:
                    content = raw.decode('utf-8', errors='ignore')
        first500 = content[:500].lower()
        if '<rss' in first500 or '<feed' in first500 or '<?xml' in first500:
            log.append(f'OK {name}: {url}')
        else:
            log.append(f'FAIL {name}: non-RSS')
    except Exception as e:
        log.append(f'FAIL {name}: {str(e)[:60]}')

with open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206\rss_test5.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log))
print('done')