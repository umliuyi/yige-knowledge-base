# -*- coding: utf-8 -*-
import urllib.request, ssl, re, json, sys
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

KEYWORDS = ['乐城', '博鳌', '干细胞', '免疫治疗', 'CAR-T', '基因治疗', '新药械', '特许药械', '临床试验', '慢阻肺', '骨关节炎', '糖尿病', '肿瘤']

def fetch():
    req = urllib.request.Request('https://36kr.com/feed', headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    raw = resp.read().decode('utf-8', errors='ignore')
    
    # Extract titles from CDATA
    titles = re.findall(r'<!\[CDATA\[([^\]]+)]]>', raw)
    # Extract all links
    links = re.findall(r'href="(https?://36kr\.com/p/\d+)"', raw)
    
    # titles[1] corresponds to titles[1] etc (skip first which is channel title)
    # links are interleaved - need to deduplicate
    unique_links = list(dict.fromkeys(links))  # preserve order, remove dupes
    
    results = []
    for title in titles[1:]:
        if not title.strip():
            continue
        for kw in KEYWORDS:
            if kw in title:
                results.append(title.strip())
                break
    
    return results

def fetch_linked():
    req = urllib.request.Request('https://36kr.com/feed', headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    raw = resp.read().decode('utf-8', errors='ignore')
    
    # Extract all links
    links = re.findall(r'href="(https?://36kr\.com/p/\d+)', raw)
    unique_links = list(dict.fromkeys(links))
    
    results = []
    for title in re.findall(r'<!\[CDATA\[([^\]]+)]]>', raw):
        t = title.strip()
        if not t:
            continue
        for kw in KEYWORDS:
            if kw in t:
                results.append({'title': t, 'link': ''})
                break
    
    # Pair with links (approximate)
    for i, r in enumerate(results):
        if i < len(unique_links):
            r['link'] = unique_links[i]
    
    return results

if __name__ == '__main__':
    items = fetch_linked()
    print(f'[{datetime.now().strftime("%H:%M")}] Found {len(items)} items')
    for it in items[:5]:
        print(it['title'][:50])
        print(' ', it['link'])
    # Save
    outpath = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206\36kr_daily.json'
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump({'date': datetime.now().strftime('%Y-%m-%d'), 'items': items}, f, ensure_ascii=False, indent=2)
    print(f'Saved to {outpath}')
