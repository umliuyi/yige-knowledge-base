# -*- coding: utf-8 -*-
import urllib.request, ssl, re, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://mp.weixin.qq.com/s/MWH5SvWrYIL3Lic0v6bXtQ'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://mp.weixin.qq.com/',
}

req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
html = resp.read().decode('utf-8', errors='ignore')

# Extract content
m = re.search(r'id="js_content"[^>]*>(.*?)</div>', html, re.DOTALL)
if m:
    raw = m.group(1)
    text = re.sub(r'<[^>]+>', '', raw)
    text = re.sub(r'\s+', ' ', text).strip()
    out = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_article2.txt'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(text)
    print('TEXT SAVED:', len(text), 'chars')
else:
    print('NO CONTENT')

# Extract images
img_urls = re.findall(r'https?://mmbiz\.qpic\.cn/mmbiz_jpg/[^\s"\'<>]+', html)
img_urls += re.findall(r'https?://mmbiz\.qpic\.cn/mmbiz_png/[^\s"\'<>]+', html)
seen = set()
unique = []
for u in img_urls:
    if u not in seen:
        seen.add(u)
        unique.append(u)
print(f'Found {len(unique)} images')

saved = []
for i, u in enumerate(unique):
    try:
        ir = urllib.request.Request(u[:200], headers=headers)
        iv = urllib.request.urlopen(ir, timeout=8, context=ctx)
        data = iv.read()
        if len(data) > 10000:
            out = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat2_img_%d.jpg' % i
            with open(out, 'wb') as f:
                f.write(data)
            saved.append((i, len(data)))
    except:
        pass
print(f'Saved {len(saved)} images > 10KB')
for i, sz in saved:
    print(f'  wechat2_img_{i}.jpg - {sz//1024}KB')
