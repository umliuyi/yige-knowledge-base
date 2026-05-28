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
        'Content-Type': 'application/json; charset=utf-8'
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

tests = [
    # Try with extra fields
    ('extra_cinematic', '{"model":"Kling 1.0","prompt":"cinematic video of a man walking on the beach at sunset, professional camera movement","duration":"5","ratio":"16:9","cfg_scale":"7.5"}'),
    # Without model
    ('no_model', '{"prompt":"a man walking on the beach","duration":"5","ratio":"16:9"}'),
    # Different model format
    ('model_v1', '{"model":"Kling-v1.0","prompt":"a man walking","duration":"5","ratio":"16:9"}'),
    # Try negative_prompt
    ('neg', '{"model":"Kling 1.0","prompt":"a man walking","negative_prompt":"blurry, low quality","duration":"5","ratio":"16:9"}'),
    # Try step parameter
    ('steps', '{"model":"Kling 1.0","prompt":"a man walking","steps":"25","duration":"5","ratio":"16:9"}'),
    # Without spaces in model name
    ('modelnospace', '{"model":"Kling1.0","prompt":"a man walking","duration":"5","ratio":"16:9"}'),
    # With seed
    ('seed', '{"model":"Kling 1.0","prompt":"a man walking","seed":"12345","duration":"5","ratio":"16:9"}'),
]

for name, body in tests:
    status, result = call(vid_url, body)
    print(name, '->', status, result[:100])
    print()