import jwt, time, urllib.request, json

ak = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
sk = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'

payload = {
    "iss": ak,
    "exp": int(time.time()) + 1800,
    "nbf": int(time.time()) - 5
}
token = jwt.encode(payload, sk, algorithm="HS256")

h = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
}

base = "https://api-beijing.klingai.com"

def call(url, body):
    req = urllib.request.Request(url, data=body.encode(), headers=h, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.status, resp.read().decode()[:500]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)
        return 'err', err[:300]

# Image works (1102 = balance issue). Try video different URLs.
video_paths = [
    '/v1/video/generations',
    '/v1/videos/generate',
    '/v1/video/create',
    '/v1/videos/create',
    '/v1/video/generation',
    '/v1/videos/generation',
    '/v1/videos',
    '/v1/video',
    '/v1/t2v/generations',
    '/v1/i2v/generations',
    '/v1/aitube/videos',
]
body_vid = '{"model":"Kling 1.0","prompt":"A horse running"}'

print("=== VIDEO URL VARIATIONS ===")
for path in video_paths:
    url = base + path
    status, result = call(url, body_vid)
    print(path, "->", status, result[:100])

# Also try image variations to confirm 1102
img_paths = [
    '/v1/images/generations',
    '/v1/image/generations',
    '/v1/images/generate',
    '/v1/img/generations',
]
body_img = '{"model":"Kling 1.0","prompt":"A horse"}'

print()
print("=== IMAGE URL VARIATIONS ===")
for path in img_paths:
    url = base + path
    status, result = call(url, body_img)
    print(path, "->", status, result[:100])