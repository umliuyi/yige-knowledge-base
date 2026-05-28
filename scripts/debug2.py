# -*- coding: utf-8 -*-
import urllib.request, ssl, re
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
req = urllib.request.Request('https://36kr.com/feed', headers={'User-Agent':'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw = resp.read().decode('utf-8', errors='ignore')
patterns = [
    ('CDATA [CDATA[', re.findall(r'<!\[CDATA\[(.*?)\]\]>', raw)),
    ('link href', re.findall(r'<link[^>]*href=["\']([^"\']+)["\']', raw)),
    ('item link', re.findall(r'<item[^>]*>.*?<link[^>]*>(.*?)</link>', raw, re.DOTALL)),
]
for name, results in patterns:
    print(f'Pattern "{name[0]}": {len(results)} hits')
    for r in results[:3]:
        print('  ', repr(r[:80]))
print('Raw sample:', repr(raw[200:500]))
