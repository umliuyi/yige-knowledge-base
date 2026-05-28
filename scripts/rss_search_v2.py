#!/usr/bin/env python3
"""RSS搜索 v2 - 调研龙虾专用，支持CDATA和编码检测"""
import urllib.request
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime

FEEDS = {
    "36氪": "https://36kr.com/feed",
    "丁香园": "http://www.dxy.cn/rss/home.xml",
    "动脉网": "https://vcbeat.top/Rss/News",
}

HEALTH_KW = [
    "乐城", "海南", "免疫治疗", "细胞治疗", "干细胞",
    "CAR-T", "ADC", "新药", "NMPA", "FDA",
    "医疗", "健康险", "特药", "惠民保", "保险",
    "癌症", "肿瘤", "糖尿病", "创新药", "生物医学"
]

def get_encoding(resp):
    content_type = resp.headers.get('Content-Type', '')
    if 'gb2312' in content_type or 'gbk' in content_type:
        return 'gbk'
    return 'utf-8'

def decode_content(content, encoding_hint=None):
    for enc in [encoding_hint, 'utf-8', 'gbk', 'gb2312']:
        try:
            return content.decode(enc, errors='strict')
        except:
            try:
                return content.decode(enc, errors='ignore')
            except:
                continue
    return content.decode('utf-8', errors='ignore')

def extract_cdata(text):
    """提取CDATA内容"""
    if not text:
        return ''
    matches = re.findall(r'<!\[CDATA\[(.*?)\]\]>', text, re.DOTALL)
    if matches:
        return matches[0]
    # 普通文本
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def fetch_and_parse(url, name):
    """抓取并解析RSS"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            enc = get_encoding(resp)
            raw = resp.read()
            content = decode_content(raw, enc)
            items = parse_rss(content)
            return {'ok': True, 'items': items, 'name': name, 'size': len(raw)}
    except Exception as e:
        return {'ok': False, 'error': str(e), 'name': name}

def parse_rss(content):
    """解析RSS/Atom XML"""
    items = []
    try:
        root = ET.fromstring(content)
        # RSS 2.0
        for item in root.findall('.//item'):
            title = extract_cdata(_text(item, 'title'))
            link = extract_cdata(_text(item, 'link'))
            desc = extract_cdata(_text(item, 'description') or _text(item, 'summary') or '')
            pub = _text(item, 'pubDate') or _text(item, 'published') or ''
            if title:
                items.append({'title': title, 'link': link, 'desc': desc[:200], 'pub': pub})
        # Atom
        for entry in root.findall('.//entry'):
            title = extract_cdata(_text(entry, 'title'))
            link_el = entry.find('link')
            link = link_el.get('href') if link_el is not None else ''
            summary = extract_cdata(_text(entry, 'summary') or _text(entry, 'content') or '')
            updated = _text(entry, 'updated') or _text(entry, 'published') or ''
            if title:
                items.append({'title': title, 'link': link, 'desc': summary[:200], 'pub': updated})
    except Exception as e:
        pass
    return items

def _text(elem, tag):
    found = elem.find(tag)
    return found.text if found is not None and found.text else ''

def is_health_related(title, desc):
    text = (title + ' ' + desc).lower()
    return any(kw.lower() in text for kw in HEALTH_KW)

def search(query=None, days_back=3):
    """主搜索"""
    all_items = []
    for name, url in FEEDS.items():
        print(f"Fetching {name}...", end=' ')
        result = fetch_and_parse(url, name)
        if result['ok']:
            matched = [it for it in result['items']]
            health = [it for it in matched if is_health_related(it['title'], it['desc'])]
            print(f"OK - {len(result['items'])} items, {len(health)} health-related")
            all_items.extend(health)
        else:
            print(f"FAIL: {result.get('error', 'unknown')}")
    # 去重
    seen = set()
    unique = []
    for it in all_items:
        key = it['title'][:30]
        if key not in seen:
            seen.add(key)
            unique.append(it)
    print(f"\nTotal: {len(unique)} health-related items")
    return unique

if __name__ == '__main__':
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else None
    results = search(query=query)
    for i, r in enumerate(results[:10], 1):
        print(f"\n{i}. {r['title'][:70]}")
        print(f"   {r.get('link','')[:80]}")
        if r.get('desc'):
            print(f"   {r['desc'][:100]}")
