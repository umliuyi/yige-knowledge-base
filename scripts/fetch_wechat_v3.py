import urllib.request, ssl, re, json
from datetime import datetime
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://mp.weixin.qq.com/s/S5p6ssSQfGLRenxeGCmPuw'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://mp.weixin.qq.com/'
})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw_bytes = resp.read()

# Try UTF-8 then GBK
raw_utf8 = raw_bytes.decode('utf-8', errors='ignore')
raw_gbk = raw_bytes.decode('gbk', errors='ignore')
utf8_c = len(re.findall(r'[\u4e00-\u9fff]', raw_utf8))
gbk_c = len(re.findall(r'[\u4e00-\u9fff]', raw_gbk))
print('UTF-8 Chinese:', utf8_c, '| GBK Chinese:', gbk_c)
raw = raw_utf8 if utf8_c > gbk_c else raw_gbk
winner = 'UTF-8' if utf8_c > gbk_c else 'GBK'
print('Winner:', winner)

# Extract OG from the winner, check both
for enc_raw in [raw_utf8, raw_gbk]:
    og_t = re.search(r'<meta property="og:title" content="([^"]+)"', enc_raw)
    if og_t and re.search(r'[\u4e00-\u9fff]', og_t.group(1)):
        title = og_t.group(1)
        desc_raw = enc_raw
        print('OG title encoding:', 'UTF-8' if enc_raw == raw_utf8 else 'GBK')
        break
og_d = re.search(r'<meta property="og:description" content="([^"]+)"', desc_raw)
og_i = re.search(r'<meta property="og:image" content="([^"]+)"', desc_raw)
title = og_t.group(1) if og_t else title
desc = og_d.group(1) if og_d else ''
img = og_i.group(1) if og_i else ''
print('Title:', title[:60])
print('Desc:', desc[:60])

# Extract paragraphs from winner
texts = re.findall(r'<(?:p|span)[^>]*>(.*?)</(?:p|span)>', raw, re.DOTALL)
clean = []
for t in texts:
    txt = re.sub(r'<[^>]+>', '', t).strip()
    if len(txt) >= 10 and re.search(r'[\u4e00-\u9fff]', txt):
        clean.append(txt)

full = '\n'.join(clean)
print('Paragraphs:', len(clean), 'chars:', len(full))
print()
print('--- CONTENT (first 10) ---')
for p in clean[:10]:
    print(p)
print()
print('--- LAST 5 ---')
for p in clean[-5:]:
    print(p)

# Save
out_raw = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_raw_0525.txt'
out_json = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_struct_0525.json'
with open(out_raw, 'w', encoding='utf-8') as f:
    f.write('Title: ' + title + '\nURL: ' + url + '\nDate: ' + datetime.now().strftime('%Y-%m-%d') + '\n\n' + full)
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({'title': title, 'desc': desc, 'url': url, 'img': img, 'date': datetime.now().strftime('%Y-%m-%d'), 'paragraphs': clean}, f, ensure_ascii=False, indent=2)
print('Saved. Total chars:', len(full))