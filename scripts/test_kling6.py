import urllib.request, json, time, hashlib, hmac, base64

ak = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
sk = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
ts = str(int(time.time()))
body = '{"prompt":"test"}'

def call(sig):
    headers = {
        'Authorization': f'Bearer {ak}',
        'X-Access-Key': ak,
        'X-Signature': sig,
        'X-Timestamp': ts,
        'Content-Type': 'application/json'
    }
    url = 'https://api.klingai.com/v1/images/generations'
    try:
        req = urllib.request.Request(url, data=body.encode(), headers=headers, method='POST')
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.status, resp.read().decode()[:200]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)[:80]
        return 'err', err

def h(s): return base64.b64encode(hmac.new(sk.encode(), s.encode(), hashlib.sha256).digest()).decode()

tests = [
    ('ts', h(ts)),
    ('ts+sk', h(ts+sk)),
    ('sk', h(sk)),
    ('body', h(body)),
    ('ts+path', h(ts + '/v1/images/generations')),
    ('ak+ts', h(ak+ts)),
    ('ts+ak', h(ts+ak)),
    ('ts+body+sk', h(ts+body+sk)),
    ('ts+sk+body', h(ts+sk+body)),
    ('sk+ts+body', h(sk+ts+body)),
    ('ak+sk+ts', h(ak+sk+ts)),
    ('sk+ak+ts', h(sk+ak+ts)),
    ('ts+body+ak', h(ts+body+ak)),
    ('body+ts+sk', h(body+ts+sk)),
]
for name, sig in tests:
    status, result = call(sig)
    print(name, '->', status, result[:60])