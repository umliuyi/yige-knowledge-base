import urllib.request, json, time, hashlib, hmac, base64

access_key = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
secret_key = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
ts = str(int(time.time()))
body = '{"prompt":"test"}'

# Try various signing approaches
def call(sig):
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

# Try HMAC-SHA256 with different message formats
def hmac_sha256(msg):
    return base64.b64encode(hmac.new(secret_key.encode(), msg.encode(), hashlib.sha256).digest()).decode()

# Some APIs use: HMAC-SHA256(secret_key, timestamp + method + path + body)
def sig_a(ts, body):
    msg = ts + 'POST' + '/v1/images/generations' + body
    return hmac_sha256(msg)

def sig_b(ts, body):
    msg = ts + body
    return hmac_sha256(msg)

def sig_c(ts, body):
    # Maybe use SHA256 hash of body, not raw body
    body_hash = hashlib.sha256(body.encode()).hexdigest()
    msg = ts + body_hash
    return hmac_sha256(msg)

def sig_d(ts, body):
    msg = access_key + ts + body
    return hmac_sha256(msg)

def sig_e(ts, body):
    msg = secret_key + ts + body
    return hmac_sha256(msg)

def sig_f(ts, body):
    msg = access_key
    return hmac_sha256(msg)

def sig_g(ts, body):
    # Using empty body for signature
    return hmac_sha256(ts + secret_key)

def sig_h(ts, body):
    # Using raw request text
    raw = f'POST\n/v1/images/generations\n{ts}\n{body}'
    return base64.b64encode(hmac.new(secret_key.encode(), raw.encode(), hashlib.sha256).digest()).decode()

for name, fn in [('a', sig_a), ('b', sig_b), ('c', sig_c), ('d', sig_d), ('e', sig_e), ('f', sig_f), ('g', sig_g), ('h', sig_h)]:
    sig = fn(ts, body)
    status, result = call(sig)
    print(name, '->', status, result[:60])