import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/rss+xml, application/xml, text/xml, application/xhtml+xml, text/html, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

urls = {
    '丁香园': 'http://www.dxy.cn/rss/home.xml',
    '丁香园https': 'https://www.dxy.cn/rss/home.xml',
    '动脉网': 'https://vcbeat.top/Rss/News',
    '健康界': 'https://www.cn-healthcare.com/rss/',
}

for name, url in urls.items():
    print(f'\n=== {name}: {url} ===')
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        print(f'Status: {resp.status_code}')
        print(f'Content-Type: {resp.headers.get("Content-Type", "unknown")}')
        content = resp.text[:500]
        print(f'Content preview: {content}')
    except Exception as e:
        print(f'Error: {e}')
