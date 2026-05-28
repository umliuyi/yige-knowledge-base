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

def call(url, body):
    h = make_headers(body)
    try:
        req = urllib.request.Request(url, data=body.encode('utf-8'), headers=h, method='POST')
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.status, resp.read().decode()[:500]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)
        return 'err', err[:200]

vid_url = 'https://api.klingai.com/v1/videos/generations'

# Try with MINIMAL body - literally just prompt
tests = [
    ('prompt_only', '{"prompt":"a man walking"}'),
    ('empty', '{}'),
    ('null_model', '{"model":null,"prompt":"a man walking"}'),
    ('empty_model', '{"model":"","prompt":"a man walking"}'),
    ('wrong_model', '{"model":"invalid-model","prompt":"a man walking"}'),
    ('algo_field', '{"model":"Kling 1.0","algo":"kling","prompt":"a man walking"}'),
    ('algo2', '{"model":"Kling 1.0","algo":"kling-video","prompt":"a man walking"}'),
    ('version', '{"model":"Kling 1.0","version":"v1","prompt":"a man walking"}'),
    ('mode', '{"model":"Kling 1.0","mode":"fast","prompt":"a man walking"}'),
    ('type', '{"model":"Kling 1.0","type":"text2video","prompt":"a man walking"}'),
    ('extra_version', '{"model":"Kling 1.0","api_version":"v1","prompt":"a man walking"}'),
]

for name, body in tests:
    status, result = call(vid_url, body)
    print(name, '->', status, result[:100])
    print()