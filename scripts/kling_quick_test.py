import jwt, time, urllib.request, json

AK = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
SK = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
BASE = 'https://api-beijing.klingai.com'

# Generate JWT
ts = str(int(time.time()))
payload = {'iss': AK, 'exp': int(ts) + 1800, 'nbf': int(ts) - 5}
try:
    token = jwt.encode(payload, SK, algorithm='HS256')
    print('Token OK:', token[:30])
except Exception as e:
    print('JWT Error:', e)

# Test create video task
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

h = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
body = json.dumps({
    'model_name': 'kling-v2-6',
    'prompt': 'A cute rabbit wearing glasses, sitting at a desk, reading a newspaper',
    'duration': '5',
    'mode': 'pro',
    'aspect_ratio': '1:1'
})

url = BASE + '/v1/videos/text2video'
req = urllib.request.Request(url, data=body.encode(), headers=h, method='POST')
try:
    resp = urllib.request.urlopen(req, timeout=30, context=ctx)
    result = json.loads(resp.read().decode())
    print('Status:', resp.status)
    print('Response:', json.dumps(result, ensure_ascii=False)[:300])
except Exception as e:
    try:
        err_body = e.read().decode()
        print('Error:', err_body[:200])
    except:
        print('Error:', str(e)[:100])
