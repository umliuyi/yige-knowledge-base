# -*- coding: utf-8 -*-
import urllib.request
import re
import urllib.parse

keywords = "海外特药"
query = urllib.parse.quote(keywords)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# Use Sogou to search for Douyin overseas drug videos
sources = [
    f"https://www.sogou.com/web?query={query}+site%3Adouyin.com",
    f"https://www.sogou.com/web?query={query}+海南+乐城+抖音",
    f"https://www.sogou.com/web?query=海外特药+博鳌+乐城+视频",
]

found = {}

for url in sources:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            html = r.read().decode('utf-8', errors='ignore')
        
        # Extract video IDs
        patterns = [
            (r'douyin\.com/video/([iA-Za-z0-9]{10,20})', 'video'),
            (r'v\.douyin\.com/([iA-Za-z0-9]+)', 'v_douyin'),
            (r'"aweme_id":"(\d+)"', 'aweme_id'),
        ]
        
        for pat, src in patterns:
            for m in re.findall(pat, html):
                if m not in found:
                    found[m] = src
                    print(f'FOUND [{src}]: {m}')
    except Exception as e:
        print(f'Error: {e}')

print(f'\nTotal unique: {len(found)}')
for vid, src in found.items():
    print(f'https://www.douyin.com/video/{vid}')
