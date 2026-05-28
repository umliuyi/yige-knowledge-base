import requests
import re
import json
from datetime import datetime
import time

# More health/medical RSS sources to test
TEST_URLS = {
    '医学界': 'https://www.yixuej.com/rss/',
    '生物谷': 'http://www.bioon.com/rss/rss.aspx',
    '药明康德': 'https://www.wuxiapptec.com/feed/',
    '医药观察家': 'https://www.yyjgb.com/feed/',
    '凤凰健康': 'https://health.ifeng.com/rss/',
    '腾讯健康': 'https://health.qq.com/rss/',
    '新浪健康': 'https://health.sina.com.cn/rss/',
    '网易健康': 'https://jiankang.163.com/rss/',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/rss+xml, application/xml, text/xml, */*',
}

def fetch(url, timeout=10):
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        return r.status_code, r.text[:300]
    except Exception as e:
        return None, str(e)

for name, url in TEST_URLS.items():
    code, content = fetch(url)
    print(f'{name}: status={code}')
    if content:
        print(f'  Preview: {content[:200]}')
    print()
    time.sleep(0.3)