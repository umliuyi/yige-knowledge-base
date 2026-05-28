import urllib.request
import time

FEEDS = {
    "36kr": "https://36kr.com/feed",
    "丁香园": "http://www.dxy.cn/rss/home.xml",
    "动脉网": "https://vcbeat.top/Rss/News",
}

results = {}
for name, url in FEEDS.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        start = time.time()
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read()
            elapsed = int((time.time() - start) * 1000)
            results[name] = f"OK ({elapsed}ms, {len(content)} bytes)"
    except Exception as e:
        results[name] = f"FAIL: {e}"

for name, status in results.items():
    print(f"{name}: {status}")
