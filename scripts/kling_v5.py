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
            req = urllib.request.Request(url, data=body.encode('utf-8'), headers=h, method='POST')
        else:
            req = urllib.request.Request(url, headers=h, method='GET')
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.status, resp.read().decode()[:500]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)
        return 'err', err[:200]

# Try every variation of the video URL
vid_tests = [
    '/v1/videos/generations',
    '/v1/video/generations', 
    '/v1/v1/video/generations',
    '/v1/videos/generation',
    '/v1/video/generation',
    '/api/v1/videos/generations',
    '/api/v1/video/generations',
]

body = '{"model":"Kling 1.0","prompt":"a man walking","duration":"5","ratio":"16:9"}'
base = 'https://api.klingai.com'

print('=== VIDEO URL VARIATIONS ===')
for path in vid_tests:
    url = base + path
    status, result = call('POST', url, body)
    print(path, '->', status, result[:80])

# Also try different image URLs
img_tests = [
    '/v1/images/generations',
    '/v1/image/generations',
    '/v1/img/generations',
]
body_img = '{"model":"Kling 1.0","prompt":"a cat"}'

print()
print('=== IMAGE URL VARIATIONS ===')
for path in img_tests:
    url = base + path
    status, result = call('POST', url, body_img)
    print(path, '->', status, result[:80])