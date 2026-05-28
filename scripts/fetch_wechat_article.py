import urllib.request, ssl, re, json, html as html_module
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://mp.weixin.qq.com/s/eBcYknrk9WJNtuO52ID9Sw'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://mp.weixin.qq.com/'
})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw_bytes = resp.read()

raw_utf8 = raw_bytes.decode('utf-8', errors='ignore')
raw_gbk = raw_bytes.decode('gbk', errors='ignore')
utf8_c = len(re.findall(r'[\u4e00-\u9fff]', raw_utf8))
gbk_c = len(re.findall(r'[\u4e00-\u9fff]', raw_gbk))
raw = raw_utf8 if utf8_c > gbk_c else raw_gbk
print(f'Using: {"UTF-8" if utf8_c > gbk_c else "GBK"} ({utf8_c} vs {gbk_c} CJK chars)')

# OG meta from UTF-8
og_t = re.search(r'<meta property="og:title" content="([^"]+)"', raw_utf8)
og_d = re.search(r'<meta property="og:description" content="([^"]+)"', raw_utf8)
og_i = re.search(r'<meta property="og:image" content="([^"]+)"', raw_utf8)
title = html_module.unescape(og_t.group(1)) if og_t else ''
desc = html_module.unescape(og_d.group(1)) if og_d else ''
img = og_i.group(1) if og_i else ''
print('Title:', title)
print('Desc:', desc[:80] if desc else 'N/A')

# Paragraphs
texts = re.findall(r'<(?:p|span)[^>]*>(.*?)</(?:p|span)>', raw, re.DOTALL)
clean = []
for t in texts:
    txt = re.sub(r'<[^>]+>', '', t).strip()
    if len(txt) >= 10 and re.search(r'[\u4e00-\u9fff]', txt):
        txt = html_module.unescape(txt)
        clean.append(txt)

full = '\n'.join(clean)
print(f'Paragraphs: {len(clean)}, chars: {len(full)}')
print()
for p in clean[:8]:
    print(p)
print('...')
for p in clean[-3:]:
    print(p)

# Save
out_raw = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_raw_0527.txt'
out_json = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_struct_0527.json'
with open(out_raw, 'w', encoding='utf-8') as f:
    f.write(f'Title: {title}\nURL: {url}\nDate: {datetime.now().strftime("%Y-%m-%d")}\n\n{full}')
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({'title': title, 'desc': desc, 'url': url, 'img': img, 'date': datetime.now().strftime('%Y-%m-%d'), 'paragraphs': clean}, f, ensure_ascii=False, indent=2)
print('Saved to', out_raw)
