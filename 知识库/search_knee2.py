# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, re, json, sys

# Force UTF-8 stdout
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def search_bing(query, count=5):
    q = urllib.parse.quote(query)
    url = f'https://cn.bing.com/search?q={q}&count={count}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    })
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode('utf-8', errors='ignore')
    
    pattern = r'<li class="b_algo"[^>]*>.*?<h2[^>]*><a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a></h2>.*?<p[^>]*>(.*?)</p>'
    matches = re.findall(pattern, html, re.DOTALL)
    results = []
    for url, title, desc in matches[:count]:
        title_clean = re.sub(r'<[^>]+>', '', title).strip()
        desc_clean = re.sub(r'<[^>]+>', '', desc).strip()
        results.append({'url': url, 'title': title_clean, 'desc': desc_clean})
    return results

queries = [
    ('膝关节干细胞 乐城', 5),
    ('CartiLife 膝关节 软骨', 5),
    ('膝关节干细胞 临床数据 骨关节炎', 5),
    ('膝关节软骨损伤 传统治疗 关节置换', 5),
]

all_results = []
for query, count in queries:
    print(f'=== {query} ===')
    try:
        results = search_bing(query, count)
        for r in results:
            print(f"Title: {r['title']}")
            print(f"URL: {r['url']}")
            desc_preview = r['desc'][:300] if r['desc'] else ''
            print(f"Desc: {desc_preview}")
            print()
            all_results.append({'query': query, **r})
    except Exception as e:
        print(f'Error: {e}')
        print()

with open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\知识库\bing_raw_results.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)
print(f'Saved {len(all_results)} results')