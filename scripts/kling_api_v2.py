import urllib.request, json, time, hashlib, hmac

ak = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
sk = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'

def make_headers(body=''):
    ts = str(int(time.time()))
    signature = hmac.new(sk.encode(), (ts + body).encode(), hashlib.sha256).digest()
    signature = signature.hex()
    return {
        'Authorization': 'Bearer ' + ak,
        'X-Access-Key': ak,
        'X-Signature': signature,
        'X-Timestamp': ts,
        'Content-Type': 'application/json'
    }

def call(method, url, body=''):
    h = make_headers(body)
    try:
        if method == 'POST':
            req = urllib.request.Request(url, data=body.encode(), headers=h, method='POST')
        else:
            req = urllib.request.Request(url, headers=h, method='GET')
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.status, resp.read().decode()[:500]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)
        return 'err', err[:200]

# Try account/credit/quota/info endpoints
tests = [
    ('GET account', 'GET', 'https://api.klingai.com/v1/account', ''),
    ('GET quota', 'GET', 'https://api.klingai.com/v1/quota', ''),
    ('GET credits', 'GET', 'https://api.klingai.com/v1/credits', ''),
    ('GET info', 'GET', 'https://api.klingai.com/v1/info', ''),
    ('GET me', 'GET', 'https://api.klingai.com/v1/me', ''),
    ('GET balance', 'GET', 'https://api.klingai.com/v1/balance', ''),
    ('GET usage', 'GET', 'https://api.klingai.com/v1/usage', ''),
    ('GET video_tasks', 'GET', 'https://api.klingai.com/v1/video_tasks', ''),
    ('GET img_tasks', 'GET', 'https://api.klingai.com/v1/image_tasks', ''),
    # Try POST to check if video task creation works with minimal body
    ('POST vid_task2', 'POST', 'https://api.klingai.com/v1/video_tasks', '{"model":"Kling 1.0"}'),
    # Try with correct model name - from the app screenshot
    ('vid_c2l', 'POST', 'https://api.klingai.com/v1/videos/generations', '{"model":"Kling","prompt":"a man walking","duration":"5","ratio":"16:9"}'),
]

for name, method, url, body in tests:
    status, result = call(method, url, body)
    print(name, '->', status, result[:120])
    print()