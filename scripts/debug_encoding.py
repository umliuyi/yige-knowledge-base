import urllib.request
import re

url = 'https://36kr.com/feed'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    raw = resp.read()

# Find item structure in raw bytes
pos = raw.find(b'<item>')
if pos >= 0:
    snippet = raw[pos:pos+500]
    print('Raw around item:')
    print(repr(snippet[:200]))

# Try encoding detection by looking at raw bytes for Chinese
# GBK Chinese chars are in range 0x8140-0xFEFE
has_gbk_signature = b'\xb9\xfb' in raw[:5000] or b'\xc7\xd0' in raw[:5000]
print(f'Has GBK signature: {has_gbk_signature}')

# Try GBK directly
try:
    content = raw.decode('gbk')
    t = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', content)
    print(f'GBK+CDATA titles: {len(t)}')
    for x in t[:3]:
        print(f'  {repr(x[:50])}')
except Exception as e:
    print(f'GBK fail: {e}')