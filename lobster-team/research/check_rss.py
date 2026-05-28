import json
with open('lobster-team/research/daily/2026-05-20-rss-raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
items = data['recent']
print(f'Total: {len(items)}')
for it in items:
    kw = it.get('matched_kw', '')
    print(f'Source: {it["source"]}')
    print(f'Title: {it["title"]}')
    print(f'Match: {kw}')
    print(f'Link: {it["link"]}')
    print()
