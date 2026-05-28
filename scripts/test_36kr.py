# -*- coding: utf-8 -*-
import urllib.request, ssl, sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://36kr.com/feed',
    headers={'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'identity'}
)
resp = urllib.request.urlopen(req, timeout=10, context=ctx)
raw = resp.read()

# Detect encoding
for enc in ('utf-8', 'gbk', 'gb2312', 'iso-8859-1'):
    try:
        text = raw.decode(enc)
        print(f'Encoding: {enc}')
        break
    except:
        continue

# Parse items
import xml.etree.ElementTree as ET
root = ET.fromstring(raw)

count = 0
for elem in root.iter():
    tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
    if tag in ('title') and elem.text:
        title = elem.text.strip()
        if len(title) > 8:
            print(f'  [{count+1}] {title[:60]}')
            count += 1
            if count >= 8:
                break

print(f'Total titles: {count}')
