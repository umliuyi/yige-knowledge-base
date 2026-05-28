# -*- coding: utf-8 -*-
import urllib.request
import re
import json
import urllib.parse

keywords = "乐城生物医疗新技术"
query = urllib.parse.quote(keywords)

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/json',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.douyin.com/',
}

# Search for videos
search_url = f"https://www.douyin.com/aweme/v1/web/search/item/?keyword={query}&count=20&offset=0"

try:
    req = urllib.request.Request(search_url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode('utf-8', errors='ignore'))
        print('Status:', r.status)
        print('Keys:', list(data.keys()) if isinstance(data, dict) else type(data))
        if 'item_list' in data:
            print('Videos found:', len(data['item_list']))
            for item in data['item_list'][:10]:
                aweme_id = item.get('aweme_id', '')
                desc = item.get('desc', '')
                statistics = item.get('statistics', {})
                print(f'\n--- Video {aweme_id} ---')
                print(f'Desc: {desc}')
                print(f'Stats: {statistics}')
        else:
            print('Raw data (first 500 chars):', json.dumps(data, ensure_ascii=False)[:500])
except Exception as e:
    print(f'Error: {e}')
