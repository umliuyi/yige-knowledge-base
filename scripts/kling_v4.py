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

def call(method, url, body, ctype='application/json'):
    h = make_headers(body)
    h['Content-Type'] = ctype
    try:
        if method == 'POST':
            req = urllib.request.Request(url, data=body.encode('utf-8'), headers=h, method='POST')
        else:
            req = urllib.request.Request(url, headers=h, method='GET')
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.status, resp.read().decode()[:500]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)
        return 'err', err[:200]

vid_url = 'https://api.klingai.com/v1/videos/generations'
img_url = 'https://api.klingai.com/v1/images/generations'

tests = [
    # Try form-urlencoded for video
    ('vid_form', 'POST', vid_url, 'model=Kling 1.0&prompt=a man walking&duration=5&ratio=16:9', 'application/x-www-form-urlencoded'),
    # Try text instead of prompt
    ('vid_text', 'POST', vid_url, '{"model":"Kling 1.0","text":"a man walking","duration":"5","ratio":"16:9"}', 'application/json'),
    # Try query param approach
    ('vid_query', 'POST', vid_url + '?model=Kling 1.0&prompt=a man', '{"prompt":"a man"}', 'application/json'),
    # Try different content types
    ('vid_text_plain', 'POST', vid_url, '{"model":"Kling 1.0","prompt":"a man walking"}', 'text/plain'),
    # Try with extra fields from common video gen APIs
    ('vid_fps', 'POST', vid_url, '{"model":"Kling 1.0","prompt":"a man walking","fps":"30","duration":"5","ratio":"16:9"}', 'application/json'),
    ('vid_seconds', 'POST', vid_url, '{"model":"Kling 1.0","prompt":"a man walking","seconds":"5","ratio":"16:9"}', 'application/json'),
    ('vid_time', 'POST', vid_url, '{"model":"Kling 1.0","prompt":"a man walking","time":"5s","ratio":"16:9"}', 'application/json'),
    # Try different ratio formats
    ('vid_ratio2', 'POST', vid_url, '{"model":"Kling 1.0","prompt":"a man walking","ratio":"16:9","duration":"5"}', 'application/json'),
    # Try with request_id
    ('vid_reqid', 'POST', vid_url, '{"model":"Kling 1.0","prompt":"a man walking","request_id":"test123","duration":"5","ratio":"16:9"}', 'application/json'),
]

for name, method, url, body, ctype in tests:
    status, result = call(method, url, body, ctype)
    print(name, '->', status, result[:100])
    print()