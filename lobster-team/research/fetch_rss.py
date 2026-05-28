import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

RSS_SOURCES = {
    '36kr科技': 'https://36kr.com/feed',
    '丁香园': 'http://www.dxy.cn/rss/home.xml',
    '动脉网': 'https://vcbeat.top/Rss/News',
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

all_items = []

for name, url in RSS_SOURCES.items():
    print(f'=== Fetching {name} ===')
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        print(f'  Status: {resp.status_code}, Length: {len(resp.text)}')
        text = resp.text
        
        root = ET.fromstring(text.encode('utf-8') if isinstance(text, str) else text)
        
        # Try RSS format
        items = root.findall('.//item')
        if not items:
            items = root.findall('.//entry')
        
        print(f'  Items found: {len(items)}')
        
        for item in items[:20]:
            title_el = item.find('title')
            title = title_el.text if title_el is not None else ''
            
            link = ''
            for child in item:
                if child.tag in ('link', 'guid') and child.text:
                    link = child.text
            
            desc = item.find('description') or item.find('summary') or item.find('content')
            desc_text = ''
            if desc is not None and desc.text:
                # Strip HTML
                import re
                desc_text = re.sub(r'<[^>]+>', '', desc.text)[:200]
            
            pub = ''
            pub_el = item.find('pubDate') or item.find('published') or item.find('updated')
            if pub_el is not None and pub_el.text:
                pub = pub_el.text[:35]
            
            print(f'  [{name}] {title.strip()[:80]}')
            
            all_items.append({
                'source': name,
                'title': title.strip(),
                'link': link,
                'desc': desc_text,
                'pub': pub,
                'url': url
            })
    except Exception as e:
        print(f'  ERROR: {e}')
    print()

print('\n\n=== ALL ITEMS COUNT:', len(all_items), '===\n')

# Keywords for lecheng and health tech
keywords = [
    '乐城', '博鳌', 'NMPA', 'FDA', 'CAR-T', '免疫治疗', '基因编辑', '干细胞',
    '细胞治疗', 'AI医疗', '创新药', '新药审批', '医疗器械', '海南', '自贸港',
    '惠民保', '特药险', '权益卡', '再生医学', ' CRISPR', 'TIL', 'TCR-T', 'NK细胞',
    '抗体', 'ADC', '双抗', 'mRNA', '肿瘤', '癌症', '精准医疗'
]

print('\n=== FILTERED ITEMS ===')
for item in all_items:
    text = (item['title'] + ' ' + item['desc']).lower()
    matched = [kw for kw in keywords if kw.lower() in text]
    if matched:
        print(f"[{item['source']}] {item['title'][:80]}")
        print(f"  Desc: {item['desc'][:100]}")
        print(f"  Matched: {matched}")
        print(f"  Link: {item['link']}")
        print()

# Save to file
import json
with open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\lobster-team\research\rss_fetch.json', 'w', encoding='utf-8') as f:
    json.dump(all_items, f, ensure_ascii=False, indent=2)
print('Saved to rss_fetch.json')