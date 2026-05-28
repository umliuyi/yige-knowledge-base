import urllib.request
import re
import time

SOURCES = {
    "36氪": ("https://36kr.com/feed", "utf-8"),
    "丁香园": ("http://www.dxy.cn/rss/home.xml", "gbk"),
    "动脉网": ("https://vcbeat.top/Rss/News", "utf-8"),
    "健康界": ("https://www.cn-healthcare.com/rss/", "utf-8"),
    "第一财经": ("https://www.yicai.com/rss/news.xml", "utf-8"),
    "财新健康": ("https://feed.caixin.com/rss/latest.xml", "utf-8"),
    "医药魔方": ("https://data.pharmacodia.com/rss/news.xml", "utf-8"),
    "药明康德": ("https://www.cphi.com.cn/rss", "utf-8"),
}

HEALTH_KW = [
    '乐城', '海南', '医疗', '健康', '癌症', '肿瘤', '干细胞',
    '免疫', 'CAR-T', 'ADC', '新药', 'NMPA', '审批', '生物医学'
]

results = {}

for name, (url, encoding) in SOURCES.items():
    t0 = time.time()
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=8) as resp:
            ct = resp.headers.get('Content-Type', '')
            raw = resp.read()

        content = raw.decode(encoding, errors='ignore')

        # Check if it's actually RSS
        is_rss = '<rss' in content or '<feed' in content or '<?xml' in content[:100]
        if not is_rss:
            results[name] = {'status': 'HTML_NOT_RSS', 'size': len(raw), 'ms': int((time.time()-t0)*1000)}
            continue

        items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
        if not items:
            items = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)

        health = []
        for it in items:
            if any(k in it for k in HEALTH_KW):
                t_m = re.search(r'<title>(.*?)</title>', it, re.DOTALL)
                if t_m:
                    health.append(t_m.group(1)[:60])

        elapsed = int((time.time() - t0) * 1000)
        results[name] = {
            'status': 'OK',
            'items': len(items),
            'health': len(health),
            'ms': elapsed,
            'content_type': ct,
            'size': len(raw),
            'sample': health[:3] if health else []
        }

    except Exception as e:
        results[name] = {'status': 'ERROR', 'error': str(e)[:50], 'ms': int((time.time()-t0)*1000)}

print("Source Test Results:")
print("=" * 60)
for name, res in sorted(results.items(), key=lambda x: x[1].get('status','')):
    if res['status'] == 'OK':
        sample_str = ' | '.join(res.get('sample', []))
        print(f"OK   {name}: {res['items']} items, {res['health']} health, {res['ms']}ms")
        if sample_str:
            print(f"     {sample_str}")
    elif res['status'] == 'HTML_NOT_RSS':
        print(f"DEAD {name}: returns HTML ({res['size']} bytes), {res['ms']}ms")
    else:
        print(f"FAIL {name}: {res.get('error', res.get('status'))} ({res['ms']}ms)")