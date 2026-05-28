import urllib.request, ssl, re
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
req = urllib.request.Request('https://36kr.com/feed', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw = resp.read().decode('utf-8', errors='ignore')
titles_raw = re.findall(r'<title><!\[CDATA\[([^\]]+)\]\]></title>', raw)
print('Total titles:', len(titles_raw))
for t in titles_raw[1:11]:
    print(repr(t[:60]))
