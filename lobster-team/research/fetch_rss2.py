import requests
import re
import json
import xml.etree.ElementTree as ET
from datetime import datetime

# Try multiple parsing approaches
def parse_rss_xml(text):
    # Try standard RSS
    try:
        root = ET.fromstring(text.encode('utf-8'))
        items = root.findall('.//item')
        if items:
            return items, 'rss'
    except:
        pass
    
    # Try Atom
    try:
        root = ET.fromstring(text.encode('utf-8'))
        items = root.findall('.//entry')
        if items:
            return items, 'atom'
    except:
        pass
    
    # Try parsing with regex as fallback
    items = re.findall(r'<item>(.*?)</item>', text, re.DOTALL)
    if items:
        return items, 'rss-regex'
    
    items = re.findall(r'<entry>(.*?)</entry>', text, re.DOTALL)
    if items:
        return items, 'atom-regex'
    
    return [], 'none'

def extract_text(elem, tag):
    el = elem.find(tag)
    return el.text if el is not None and el.text else ''

def strip_html(text):
    if not text:
        return ''
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

RSS_SOURCES = {
    '36kr科技': 'https://36kr.com/feed',
    '丁香园': 'http://www.dxy.cn/rbs/home.xml',  # Try alternative path
    '动脉网': 'https://vcbeat.top/Rss/News',
    '健康界': 'https://www.cn-healthcare.com/rss/',
    '第一财经': 'https://www.yicai.com/rss/news.xml',
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

all_items = []

for name, url in RSS_SOURCES.items():
    print(f'\n=== {name} ===')
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        print(f'Status: {resp.status_code}, Len: {len(resp.text)}')
        
        # Try different encodings
        for enc in ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']:
            try:
                text = resp.content.decode(enc, errors='replace')
                break
            except:
                text = resp.text
        
        items, ptype = parse_rss_xml(text)
        print(f'Parse type: {ptype}, Items: {len(items)}')
        
        for item in items[:20]:
            if ptype in ('rss', 'rss-regex') and isinstance(item, str):
                # Regex extracted item
                title = re.search(r'<title[^>]*>(.*?)</title>', item, re.DOTALL)
                title = strip_html(title.group(1)) if title else ''
                link = re.search(r'<link[^>]*>(.*?)</link>', item, re.DOTALL)
                link = link.group(1).strip() if link else ''
                desc = re.search(r'<description[^>]*>(.*?)</description>', item, re.DOTALL)
                desc = strip_html(desc.group(1)[:300]) if desc else ''
            else:
                title = extract_text(item, 'title')
                link = ''
                for child in item:
                    if child.tag in ('link', 'guid') and child.text:
                        link = child.text
                desc = strip_html((extract_text(item, 'description') or extract_text(item, 'summary') or extract_text(item, 'content'))[:300])
            
            print(f'  TITLE: {title[:80]}')
            
            all_items.append({
                'source': name,
                'title': title,
                'link': link,
                'desc': desc,
                'url': url
            })
            
    except Exception as e:
        print(f'ERROR: {e}')

print(f'\n\nTotal items: {len(all_items)}')

# Filter by keywords
keywords = [
    '乐城', '博鳌', 'NMPA', 'FDA', 'CAR-T', '免疫治疗', '基因编辑', '干细胞',
    '细胞治疗', 'AI医疗', '创新药', '新药审批', '医疗器械', '海南', '自贸港',
    '惠民保', '特药险', '权益卡', '再生医学', 'CRISPR', 'TIL', 'TCR-T', 'NK细胞',
    '抗体', 'ADC', '双抗', 'mRNA', '肿瘤', '癌症', '精准医疗', '特药', '生物制药'
]

print('\n=== MATCHED ITEMS ===')
for item in all_items:
    text = (item['title'] + ' ' + item['desc']).lower()
    matched = [kw for kw in keywords if kw.lower() in text]
    if matched:
        print(f"[{item['source']}] {item['title'][:80]}")
        print(f"  Desc: {item['desc'][:120]}")
        print(f"  Matched: {matched}")
        print(f"  Link: {item['link'][:80]}")
        print()

# Save
with open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\lobster-team\research\rss_fetch.json', 'w', encoding='utf-8') as f:
    json.dump(all_items, f, ensure_ascii=False, indent=2)
print('Saved rss_fetch.json')