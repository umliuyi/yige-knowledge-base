import requests
from urllib.parse import quote

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

keyword = "乐城先行区"
url = f'https://weixin.sogou.com/weixin?type=1&query={quote(keyword)}&ie=utf8'
resp = requests.get(url, headers=headers, timeout=10)
print('状态码:', resp.status_code)
print('内容长度:', len(resp.text))
print('内容末尾2000字符:')
print(resp.text[-2000:])
