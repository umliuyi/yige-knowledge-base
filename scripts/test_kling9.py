import urllib.request, json, time, hashlib, hmac, base64

ak = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
sk = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
ts = str(int(time.time()))

body_img = '{"model":" Kling 1.0","prompt":"a beautiful landscape","image_size":"1024x1024"}'

def call(sig):
    headers = {
        'Authorization': f'Bearer {ak}',
        'X-Access-Key': ak,
        'X-Signature': sig,
        'X-Timestamp': ts,
        'Content-Type': 'application/json'
    }
    url = 'https://api.klingai.com/v1/images/generations'
    req = urllib.request.Request(url, data=body_img.encode(), headers=headers, method='POST')
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.status, resp.read().decode()[:200]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)[:80]
        return 'err', err

tests = [
    ('ts_hex_raw', hmac.new(sk.encode(), ts.encode(), hashlib.sha256).hexdigest()),
    ('ts_b64_raw', base64.b64encode(hmac.new(sk.encode(), ts.encode(), hashlib.sha256).digest()).decode()),
    ('body_utf8', base64.b64encode(hmac.new(sk.encode(), body_img.encode('utf-8'), hashlib.sha256).digest()).decode()),
    ('method_body', base64.b64encode(hmac.new(sk.encode(), ('POST' + body_img).encode(), hashlib.sha256).digest()).decode()),
    ('ak_body_ts', base64.b64encode(hmac.new(sk.encode(), (ak + body_img + ts).encode(), hashlib.sha256).digest()).decode()),
    ('path_ts', base64.b64encode(hmac.new(sk.encode(), ('/v1/images/generations' + ts).encode(), hashlib.sha256).digest()).decode()),
    ('bodyhash_b64', base64.b64encode(hashlib.sha256(body_img.encode()).digest()).decode()),
    ('bodyhash_hex', hashlib.sha256(body_img.encode()).hexdigest()),
    ('ts_nl_body', base64.b64encode(hmac.new(sk.encode(), (ts + '\n' + body_img).encode(), hashlib.sha256).digest()).decode()),
    ('double_hmac', base64.b64encode(hmac.new(hmac.new(sk.encode(), ak.encode(), hashlib.sha256).digest(), ts.encode(), hashlib.sha256).digest()).decode()),
    ('ak_only', base64.b64encode(hmac.new(sk.encode(), ak.encode(), hashlib.sha256).digest()).decode()),
    ('sk_only', base64.b64encode(hmac.new(sk.encode(), sk.encode(), hashlib.sha256).digest()).decode()),
    ('ak_ts_body', base64.b64encode(hmac.new(sk.encode(), (ak + ts + body_img).encode(), hashlib.sha256).digest()).decode()),
    ('ts_ak_body', base64.b64encode(hmac.new(sk.encode(), (ts + ak + body_img).encode(), hashlib.sha256).digest()).decode()),
    ('body_ak_ts', base64.b64encode(hmac.new(sk.encode(), (body_img + ak + ts).encode(), hashlib.sha256).digest()).decode()),
    ('ts_body_ak', base64.b64encode(hmac.new(sk.encode(), (ts + body_img + ak).encode(), hashlib.sha256).digest()).decode()),
    ('req_full', base64.b64encode(hmac.new(sk.encode(), (ts + 'POST' + '/v1/images/generations' + body_img).encode(), hashlib.sha256).digest()).decode()),
    ('req_nb', base64.b64encode(hmac.new(sk.encode(), (ts + 'POST/v1/images/generations' + body_img).encode(), hashlib.sha256).digest()).decode()),
    ('req_ns', base64.b64encode(hmac.new(sk.encode(), ('POST /v1/images/generations ' + ts + ' ' + body_img).encode(), hashlib.sha256).digest()).decode()),
]

for name, sig in tests:
    status, result = call(sig)
    print(name, '->', status, result[:80])