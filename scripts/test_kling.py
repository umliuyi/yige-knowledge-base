import urllib.request, json, time, hashlib, hmac, base64

access_key = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
secret_key = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
ts = str(int(time.time()))

tests = [
    ('GET', 'https://api.klingai.com/v1/user/info', ''),
    ('GET', 'https://api.klingai.com/v1/images', ''),
    ('POST', 'https://api.klingai.com/v1/images/generations', '{"model":" Kling 1"}'),
    ('POST', 'https://api.klingai.com/api/v1/images/generations', '{"model":" Kling 1"}'),
]

for method, url, body in tests:
    headers = {
        'X-Access-Key': access_key,
        'X-Timestamp': ts,
        'Content-Type': 'application/json'
    }
    try:
        if method == 'POST':
            data = body.encode()
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        else:
            req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        print(f'{method} {url} -> {resp.status}')
        print(resp.read().decode()[:200])
    except Exception as e:
        print(f'{method} {url} -> Error: {str(e)[:100]}')