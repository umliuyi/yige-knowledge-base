import urllib.request, ssl, re, json
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

KEYWORDS = ['乐城', '博鳌', '干细胞', '免疫治疗', 'CAR-T', '基因治疗', '新药械', '特许药械', '临床试验', '慢阻肺', '骨关节', '糖尿病', '肿瘤']

req = urllib.request.Request('https://36kr.com/feed', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw = resp.read().decode('utf-8', errors='ignore')

cdata_links = re.findall(r'<!\[CDATA\[(https?://[^\]]+)\]\]>', raw)
article_links = [l for l in cdata_links if '/p/' in l]

titles_raw = re.findall(r'<title><!\[CDATA\[([^\]]+)\]\]></title>', raw)
titles = [t.strip() for t in titles_raw[1:] if t.strip()]

pubdates = re.findall(r'<pubDate>([^<]+)', raw)

results = []
for i, title in enumerate(titles):
    for kw in KEYWORDS:
        if kw in title:
            link = article_links[i] if i < len(article_links) else ''
            pd = pubdates[i] if i < len(pubdates) else ''
            results.append({'title': title, 'link': link, 'pubdate': pd, 'keyword': kw})
            break

print('[{}] 36kr: {} matching'.format(datetime.now().strftime('%H:%M'), len(results)))
for r in results[:5]:
    print(r['title'][:50])
    print(' ', r['link'])

out = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206\36kr_daily.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump({'date': datetime.now().strftime('%Y-%m-%d'), 'source': '36kr', 'items': results}, f, ensure_ascii=False, indent=2)
print('Saved')
