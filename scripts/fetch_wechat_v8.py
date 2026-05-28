import urllib.request, ssl, re, json, html as html_module
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
raw_utf8 = raw_bytes.decode('utf-8', errors='ignore')
raw_gbk = raw_bytes.decode('gbk', errors='ignore')

print('UTF-8 CJK:', len(re.findall(r'[\u4e00-\u9fff]', raw_utf8)))
print('GBK CJK:', len(re.findall(r'[\u4e00-\u9fff]', raw_gbk)))
print('Content-Type:', resp.headers.get('Content-Type'))
print()

# Find og:title in both encodings
for name, raw in [('UTF-8', raw_utf8), ('GBK', raw_gbk)]:
    m = re.search(r'<meta property="og:title" content="([^"]+)"', raw)
    if m:
        print(name + ' og:title raw:', repr(m.group(1)[:60]))

# Find first non-garbled title in UTF-8 og:title
# The key issue: og:title in the raw UTF-8 decoded string has replacement chars
# We can try: encode the GBK og:title back to bytes, then decode as UTF-8
gbk_og = re.search(r'<meta property="og:title" content="([^"]+)"', raw_gbk)
if gbk_og:
    gbk_title = gbk_og.group(1)
    print('GBK og:title:', repr(gbk_title[:60]))
    # Encode GBK title back to bytes
    gbk_bytes = gbk_title.encode('gbk')
    utf8_recover = gbk_bytes.decode('utf-8', errors='replace')
    print('Recovered from GBK bytes:', repr(utf8_recover[:60]))
    chinese_recovered = re.findall(r'[\u4e00-\u9fff]+', utf8_recover)
    if chinese_recovered:
        print('Recovered Chinese words:', ''.join(chinese_recovered)[:40])

# Try same for description
gbk_desc_m = re.search(r'<meta property="og:description" content="([^"]+)"', raw_gbk)
if gbk_desc_m:
    gbk_desc = gbk_desc_m.group(1)
    gbk_bytes_desc = gbk_desc.encode('gbk')
    utf8_recover_desc = gbk_bytes_desc.decode('utf-8', errors='replace')
    print()
    print('Recovered desc:', repr(utf8_recover_desc[:80]))

# Extract body paragraphs
texts = re.findall(r'<(?:p|span)[^>]*>(.*?)</(?:p|span)>', raw_gbk, re.DOTALL)
clean = []
for t in texts:
    txt = re.sub(r'<[^>]+>', '', t).strip()
    if len(txt) >= 10 and re.search(r'[\u4e00-\u9fff]', txt):
        txt = html_module.unescape(txt)
        clean.append(txt)

print()
print('Paragraphs:', len(clean), 'chars:', sum(len(p) for p in clean))
for p in clean[:5]:
    print(p)
print()
for p in clean[-3:]:
    print(p)