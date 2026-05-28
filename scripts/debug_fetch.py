# -*- coding: utf-8 -*-
import urllib.request, ssl, re, json
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://36kr.com/feed', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw = resp.read().decode('utf-8', errors='ignore')

# Try different CDATA patterns
cdata1 = re.findall(r'<!\[CDATA\[(.*?)\]\]>', raw)
cdata2 = re.findall(r'<!\[CDATA\[([\s\S]*?)\]>', raw)  
print('Pattern1 CDATA count:', len(cdata1))
print('First 3:')
for c in cdata1[:3]:
    print(' ', repr(c[:80]))
print('Total raw length:', len(raw))
print('Sample raw:', repr(raw[500:700]))
