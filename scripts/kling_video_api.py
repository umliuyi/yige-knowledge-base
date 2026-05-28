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

def call(url, body):
    h = make_headers(body)
    try:
        req = urllib.request.Request(url, data=body.encode(), headers=h, method='POST')
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.status, resp.read().decode()[:500]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)
        return 'err', err[:200]

# KEY: try WITHOUT duration (the screenshot example didn't have duration)
# Also try different ratios and model names

# Image tests
img_url = 'https://api.klingai.com/v1/images/generations'
img_tests = [
    ('img_no_dur', '{"model":"Kling 1.0","prompt":"a girl on the beach","ratio":"16:9"}'),
    ('img_1x1', '{"model":"Kling 1.0","prompt":"a girl","ratio":"1:1"}'),
    ('img_9x16', '{"model":"Kling 1.0","prompt":"a girl","ratio":"9:16"}'),
    ('img_aspect', '{"model":"Kling 1.0","prompt":"a girl","aspect_ratio":"16:9"}'),
    ('img_size', '{"model":"Kling 1.0","prompt":"a girl","image_size":"1024x1024"}'),
]

# Video tests
vid_url = 'https://api.klingai.com/v1/videos/generations'
vid_tests = [
    ('vid_no_dur', '{"model":"Kling 1.0","prompt":"a girl on the beach","ratio":"16:9"}'),
    ('vid_9x16', '{"model":"Kling 1.0","prompt":"a girl walking","ratio":"9:16"}'),
    ('vid_1x1', '{"model":"Kling 1.0","prompt":"a girl","ratio":"1:1"}'),
    ('vid_no_ratio', '{"model":"Kling 1.0","prompt":"a girl walking"}'),
    ('vid_nd_nor', '{"model":"Kling 1.0","prompt":"a girl walking on the beach"}'),
]

print('=== IMAGE TESTS ===')
for name, body in img_tests:
    status, result = call(img_url, body)
    print(name, '->', status, result[:100])

print()
print('=== VIDEO TESTS ===')
for name, body in vid_tests:
    status, result = call(vid_url, body)
    print(name, '->', status, result[:100])