import jwt, time, urllib.request, json

ak = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
sk = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'

# Generate JWT
payload = {
    "iss": ak,
    "exp": int(time.time()) + 1800,
    "nbf": int(time.time()) - 5
}
token = jwt.encode(payload, sk, algorithm="HS256")
print("JWT:", token[:30], "...")
print("Len:", len(token))

h = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
}

# CORRECT BASE URL
base = "https://api-beijing.klingai.com"

def call(url, body):
    req = urllib.request.Request(url, data=body.encode(), headers=h, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.status, resp.read().decode()[:500]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)
        return 'err', err[:300]

# Image tests
img_url = base + "/v1/images/generations"
img_tests = [
    ('img_simple', '{"model":"Kling 1.0","prompt":"A running horse"}'),
    ('img_cat', '{"model":"Kling 1.0","prompt":"A cat"}'),
    ('img_no_model', '{"prompt":"A cat"}'),
]

# Video tests
vid_url = base + "/v1/videos/generations"
vid_tests = [
    ('vid_simple', '{"model":"Kling 1.0","prompt":"A horse running on the beach"}'),
    ('vid_cat', '{"model":"Kling 1.0","prompt":"A cat running"}'),
    ('vid_no_model', '{"prompt":"A horse running"}'),
]

print()
print("=== IMAGE TESTS ===")
for name, body in img_tests:
    status, result = call(img_url, body)
    print(name, "->", status, result[:150])
    print()

print("=== VIDEO TESTS ===")
for name, body in vid_tests:
    status, result = call(vid_url, body)
    print(name, "->", status, result[:150])
    print()