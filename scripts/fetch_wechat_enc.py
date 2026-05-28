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

# Try detect encoding from headers or content-type
content_type = resp.headers.get('Content-Type', '')
charset = re.search(r'charset=([^\s;"]+)', content_type)
if charset:
    encoding = charset.group(1)
else:
    encoding = 'utf-8'

print('Detected encoding:', encoding)
raw = raw_bytes.decode(encoding, errors='ignore')

# If still garbled, try GBK
if not re.search(r'[\u4e00-\u9fff]', raw[:2000]):
    raw = raw_bytes.decode('gbk', errors='ignore')
    print('Re-trying with GBK')

# Extract OG
og_title = re.search(r'<meta property="og:title" content="([^"]+)"', raw)
og_desc = re.search(r'<meta property="og:description" content="([^"]+)"', raw)
og_img = re.search(r'<meta property="og:image" content="([^"]+)"', raw)
title = og_title.group(1) if og_title else ''
desc = og_desc.group(1) if og_desc else ''
img = og_img.group(1) if og_img else ''

print('Title:', title)
print('Has Chinese in title:', bool(re.search(r'[\u4e00-\u9fff]', title)))

# Extract text
texts = re.findall(r'<(?:p|span)[^>]*>(.*?)</(?:p|span)>', raw, re.DOTALL)
clean = []
for t in texts:
    txt = re.sub(r'<[^>]+>', '', t).strip()
    if len(txt) >= 10 and re.search(r'[\u4e00-\u9fff]', txt):
        clean.append(txt)

full = '\n'.join(clean)
print('Chinese paragraphs:', len(clean))
print('First 3:')
for p in clean[:3]:
    print(' -', p[:60])

# Save
out_raw = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_raw_0525.txt'
out_json = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_struct_0525.json'
with open(out_raw, 'w', encoding='utf-8') as f:
    f.write(f'Title: {title}\nDesc: {desc}\nURL: {url}\n\n{full}')
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({'title': title, 'desc': desc, 'url': url, 'img': img, 'paragraphs': clean}, f, ensure_ascii=False, indent=2)
print('Done')