# fetch 36kr RSS
import urllib.request, ssl, re, json
from datetime import datetime
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
url = 'https://36kr.com/feed'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw = resp.read().decode('utf-8', errors='ignore')
# try CDATA
hits = re.findall(r'<!\[CDATA\[(.*?)\]\]>', raw)
print('CDATA count:', len(hits))
for h in hits[:5]: print(' -', repr(h[:50]))
print('Total raw len:', len(raw))
print('Sample:', repr(raw[300:600]))
