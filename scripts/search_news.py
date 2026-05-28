import urllib.request, urllib.parse, re, sys

query = '干细胞治疗糖尿病 最新新闻 2026'
url = 'https://www.google.com/search?q=' + urllib.parse.quote(query) + '&hl=zh-CN'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
})
try:
    r = urllib.request.urlopen(req, timeout=10)
    html = r.read().decode('utf-8', errors='replace')
except Exception as e:
    print('Fetch error:', e)
    sys.exit(1)

# Remove script and style
html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<[^>]+>', ' ', html)
html = re.sub(r'\s+', ' ', html).strip()
print(html[:8000])