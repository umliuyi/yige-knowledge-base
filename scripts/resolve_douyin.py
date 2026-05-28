# -*- coding: utf-8 -*-
import urllib.request
import re
import urllib.parse

keywords = "乐城生物医疗新技术"
query = urllib.parse.quote(keywords)

# Try multiple sources
sources = [
    f"https://www.sogou.com/web?query={query}+site%3Av.douyin.com",
    f"https://www.sogou.com/web?query={query}+douyin.com%2Fvideo",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

found = set()

for url in sources:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            html = r.read().decode('utf-8', errors='ignore')
        
        # Extract video IDs from various patterns
        patterns = [
            r'douyin\.com/video/(\d+)',
            r'v\.douyin\.com/(\w+)',
            r'www\.douyin\.com/aweme/v\d+/\?*.*?video_id=(\w+)',
            r'"video_id":"(\w+)"',
            r'"aweme_id":"(\d+)"',
        ]
        for pat in patterns:
            for m in re.findall(pat, html):
                if len(m) > 5:
                    if m not in found:
                        found.add(m)
                        print(f'FOUND: {m}')
    except Exception as e:
        print(f'Error ({url[:60]}): {e}')

print(f'\nTotal unique video IDs found: {len(found)}')
for vid in found:
    # Try to construct the web URL
    print(f'https://www.douyin.com/video/{vid}')
