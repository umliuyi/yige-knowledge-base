# -*- coding: utf-8 -*-
import urllib.request
import re

url = 'https://www.bing.com/search?q=%E4%B9%90%E5%9F%8E%E7%94%9F%E7%89%A9%E5%8C%BB%E8%82%A3%E6%96%B0%E6%8A%80%E6%9C%AF'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode('utf-8', errors='ignore')
    pattern = r'douyin\.com/video/\d+'
    urls = re.findall(pattern, html)
    unique = sorted(set(urls))
    print('Found:', len(unique))
    for u in unique[:20]:
        print('https://' + u)
except Exception as e:
    print('Error:', e)
