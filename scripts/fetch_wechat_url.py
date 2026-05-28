import urllib.request, ssl, re, sys
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://mp.weixin.qq.com/s/S5p6ssSQfGLRenxeGCmPuw'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://mp.weixin.qq.com/'
})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw = resp.read().decode('utf-8', errors='ignore')

print('Page size:', len(raw))

# OG tags
og_title = re.search(r'<meta property="og:title" content="([^"]+)"', raw)
og_desc = re.search(r'<meta property="og:description" content="([^"]+)"', raw)
og_img = re.search(r'<meta property="og:image" content="([^"]+)"', raw)
print('OG title:', og_title.group(1) if og_title else 'N/A')
print('OG desc:', og_desc.group(1)[:80] if og_desc else 'N/A')
print('OG img:', og_img.group(1)[:80] if og_img else 'N/A')

# Extract text paragraphs
texts = re.findall(r'<p[^>]*>(.*?)</p>', raw, re.DOTALL)
count = 0
for t in texts:
    clean = re.sub(r'<[^>]+>', '', t).strip()
    if len(clean) > 20:
        print('P:', clean[:100])
        count += 1
        if count >= 20:
            break