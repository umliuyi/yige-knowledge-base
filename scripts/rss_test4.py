# -*- coding: utf-8 -*-
import urllib.request, ssl, sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

rss_sources = [
    # 英文医学/健康RSS（可靠的）
    ('NIH News', 'https://www.nih.gov/news-events/news-releases/feed'),
    ('ScienceDaily-Health', 'https://www.sciencedaily.com/rss/health/medicine.xml'),
    ('MedicalNewsToday', 'https://rss.medicalnewstoday.com/clinicalnews.xml'),
    ('WebMD', 'https://rss.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC'),
    ('HealthDay', 'https://www.healthday.com/rss/news'),
    # 中文搜索类RSS
    ('丁香园搜索-糖尿病', 'https://www.dxy.cn/search/doRedirect?query=%E7%B3%96%E5%B0%BF%E7%97%85&type=rss'),
    ('丁香园搜索-肿瘤', 'https://www.dxy.cn/search/doRedirect?query=%E8%82%BF%E7%98%A4&type=rss'),
    # 其他
    ('丁香园-用药', 'https://drugs.dxy.cn/rss'),
    ('腾讯新闻-健康', 'https://news.qq.com/rss/health.xml'),
    ('少数派-健康', 'https://sspai.com/rss/tag/健康'),
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

with open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206\rss_test4.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log))
print('done')