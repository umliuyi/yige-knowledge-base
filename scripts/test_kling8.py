import urllib.request, json, time, hashlib, hmac, base64

ak = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
sk = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
ts = str(int(time.time()))

# Try POST with Bearer token + different signature approaches
body_img = '{"model":" Kling 1.0","prompt":"a beautiful landscape","image_size":"1024x1024"}'

def call_with_sig(url, body, sig):
    headers = {
        'Authorization': f'Bearer {ak}',
        'X-Access-Key': ak,
        'X-Signature': sig,
        'X-Timestamp': ts,
        'Content-Type': 'application/json'
    }
    req = urllib.request.Request(url, data=body.encode(), headers=headers, method='POST')
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.status, resp.read().decode()[:200]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)[:80]
        return 'err', err

url = 'https://api.klingai.com/v1/images/generations'

# Try different message formats for signature
def mk_msg(*parts): return ''.join(parts)
def sig(secret, msg): return base64.b64encode(hmac.new(secret.encode(), msg.encode(), hashlib.sha256).digest()).decode()

tests = [
    # Format: timestamp only
    ('ts', sig(sk, ts)),
    # Format: body hash only  
    ('body_hash', sig(sk, hashlib.sha256(body_img.encode()).hexdigest())),
    # Format: ts + body hash
    ('ts_bodyhash', sig(sk, ts + hashlib.sha256(body_img.encode()).hexdigest())),
    # Format: access_key + ts
    ('ak_ts', sig(sk, ak + ts)),
    # Format: ts + access_key
    ('ts_ak', sig(sk, ts + ak)),
    # Format: secret + timestamp
    ('sk_ts', sig(sk, sk + ts)),
    # Format: timestamp + secret
    ('ts_sk', sig(sk, ts + sk)),
    # Format: full request string
    ('req_str', sig(sk, f'POST\n/v1/images/generations\n{ts}\n{body_img}')),
    # Format: just access_key
    ('ak_only', sig(sk, ak)),
    # Format: body only
    ('body_only', sig(sk, body_img)),
    # Format: ts + body
    ('ts_body', sig(sk, ts + body_img)),
    # Format: body + ts
    ('body_ts', sig(sk, body_img + ts)),
    # Format: ak + ts + body_hash
    ('ak_ts_bh', sig(sk, ak + ts + hashlib.sha256(body_img.encode()).hexdigest())),
    # Format: ts + ak + body_hash
    ('ts_ak_bh', sig(sk, ts + ak + hashlib.sha256(body_img.encode()).hexdigest())),
]

for name, sig_val in tests:
    status, result = call_with_sig(url, body_img, sig_val)
    code = ''
    if status == 'err':
        try:
            code = json.loads(result.split('{')[1].split('}')[0]) if '{' in result else ''
        except: pass
    print(name, '->', status, result[:80])