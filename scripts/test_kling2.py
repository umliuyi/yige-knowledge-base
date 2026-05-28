import urllib.request, json, time, hashlib, hmac, base64

access_key = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
secret_key = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
ts = str(int(time.time()))

# SUCCESS: Bearer auth with access_key as token
tests = [
    ('GET', 'https://api.klingai.com/v1/user/info'),
    ('GET', 'https://api.klingai.com/v1/images'),
    ('GET', 'https://api.klingai.com/v1/videos'),
    ('POST', 'https://api.klingai.com/v1/images/generations', '{"prompt":"a beautiful landscape"}'),
    ('POST', 'https://api.klingai.com/v1/videos/generations', '{"prompt":"a man walking"}'),
]
for item in tests:
    method = item[0]
    url = item[1]
    body = item[2] if len(item) > 2 else ''
    headers = {
        'Authorization': f'Bearer {access_key}',
        'Content-Type': 'application/json'
    }
    try:
        if method == 'POST':
            req = urllib.request.Request(url, data=body.encode(), headers=headers, method='POST')
        else:
            req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        body_resp = resp.read().decode()
        print(f'{method} {url} -> {resp.status}:', body_resp[:200])
    except Exception as e:
        err = ''
        if hasattr(e, 'read'):
            err = e.read().decode()
        print(f'{method} {url} -> Error: {str(e)[:60]} | {err[:80]}')