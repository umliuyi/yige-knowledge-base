#!/usr/bin/env python3
"""
RSS定向搜索 - 调研龙虾专用
抓取多个权威来源，返回最新医疗/健康/乐城相关内容
"""
import urllib.request
import urllib.parse
import time
import json
import re
from datetime import datetime, timedelta

FEEDS = {
    "36氪": "https://36kr.com/feed",
    "丁香园": "http://www.dxy.cn/rss/home.xml",
    "动脉网": "https://vcbeat.top/Rss/News",
    "人民日报健康": "https://paper.people.com.cn/rmrbhwb/rss/rss5.xml",
}

# 关键词配置
HEALTH_KEYWORDS = [
    "乐城", "海南", "免疫治疗", "细胞治疗", "干细胞",
    "CAR-T", "ADC", "新药", "审批", "NMPA", "FDA",
    "医疗", "健康险", "特药", "惠民保", "保险",
    "癌症", "肿瘤", "糖尿病", "创新药"
]

def fetch_feed(name, url, timeout=15):
    """抓取单个RSS源"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            return {'name': name, 'ok': True, 'content': content, 'size': len(content)}
    except Exception as e:
        return {'name': name, 'ok': False, 'error': str(e)}

def extract_items(content, max_items=20):
    """从RSS XML中提取条目"""
    items = []
    # 简单XML解析（不用外部库）
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(content)
        # RSS 2.0
        for item in root.findall('.//item'):
            title = _get_text(item, 'title')
            link = _get_text(item, 'link')
            desc = _get_text(item, 'description')
            pub_date = _get_text(item, 'pubDate')
            if title:
                items.append({
                    'title': clean_html(title),
                    'link': link,
                    'desc': clean_html(desc)[:200] if desc else '',
                    'pub_date': pub_date
                })
        # Atom
        for entry in root.findall('.//entry'):
            title = _get_text(entry, 'title')
            link_el = entry.find('link')
            link = link_el.get('href') if link_el is not None else ''
            summary = _get_text(entry, 'summary') or _get_text(entry, 'content')
            updated = _get_text(entry, 'updated') or _get_text(entry, 'published')
            if title:
                items.append({
                    'title': clean_html(title),
                    'link': link,
                    'desc': clean_html(summary)[:200] if summary else '',
                    'pub_date': updated
                })
    except Exception as e:
        pass
    return items[:max_items]

def _get_text(elem, tag):
    found = elem.find(tag)
    return found.text.strip() if found is not None and found.text else ''

def clean_html(text):
    """去除HTML标签"""
    if not text:
        return ''
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&#39;', "'", text)
    text = re.sub(r'&nbsp;', ' ', text)
    return text.strip()

def keyword_match(title, desc, keywords):
    """检查标题或摘要是否包含关键词"""
    text = (title + ' ' + desc).lower()
    for kw in keywords:
        if kw.lower() in text:
            return True
    return False

def search_rss(query=None, days_back=3, max_per_source=10):
    """主搜索函数"""
    cutoff = datetime.now() - timedelta(days=days_back)
    all_items = []

    for name, url in FEEDS.items():
        feed = fetch_feed(name, url)
        if not feed['ok']:
            print(f"[WARN] {name} failed: {feed['error']}")
            continue

        items = extract_items(feed['content'], max_per_source)
        matched = []
        for item in items:
            if query:
                if query.lower() not in item['title'].lower() and query.lower() not in item['desc'].lower():
                    continue
            if keyword_match(item['title'], item['desc'], HEALTH_KEYWORDS):
                matched.append(item)

        print(f"[OK] {name}: found {len(matched)} relevant items")
        all_items.extend(matched)

    # 去重（按标题相似度）
    seen = set()
    unique = []
    for item in all_items:
        key = item['title'][:30]
        if key not in seen:
            seen.add(key)
            unique.append(item)

    # 按日期排序
    unique.sort(key=lambda x: x.get('pub_date', ''), reverse=True)
    return unique

if __name__ == '__main__':
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"RSS搜索 | 查询: {query or '全部健康关键词'} | 来源: {len(FEEDS)}个")
    results = search_rss(query=query)
    print(f"\n共找到 {len(results)} 条相关内容:\n")
    for i, r in enumerate(results[:10], 1):
        print(f"{i}. {r['title'][:60]}")
        print(f"   来源: {r.get('link','')[:80]}")
        if r.get('desc'):
            print(f"   摘要: {r['desc'][:100]}")
        print()
