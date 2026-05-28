# -*- coding: utf-8 -*-
import urllib.request
import re
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# Search terms
queries = [
    ('海外特药', 'site:douyin.com'),
    ('海南乐城 海外新药', 'douyin.com/video'),
    ('博鳌乐城 特药 视频', ''),
    ('乐城 新药械 抖音', ''),
    ('进口新药 海南乐城', ''),
]

found = {}

for kw, site in queries:
    q = urllib.parse.quote(kw)
    if site:
        url = f'https://www.sogou.com/web?query={q}+{urllib.parse.quote(site)}'
    else:
        url = f'https://www.sogou.com/web?query={q}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            html = r.read().decode('utf-8', errors='ignore')
        
        # Extract video IDs from Sogou redirect links (hedJjaC291...)
        redir_pattern = r'hedJjaC291[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-]+'
        redirects = re.findall(redir_pattern, html)
        
        # Also find direct video IDs
        video_patterns = [
            r'douyin\.com/video/([iA-Za-z0-9]{10,20})',
            r'v\.douyin\.com/([A-Za-z0-9]+)',
        ]
        
        for pat in video_patterns:
            for m in re.findall(pat, html):
                if m not in found:
                    found[m] = kw
                    print(f'[{kw}] Direct video: https://www.douyin.com/video/{m}')
        
        for rdr in redirects[:5]:
            if rdr not in found:
                found[rdr] = kw
        
        print(f'[{kw}] Search done, redirects found: {len(redirects)}')
        
    except Exception as e:
        print(f'[{kw}] Error: {e}')

print(f'\nTotal unique: {len(found)}')
