# -*- coding: utf-8 -*-
import urllib.request, ssl, re, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://mp.weixin.qq.com/s/jUT9zcatb4s0QX6bQjUhVQ'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://mp.weixin.qq.com/',
}

req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
html = resp.read().decode('utf-8', errors='ignore')

# Extract image URLs
img_urls = re.findall(r'https?://mmbiz\.qpic\.cn[^\s"\'<>]+', html)
print(f'Found {len(img_urls)} images')

# Deduplicate
seen = set()
unique = []
for u in img_urls:
    if u not in seen:
        seen.add(u)
        unique.append(u)

print(f'Unique: {len(unique)}')
for i, u in enumerate(unique[:5]):
    print(f'  [{i}] {u[:80]}...')

# Save first image
if unique:
    try:
        img_req = urllib.request.Request(unique[0], headers=headers)
        img_resp = urllib.request.urlopen(img_req, timeout=10, context=ctx)
        img_data = img_resp.read()
        out = os.path.join(r'C:\Users\Administrator\.openclaw-autoclaw\workspace', 'wechat_img1.jpg')
        with open(out, 'wb') as f:
            f.write(img_data)
        print(f'Saved first image: {len(img_data)} bytes to {out}')
    except Exception as e:
        print(f'Image save failed: {e}')
