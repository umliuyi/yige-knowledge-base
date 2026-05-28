import urllib.request, json, time, hashlib, hmac, base64
ak = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
sk = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
ts = str(int(time.time()))

body = '{"prompt":"landscape"}'

# Kuaishou/Kling might use: sign = MD5(secret_key + timestamp)
for name, body_content in [
    ('body1', '{"prompt":"landscape"}'),
    ('body2', '{"image_size":"1024x1024","model":" Kling 1.0","prompt":"landscape"}'),
]:
    sig = hashlib.md5((sk + ts).encode()).hexdigest()
    h = {'Authorization': 'Bearer ' + ak, 'X-Access-Key': ak, 'X-Signature': sig, 'X-Timestamp': ts, 'Content-Type': 'application/json'}
    url = 'https://api.klingai.com/v1/images/generations'
    req = urllib.request.Request(url, data=body_content.encode(), headers=h, method='POST')
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        print(name, '->', resp.status, resp.read().decode()[:100])
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)[:80]
        print(name, '->', err[:100])