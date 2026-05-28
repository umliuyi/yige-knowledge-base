import urllib.request, json, time, hashlib, hmac, base64

access_key = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
secret_key = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
ts = str(int(time.time()))
body = '{"prompt":"test"}'

def call(sig_fn):
    sig = sig_fn(secret_key, 'POST', '/v1/images/generations', body, ts, access_key)
    headers = {
        'Authorization': f'Bearer {access_key}',
        'X-Access-Key': access_key,
        'X-Signature': sig,
        'X-Timestamp': ts,
        'Content-Type': 'application/json'
    }
    url = 'https://api.klingai.com/v1/images/generations'
    try:
        req = urllib.request.Request(url, data=body.encode(), headers=headers, method='POST')
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.status, resp.read().decode()[:100]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)[:80]
        return 'err', err

def sig1(sk, m, p, b, t, ak): return base64.b64encode(hmac.new(sk.encode(), (t + b).encode(), hashlib.sha256).digest()).decode()
def sig2(sk, m, p, b, t, ak): return base64.b64encode(hmac.new(sk.encode(), (t + '|' + b).encode(), hashlib.sha256).digest()).decode()
def sig3(sk, m, p, b, t, ak): return base64.b64encode(hmac.new(sk.encode(), (b + t).encode(), hashlib.sha256).digest()).decode()
def sig4(sk, m, p, b, t, ak): return base64.b64encode(hmac.new(sk.encode(), (m + p + t + b).encode(), hashlib.sha256).digest()).decode()
def sig5(sk, m, p, b, t, ak): return base64.b64encode(hmac.new(sk.encode(), (ak + t + b).encode(), hashlib.sha256).digest()).decode()
def sig6(sk, m, p, b, t, ak): return base64.b64encode(hmac.new(sk.encode(), (t + ak + b).encode(), hashlib.sha256).digest()).decode()
def sig7(sk, m, p, b, t, ak): return base64.b64encode(hmac.new(sk.encode(), (ak + b + t).encode(), hashlib.sha256).digest()).decode()

for name, fn in [('ts+body', sig1), ('ts|body', sig2), ('body+ts', sig3), ('m+p+t+b', sig4), ('ak+t+b', sig5), ('t+ak+b', sig6), ('ak+b+t', sig7)]:
    status, result = call(fn)
    print(name, '->', status, result[:60])