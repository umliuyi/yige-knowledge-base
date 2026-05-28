import urllib.request, json, time, hashlib, hmac, base64

ak = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
sk = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
ts = str(int(time.time()))

body_img = '{"model":" Kling 1.0","prompt":"a beautiful landscape"}'

def call(url, headers, body):
    req = urllib.request.Request(url, data=body.encode(), headers=headers, method='POST')
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.status, resp.read().decode()[:300]
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)[:80]
        return 'err', err

url = 'https://api.klingai.com/v1/images/generations'

# Key insight: What if X-Access-Key value should be just the raw key,
# and X-Signature should be HMAC of (ts + body) using secret key as key?
# But Secret Key in Kling might actually be a raw secret (not an HMAC key)

# Test: Try different Authorization header values
auth_tests = [
    (ak, 'X-Access-Key: ' + ak),  # plain key
    ('Bearer ' + ak, 'X-Access-Key: ' + ak),  # standard Bearer
    (ak, 'X-Api-Key: ' + ak),  # different header name
    ('Bearer ' + ak, 'X-Api-Key: ' + ak),
]

# Signature using body-only HMAC
sig = base64.b64encode(hmac.new(sk.encode(), body_img.encode(), hashlib.sha256).digest()).decode()

for auth_val, key_hdr in auth_tests:
    h = {
        'Authorization': auth_val,
        key_hdr: ak,
        'X-Signature': sig,
        'X-Timestamp': ts,
        'Content-Type': 'application/json'
    }
    status, result = call(url, h, body_img)
    print('Auth=' + auth_val[:20] + ' KeyHdr=' + key_hdr[:20], '->', status, result[:80])
    print()

# Now test: what if the body is NOT included in signature?
sig_no_body = base64.b64encode(hmac.new(sk.encode(), ts.encode(), hashlib.sha256).digest()).decode()
h = {
    'Authorization': 'Bearer ' + ak,
    'X-Access-Key': ak,
    'X-Signature': sig_no_body,
    'X-Timestamp': ts,
    'Content-Type': 'application/json'
}
status, result = call(url, h, body_img)
print('Sig_no_body ->', status, result[:80])