# -*- coding: utf-8 -*-
import urllib.request
import re
import json
import html

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '',
}

# Try to get video details via Douyin open API
video_ids = [
    '7499636021861420328',
    '7289360014743997711', 
    '7298519286220377378',
    '7078854159738473759',
]

print("通过抖音开放API获取视频信息...")
print("=" * 60)

for vid in video_ids:
    # Try the aweme detail API
    url = f'https://www.iesdouyin.com/aweme/v1/web/aweme/detail/?aweme_id={vid}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8', errors='ignore'))
        
        aweme = data.get('aweme_detail', {})
        if aweme:
            desc = aweme.get('desc', '')
            stats = aweme.get('statistics', {})
            author = aweme.get('author', {})
            nickname = author.get('nickname', '')
            print(f'\n📹 视频ID: {vid}')
            print(f'   描述: {desc}')
            print(f'   作者: {nickname}')
            print(f'   点赞: {stats.get("digg_count", "N/A")}')
            print(f'   评论: {stats.get("comment_count", "N/A")}')
            print(f'   分享: {stats.get("share_count", "N/A")}')
            print(f'   播放: {stats.get("play_count", "N/A")}')
        else:
            print(f'\n视频 {vid}: 无详细数据')
    except Exception as e:
        print(f'\n视频 {vid} API错误: {e}')

print('\n' + '=' * 60)

# Now try to search for more 海外特药 + 乐城 videos via Toutiao API
print("\n通过今日头条搜索海外特药+乐城视频...")
toutiao_search = 'https://www.toutiao.com/api/search/v/?keyword=%E6%B5%B7%E5%A4%96%E7%89%B9%E8%8D%AF+%E4%B9%90%E5%9F%8E&count=20&source=input'
try:
    req = urllib.request.Request(toutiao_search, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode('utf-8', errors='ignore'))
    print('Toutiao response keys:', list(data.keys())[:10] if isinstance(data, dict) else type(data))
except Exception as e:
    print(f'Toutiao搜索错误: {e}')
