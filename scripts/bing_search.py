import urllib.request, urllib.parse, re, ssl

query = '乐城 干细胞 最新消息 2026'
url = 'https://www.bing.com/search?q=' + urllib.parse.quote(query)
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
})
ctx = ssl.create_default_context()
try:
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        content = r.read().decode('utf-8', errors='ignore')
    # Extract search results
    items = re.findall(r'<li class="b_algo"(.*?)</li>', content, re.DOTALL)
    results = []
    for item in items[:8]:
        title_match = re.search(r'<h2>(.*?)</h2>', item, re.DOTALL)
        snippet_match = re.search(r'<p>(.*?)</p>', item, re.DOTALL)
        if title_match and snippet_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            snippet = re.sub(r'<[^>]+>', '', snippet_match.group(1)).strip()
            if title and snippet:
                results.append(f"标题: {title[:80]}\n摘要: {snippet[:200]}\n")
    for r in results:
        print(r)
    if not results:
        print('No results found, trying alternative...')
        # fallback: simple text extraction
        text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        matches = re.findall(r'博鳌乐城[^。\n]{10,100}', text)
        for m in matches[:5]:
            print(m)
except Exception as e:
    print(f'Error: {e}')