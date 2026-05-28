# -*- coding: utf-8 -*-
import urllib.request, ssl, re, json
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

KEYWORDS = ['乐城', '博鳌', '干细胞', '免疫治疗', 'CAR-T', '基因治疗', '新药械', '特许药械', '临床试验', '慢阻肺', '骨关节炎', '糖尿病', '肿瘤']

req = urllib.request.Request('https://36kr.com/feed', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw = resp.read().decode('utf-8', errors='ignore')

# Get all titles from CDATA
titles_raw = re.findall(r'<!\[CDATA\[([^\]]+)\]\]>', raw)
# Get all links
links_raw = re.findall(r'href="(https?://[^\"]+)"', raw)
# Deduplicate while preserving order
seen = set()
unique_links = []
for l in links_raw:
    if l not in seen:
        seen.add(l)
        unique_links.append(l)

# Filter titles by keywords
items = []
for i, t in enumerate(titles_raw[1:], 1):  # skip channel title
    t = t.strip()
    if not t:
        continue
    for kw in KEYWORDS:
        if kw in t:
            link = unique_links[i] if i < len(unique_links) else ''
            items.append({'title': t, 'link': link, 'kw': kw})
            break

print(f'[{datetime.now().strftime("%H:%M")}] Found {len(items)} items')
for it in items[:5]:
    print(it['title'][:50], '|', it['link'][:60])
for it in items[:5]:
    print(it['title'][:50])
    print(' ', it['link'])

# Save
out = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206\36kr_daily.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump({'date': datetime.now().strftime('%Y-%m-%d'), 'items': items}, f, ensure_ascii=False, indent=2)
print('Saved to', out)
