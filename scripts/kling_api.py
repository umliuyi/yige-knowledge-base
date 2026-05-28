import urllib.request, json, time, hashlib, hmac

ak = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
sk = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'

def make_headers(body):
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

# Try the exact model names from Kling's UI (not from screenshot)
# Model might be "Kling" not "Kling 1.0"  
body_img_tests = [
    '{"model":"Kling","prompt":"a cat"}',
    '{"model":"Kling 1","prompt":"a cat"}',
    '{"model":"Kling-pro","prompt":"a cat"}',
    '{"model":"Kling1.0","prompt":"a cat"}',
    '{"model_name":"Kling 1.0","prompt":"a cat"}',
    '{"model":"kling-1.0","prompt":"a cat"}',
    '{"model_id":"Kling 1.0","prompt":"a cat"}',
    '{"model":"Kling","text":"a cat"}',
]

print('=== IMAGE TESTS ===')
for body in body_img_tests:
    status, result = call('POST', 'https://api.klingai.com/v1/images/generations', body)
    print(body[:50], '->', status, result[:80])

print()
print('=== VIDEO TESTS ===')
body_vid_tests = [
    '{"model":"Kling","prompt":"a cat","duration":"5","ratio":"16:9"}',
    '{"model":"Kling 1","prompt":"a cat","duration":"5","ratio":"16:9"}',
    '{"model":"Kling-pro","prompt":"a cat","duration":"5","ratio":"16:9"}',
    '{"model":"Kling1.0","prompt":"a cat","duration":"5","ratio":"16:9"}',
]
for body in body_vid_tests:
    status, result = call('POST', 'https://api.klingai.com/v1/videos/generations', body)
    print(body[:50], '->', status, result[:80])