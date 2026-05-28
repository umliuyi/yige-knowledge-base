# -*- coding: utf-8 -*-
import urllib.request
import re
import urllib.parse
import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# Videos found so far
video_data = {
    '7499636021861420328': '海外特药',
    '7289360014743997711': '海南乐城海外新药',
    '7298519286220377378': '海南乐城海外新药',
    '7078854159738473759': '博鳌乐城特药',
}

print("获取各视频页面标题...")
print("=" * 60)

for vid, keyword in video_data.items():
    url = f'https://www.douyin.com/video/{vid}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html_content = r.read().decode('utf-8', errors='ignore')
        
        # Extract title/description
        title_patterns = [
            r'<title>([^<]+)</title>',
            r'"description":"([^"]{10,300})"',
            r'"desc":"([^"]{10,300})"',
            r'<meta name="description" content="([^"]{10,300})"',
        ]
        
        title = ''
        for pat in title_patterns:
            m = re.search(pat, html_content)
            if m:
                title = html.unescape(m.group(1))[:200]
                break
        
        # Extract stats if available
        stats = {}
        stat_patterns = {
            '点赞': r'"digg_count":(\d+)',
            '评论': r'"comment_count":(\d+)',
            '分享': r'"share_count":(\d+)',
            '播放': r'"play_count":(\d+)',
        }
        for stat_name, stat_pat in stat_patterns.items():
            m = re.search(stat_pat, html_content)
            if m:
                stats[stat_name] = m.group(1)
        
        print(f'\n📹 视频ID: {vid}')
        print(f'   关键词: {keyword}')
        print(f'   标题: {title}')
        print(f'   数据: {stats}')
        print(f'   链接: https://www.douyin.com/video/{vid}')
        
    except Exception as e:
        print(f'\n视频 {vid} 出错: {e}')

print('\n' + '=' * 60)

# Also search for more video content via Sogou
print("\n抓取搜狗搜索结果中的海外特药视频...")
search_queries = [
    '海南乐城 海外特药 抖音',
    '博鳌乐城 进口新药 视频',
    '乐城 新药械 临床 抖音',
]

for q in search_queries:
    url = f'https://www.sogou.com/web?query={urllib.parse.quote(q)}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            html_content = r.read().decode('utf-8', errors='ignore')
        
        # Find video links and titles
        # Pattern: title text near douyin.com links
        items = re.findall(r'<h3[^>]*>(.*?)</h3>.*?(douyin\.com/video/\w+)', html_content, re.DOTALL)
        for title_html, link in items[:3]:
            # Clean HTML tags
            clean_title = re.sub(r'<[^>]+>', '', title_html)
            clean_title = html.unescape(clean_title).strip()
            if clean_title and len(clean_title) > 5:
                vid_match = re.search(r'douyin\.com/video/(\w+)', link)
                if vid_match:
                    vid = vid_match.group(1)
                    print(f'\n📹 {clean_title}')
                    print(f'   https://www.douyin.com/video/{vid}')
    except Exception as e:
        print(f'搜索"{q}"出错: {e}')
