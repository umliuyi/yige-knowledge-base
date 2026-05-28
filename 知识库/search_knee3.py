# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, re, json, io
import sys
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
    # Pattern: find result blocks
    pattern = r'<li class="b_algo"[^>]*>.*?<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a></h2>(.*?)</li>'
    matches = re.findall(pattern, html, re.DOTALL)
    results = []
    for url, title, rest in matches[:count]:
        title_clean = re.sub(r'<[^>]+>', '', title).strip()
        # Extract description from the rest
        desc_match = re.search(r'<p[^>]*>(.*?)</p>', rest, re.DOTALL)
        desc_clean = ''
        if desc_match:
            desc_clean = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()
        results.append({'url': url, 'title': title_clean, 'desc': desc_clean})
    return results

queries = [
    ('乐城 脐带间充质干细胞 膝骨关节炎 帝诺医院', 5),
    ('OM-021001 细胞治疗 膝关节 半月板 博鳌超级医院', 5),
    ('膝关节置换手术 费用 恢复期 风险', 5),
    ('膝关节干细胞治疗 骨关节炎 临床试验 数据', 5),
]

all_results = []
for query, count in queries:
    print(f'=== {query} ===')
    try:
        results = search_bing(query, count)
        for r in results:
            print(f"Title: {r['title']}")
            print(f"URL: {r['url']}")
            print(f"Desc: {r['desc'][:300]}")
            print()
            all_results.append({'query': query, **r})
    except Exception as e:
        print(f'Error: {e}')

with open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\知识库\bing_raw2.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)
print(f'Saved {len(all_results)} results')