import urllib.request, json, time

ak = 'ATQYNGHDEYeKhJgKKTmeh3yMpHRnfQrT'
sk = '8HaCmCpGMCTYNJEhgBmhCKKykJbDf4b9'
ts = str(int(time.time()))
body = '{"prompt":"a beautiful landscape"}'

# Try X-Access-Key only (no signature) for POST
headers = {'X-Access-Key': ak, 'Content-Type': 'application/json'}
url = 'https://api.klingai.com/v1/images/generations'
req = urllib.request.Request(url, data=body.encode(), headers=headers, method='POST')
try:
    resp = urllib.request.urlopen(req, timeout=10)
    print('X-Access-Key only ->', resp.status, resp.read().decode()[:200])
except Exception as e:
    err = e.read().decode() if hasattr(e, 'read') else str(e)[:60]
    print('X-Access-Key only ->', err[:100])

# Try different base URLs
for base in ['https://api.klingai.com', 'https://api-sg.klingai.com', 'https://api-prod.klingai.com', 'https://api-v2.klingai.com']:
    url = base + '/v1/user/info'
    headers = {'Authorization': f'Bearer {ak}', 'Content-Type': 'application/json'}
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=8)
        print(base, '->', resp.status, resp.read().decode()[:100])
    except Exception as e:
        print(base, '->', str(e)[:60])