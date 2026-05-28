import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://mp.weixin.qq.com/',
}

# 尝试通过搜狗搜索找到乐城先行区的公众号主页URL
# type=1 搜索公众号，type=2 搜索文章
# 需要提取结果中的 biz 参数

# 方法：通过搜狗搜索，找到目标公众号的主页，然后提取biz
search_url = f'https://weixin.sogou.com/weixin?type=1&query=%E4%B9%90%E5%9F%8E%E5%85%88%E8%A1%8C%E5%8C%BA&ie=utf8'

session = requests.Session()
resp = session.get(search_url, headers=headers, timeout=10)

print(f"状态码: {resp.status_code}")
print(f"内容长度: {len(resp.text)}")

# 搜狗微信页面通常是GBK编码，但API返回UTF-8
# 查看内容中是否有有用的信息
if resp.apparent_encoding:
    try:
        resp.encoding = resp.apparent_encoding
    except:
        resp.encoding = 'utf-8'

text = resp.text

# 查找可能包含的公众号信息
# 搜狗的结果通常在 script 标签的变量中
print("\n查找JSON数据...")
# 查找 var appmsg 相关内容
appmsgs = re.findall(r'appmsg[^;]+', text)
print(f"找到appmsg相关: {len(appmsgs)}")
for a in appmsgs[:3]:
    print(f"  {a[:100]}")

# 查找 biz 相关内容
bizs = re.findall(r'biz[^;"]+', text)
print(f"\n找到biz相关: {len(bizs)}")
for b in bizs[:5]:
    print(f"  {b[:100]}")

# 查找 url 相关内容
urls = re.findall(r'url[^;"]+', text)
print(f"\n找到url相关: {len(urls)}")
for u in urls[:5]:
    print(f"  {u[:100]}")

# 检查是否是反爬页面
if '验证码' in text or '验证' in text:
    print("\n⚠️ 可能需要验证码")
