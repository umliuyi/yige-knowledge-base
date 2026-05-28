import urllib.request, json, time, hashlib, hmac

ak = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
sk = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'

def make_headers(body=''):
    ts = str(int(time.time()))
    # CORRECT: Hex(HMAC-SHA256(SecretKey, Timestamp + Body))
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
        req = urllib.request.Request(url, data=body.encode('utf-8'), headers=h, method='POST')
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.status, resp.read().decode()[:500]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)
        return 'err', err[:200]

# From the screenshot, the image generation example shows:
# model="Kling 1.0" (with space)
# prompt="..."  
# Let's try exactly what the screenshot shows for IMAGE first

img_url = 'https://api.klingai.com/v1/images/generations'
vid_url = 'https://api.klingai.com/v1/videos/generations'

# Image tests - match exact format from screenshot
img_tests = [
    ('img_screenshot_fmt', '{"model":"Kling 1.0","prompt":"A running horse"}'),
    ('img_simple', '{"model":"Kling 1.0","prompt":"A cat"}'),
]

# Video tests - from the video API section of the docs
vid_tests = [
    ('vid_model_kling', '{"model":"Kling 1.0","prompt":"A horse running on the beach"}'),
    ('vid_neg', '{"model":"Kling 1.0","prompt":"A horse running","negative_prompt":""}'),
    ('vid_no_neg', '{"model":"Kling 1.0","prompt":"A horse running"}'),
    ('vid_with_space', '{"model":"Kling 1.0","prompt":"A man walking on the beach","duration":"5","ratio":"16:9"}'),
    ('vid_style', '{"model":"Kling 1.0","prompt":"A man","duration":"5","ratio":"16:9","style":"video"}'),
    ('vid_nd', '{"model":"Kling 1.0","prompt":"A man walking on the beach"}'),
]

print('=== IMAGE TESTS ===')
for name, body in img_tests:
    status, result = call(img_url, body)
    print(name, '->', status, result[:120])
    print()

print('=== VIDEO TESTS ===')
for name, body in vid_tests:
    status, result = call(vid_url, body)
    print(name, '->', status, result[:120])
    print()