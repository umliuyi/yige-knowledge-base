import urllib.request, json, time, hashlib, hmac, base64

ak = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
sk = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
ts = str(int(time.time()))

body_img = '{"model":" Kling 1.0","prompt":"a beautiful landscape"}'

def call(url, headers, body):
    req = urllib.request.Request(url, data=body.encode(), headers=headers, method='POST')
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.status, resp.read().decode()[:300]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)[:80]
        return 'err', err

url = 'https://api.klingai.com/v1/images/generations'

# Try base64-encoded secret key as HMAC key
sk_b64 = base64.b64encode(sk.encode()).decode()

# Try empty signature (test if signature is even checked)
tests = [
    # (name, headers_dict)
    ('empty_sig', {'Authorization': 'Bearer ' + ak, 'X-Access-Key': ak, 'X-Signature': '', 'X-Timestamp': ts, 'Content-Type': 'application/json'}),
    ('no_sig', {'Authorization': 'Bearer ' + ak, 'X-Access-Key': ak, 'X-Timestamp': ts, 'Content-Type': 'application/json'}),
    ('no_ts', {'Authorization': 'Bearer ' + ak, 'X-Access-Key': ak, 'X-Signature': 'test', 'Content-Type': 'application/json'}),
    ('bearer_only', {'Authorization': 'Bearer ' + ak, 'Content-Type': 'application/json'}),
    ('b64_sk_ts', {'Authorization': 'Bearer ' + ak, 'X-Access-Key': ak, 'X-Signature': base64.b64encode(hmac.new(sk_b64.encode(), ts.encode(), hashlib.sha256).digest()).decode(), 'X-Timestamp': ts, 'Content-Type': 'application/json'}),
    ('b64_sk_body', {'Authorization': 'Bearer ' + ak, 'X-Access-Key': ak, 'X-Signature': base64.b64encode(hmac.new(sk_b64.encode(), body_img.encode(), hashlib.sha256).digest()).decode(), 'X-Timestamp': ts, 'Content-Type': 'application/json'}),
    ('plain_sk', {'Authorization': 'Bearer ' + ak, 'X-Access-Key': ak, 'X-Signature': sk, 'X-Timestamp': ts, 'Content-Type': 'application/json'}),
    ('plain_ak', {'Authorization': 'Bearer ' + ak, 'X-Access-Key': ak, 'X-Signature': ak, 'X-Timestamp': ts, 'Content-Type': 'application/json'}),
    ('hmac_plain', {'Authorization': 'Bearer ' + ak, 'X-Access-Key': ak, 'X-Signature': base64.b64encode(hmac.new(sk.encode(), (ts + body_img).encode(), hashlib.sha256).digest()).decode(), 'X-Timestamp': ts, 'Content-Type': 'application/json'}),
    ('hmac_hex', {'Authorization': 'Bearer ' + ak, 'X-Access-Key': ak, 'X-Signature': hmac.new(sk.encode(), (ts + body_img).encode(), hashlib.sha256).hexdigest(), 'X-Timestamp': ts, 'Content-Type': 'application/json'}),
]

for name, headers in tests:
    status, result = call(url, headers, body_img)
    print(name, '->', status, result[:80])