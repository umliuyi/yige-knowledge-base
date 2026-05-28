# -*- coding: utf-8 -*-
import urllib.request
import re
import json
import urllib.parse

# Video IDs we already found from search
video_ids = [
    ('iJS9PbpH', '海南博鳌乐城 关于遴选生物医学新技术转化应用项目公告'),
    ('iBQvdLgW', '博鳌乐城先行区生物医学新技术转化应用第一批实施目录'),
    ('h0gfEAfive4', '生物医学新技术临床研究和临床转化应用管理条例发布'),
    ('6978452995369454888', '海南打细胞新规出炉 乐城先行区生物医学新技术促进规定'),
    ('iPagChtb', '博鳌乐城启动生物医学新项目技术遴选'),
]

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

print("抓取各视频页面数据...")
print("=" * 60)

for vid, title in video_ids:
    url = f'https://www.douyin.com/video/{vid}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
        
        # Extract JSON data embedded in the page
        patterns = [
            r'"digg_count":"(\d+)"',
            r'"comment_count":"(\d+)"',
            r'"share_count":"(\d+)"',
            r'"download_count":"(\d+)"',
            r'"forward_count":"(\d+)"',
            r'"play_count":"(\d+)"',
            r'"aweme_id":"(\d+)"',
            r'"desc":"([^"]{10,200})"',
            r'"author":\{"[^}]*?"nickname":"([^"]+)"',
        ]
        
        data = {}
        for pat in patterns:
            m = re.search(pat, html)
            if m:
                data[pat.split('"')[1]] = m.group(1)
        
        print(f'\n📹 视频: {title}')
        print(f'   链接: https://www.douyin.com/video/{vid}')
        for k, v in data.items():
            print(f'   {k}: {v}')
        
    except Exception as e:
        print(f'\n视频 {vid} 获取失败: {e}')

print('\n' + '=' * 60)
print("分析完成")
