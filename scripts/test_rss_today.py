import urllib.request
import urllib.error
import re
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import html

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

sources = {
    '36kr': 'https://36kr.com/feed',
    '丁香园': 'http://www.dxy.cn/rss/home.xml',
    '动脉网': 'https://vcbeat.top/Rss/News',
}

def extract_text(elem):
    texts = []
    if elem.text:
        texts.append(elem.text)
    for child in elem:
        texts.append(extract_text(child))
        if child.tail:
            texts.append(child.tail)
    return ''.join(texts)

def parse_rss_content(content, source_name):
    items = []
    try:
        root = ET.fromstring(content.encode('utf-8') if isinstance(content, str) else content)
        channel = root.find('channel')
        if channel is not None:
            for item in channel.findall('item'):
                title = extract_text(item.find('title')) if item.find('title') is not None else ''
                description = extract_text(item.find('description')) if item.find('description') is not None else ''
                pub_date = extract_text(item.find('pubDate')) if item.find('pubDate') is not None else ''
                link = extract_text(item.find('link')) if item.find('link') is not None else ''
                if title or description:
                    items.append({
                        'title': title.strip(),
                        'description': description.strip()[:500],
                        'pubDate': pub_date.strip(),
                        'link': link.strip(),
                        'source': source_name
                    })
    except Exception as e:
        print(f'  Parse error: {e}')
    return items

# Test 36kr only
name = '36kr'
url = sources[name]
try:
    print(f'Fetching {name}... ', end='', flush=True)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        content = response.read().decode('utf-8', errors='replace')
    print(f'OK - {len(content)} bytes')
    
    items = parse_rss_content(content, name)
    print(f'Total items: {len(items)}\n')
    
    # Print all titles
    for i, item in enumerate(items):
        print(f'{i+1}. [{item["source"]}] {item["title"]}')
        if item['description']:
            print(f'   DESC: {item["description"][:150]}...')
        print()
    
except Exception as e:
    print(f'ERROR: {e}')
