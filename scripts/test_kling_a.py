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
        return resp.status, resp.read().decode()[:300]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)[:80]
        return 'err', err

# Try HMAC-SHA1 (not SHA256) - some older APIs use this
tests_sha1 = [
    ('sha1_ts', base64.b64encode(hmac.new(sk.encode(), ts.encode(), hashlib.sha1).digest()).decode()),
    ('sha1_body', base64.b64encode(hmac.new(sk.encode(), body_img.encode(), hashlib.sha1).digest()).decode()),
    ('sha1_ts_body', base64.b64encode(hmac.new(sk.encode(), (ts + body_img).encode(), hashlib.sha1).digest()).decode()),
    ('sha1_ak_body', base64.b64encode(hmac.new(sk.encode(), (ak + body_img).encode(), hashlib.sha1).digest()).decode()),
]

# Also try HMAC-SHA256 but output as raw binary (not base64)
tests_binary = [
    ('bin_ts', hmac.new(sk.encode(), ts.encode(), hashlib.sha256).digest().hex()),
    ('bin_body', hmac.new(sk.encode(), body_img.encode(), hashlib.sha256).digest().hex()),
    ('bin_ts_body', hmac.new(sk.encode(), (ts + body_img).encode(), hashlib.sha256).digest().hex()),
    ('bin_ak_body', hmac.new(sk.encode(), (ak + body_img).encode(), hashlib.sha256).digest().hex()),
]

# Also try MD5-based
tests_md5 = [
    ('md5_ts', hashlib.md5((sk + ts).encode()).hexdigest()),
    ('md5_body', hashlib.md5((sk + body_img).encode()).hexdigest()),
]

# Also try including body in signature differently
tests_other = [
    # Use body as-is, not hashed
    ('raw_sig1', base64.b64encode(hmac.new((sk + ts).encode(), body_img.encode(), hashlib.sha256).digest()).decode()),
    ('raw_sig2', base64.b64encode(hmac.new((ts + sk).encode(), body_img.encode(), hashlib.sha256).digest()).decode()),
    # Different delimiter
    ('delim1', base64.b64encode(hmac.new(sk.encode(), (ts + '|' + body_img).encode(), hashlib.sha256).digest()).decode()),
    ('delim2', base64.b64encode(hmac.new(sk.encode(), (ts + ':' + body_img).encode(), hashlib.sha256).digest()).decode()),
    ('delim3', base64.b64encode(hmac.new(sk.encode(), (ts + body_img + sk).encode(), hashlib.sha256).digest()).decode()),
    # Try with request body as JSON string
    ('json_str', base64.b64encode(hmac.new(sk.encode(), json.dumps(json.loads(body_img), separators=(',', ':')).encode(), hashlib.sha256).digest()).decode()),
]

for name, sig in tests_sha1 + tests_binary + tests_md5 + tests_other:
    status, result = call(sig)
    print(name, '->', status, result[:80])