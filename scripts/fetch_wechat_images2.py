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

# Extract image URLs - look for larger images
img_urls = re.findall(r'https?://mmbiz\.qpic\.cn/mmbiz_jpg/[^\s"\'<>]+', html)
img_urls += re.findall(r'https?://mmbiz\.qpic\.cn/mmbiz_png/[^\s"\'<>]+', html)

# Filter by minimum size
seen = set()
unique = []
for u in img_urls:
    if u not in seen:
        seen.add(u)
        unique.append(u)

print(f'Found {len(unique)} unique images')

saved = []
for i, u in enumerate(unique[:10]):
    try:
        img_req = urllib.request.Request(u[:200], headers=headers)
        img_resp = urllib.request.urlopen(img_req, timeout=8, context=ctx)
        data = img_resp.read()
        size = len(data)
        if size > 10000:  # Only save images > 10KB
            out = os.path.join(r'C:\Users\Administrator\.openclaw-autoclaw\workspace', f'wechat_img_{i}.jpg')
            with open(out, 'wb') as f:
                f.write(data)
            saved.append((i, size, out))
            print(f'  [{i}] {size} bytes - SAVED')
        else:
            print(f'  [{i}] {size} bytes - too small')
    except Exception as e:
        print(f'  [{i}] FAIL: {str(e)[:30]}')

print(f'\nSaved {len(saved)} images > 10KB')
for idx, size, path in saved:
    print(f'  wechat_img_{idx}.jpg - {size//1024}KB')
