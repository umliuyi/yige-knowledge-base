import urllib.request, json, time, hashlib, hmac, base64, urllib.parse

access_key = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
secret_key = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
ts = str(int(time.time()))

# Try signing POST requests with HMAC
def sign_post(secret, body, ts):
    msg = f'{ts}\n{body}'
    return base64.b64encode(hmac.new(secret.encode(), msg.encode(), hashlib.sha256).digest()).decode()

body_img = '{"prompt":"a beautiful landscape","model":" Kling 1.0"}'
body_vid = '{"prompt":"a man walking in the city","model":" Kling 1.0"}'

tests = [
    ('POST', 'https://api.klingai.com/v1/images/generations', body_img),
    ('POST', 'https://api.klingai.com/v1/videos/generations', body_vid),
    ('POST', 'https://api.klingai.com/v1/images/generations', '{"prompt":"landscape"}'),
    ('POST', 'https://api.klingai.com/v1/videos/generations', '{"prompt":"man walking"}'),
]
for method, url, body in tests:
    sig = sign_post(secret_key, body, ts)
    headers = {
        'Authorization': f'Bearer {access_key}',
        'X-Access-Key': access_key,
        'X-Signature': sig,
        'X-Timestamp': ts,
        'Content-Type': 'application/json'
    }
    try:
        req = urllib.request.Request(url, data=body.encode(), headers=headers, method='POST')
        resp = urllib.request.urlopen(req, timeout=10)
        body_resp = resp.read().decode()
        print(f'{method} {url} -> {resp.status}:', body_resp[:300])
    except Exception as e:
        err = ''
        if hasattr(e, 'read'):
            err = e.read().decode()
        print(f'{method} {url} -> Error: {str(e)[:60]} | {err[:100]}')