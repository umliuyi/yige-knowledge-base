# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def search_bing(query, count=5):
    q = urllib.parse.quote(query)
    url = 'https://cn.bing.com/search?q=' + q + '&count=' + str(count)
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    })
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode('utf-8', errors='ignore')
    pattern = r'<li class="b_algo"[^>]*>.*?<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a></h2>(.*?)</li>'
    matches = re.findall(pattern, html, re.DOTALL)
    results = []
    for url, title, rest in matches[:count]:
        title_clean = re.sub(r'<[^>]+>', '', title).strip()
        desc_match = re.search(r'<p[^>]*>(.*?)</p>', rest, re.DOTALL)
        desc_clean = ''
        if desc_match:
            desc_clean = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()
        results.append({'url': url, 'title': title_clean, 'desc': desc_clean})
    return results

queries = [
    ('海南帝诺医院 膝骨关节炎 干细胞', 5),
    ('博鳌超级医院 OM-021001 半月板 细胞', 5),
    ('knee replacement surgery cost recovery time risk comparison', 5),
    ('autologous chondrocyte implantation vs knee replacement comparison outcome', 5),
]

all_results = []
for query, count in queries:
    print('=== ' + query + ' ===')
    try:
        results = search_bing(query, count)
        for r in results:
            print('Title: ' + r['title'])
            print('URL: ' + r['url'])
            print('Desc: ' + r['desc'][:200])
            print()
            all_results.append({'query': query, 'title': r['title'], 'url': r['url'], 'desc': r['desc']})
    except Exception as e:
        print('Error: ' + str(e))
    print()

import json
with open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\知识库\bing_raw4.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)
print('Saved ' + str(len(all_results)) + ' results')