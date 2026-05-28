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
print("JWT len:", len(token))

# Call API with JWT only (no X-Access-Key)
h_jwt_only = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
}

# Call with JWT + X-Access-Key
h_both = {
    "Authorization": "Bearer " + token,
    "X-Access-Key": ak,
    "Content-Type": "application/json"
}

img_url = "https://api.klingai.com/v1/images/generations"
vid_url = "https://api.klingai.com/v1/videos/generations"

def do(url, body, headers):
    req = urllib.request.Request(url, data=body.encode(), headers=headers, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.status, resp.read().decode()[:300]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)
        return 'err', err[:200]

tests = [
    ('img_jwt_only', img_url, '{"model":"Kling 1.0","prompt":"A running horse"}', h_jwt_only),
    ('vid_jwt_only', vid_url, '{"model":"Kling 1.0","prompt":"A horse running on the beach"}', h_jwt_only),
    ('img_jwt_both', img_url, '{"model":"Kling 1.0","prompt":"A running horse"}', h_both),
    ('vid_jwt_both', vid_url, '{"model":"Kling 1.0","prompt":"A horse running on the beach"}', h_both),
    ('img_jwt_simple', img_url, '{"model":"Kling 1.0","prompt":"A cat"}', h_jwt_only),
    ('vid_jwt_simple', vid_url, '{"model":"Kling 1.0","prompt":"A cat"}', h_jwt_only),
]

for name, url, body, h in tests:
    status, result = do(url, body, h)
    print(name, '->', status, result[:100])