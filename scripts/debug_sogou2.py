import requests
from urllib.parse import quote
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# 测试搜狗微信文章搜索（type=2）而不是公众号搜索（type=1）
keyword = "乐城先行区"
url = f'https://weixin.sogou.com/weixin?type=2&query={quote(keyword)}&ie=utf8'
print(f"测试搜狗文章搜索: {url}")

try:
    resp = requests.get(url, headers=headers, timeout=10)
    print(f"状态码: {resp.status_code}, 长度: {len(resp.text)}")
    
    # 找mp.weixin.qq.com链接
    urls = re.findall(r'https?://mp\.weixin\.qq\.com/s[^\s"\'<>]+', resp.text)
    print(f"找到文章链接数: {len(urls)}")
    for u in urls[:5]:
        print(f"  {u}")
    
    # 打印中间部分
    if len(resp.text) > 1000:
        print(f"\n中间内容(1000-2000):")
        print(resp.text[1000:2000])
except Exception as e:
    print(f"错误: {e}")

# 测试搜狗微信搜索的完整结果页面
print("\n\n尝试获取搜狗搜索完整结果...")
url2 = f'https://weixin.sogou.com/weixin?type=1&s_from=input&query={quote(keyword)}&ie=utf8&_sug_=n&_sug_type_='
try:
    resp = requests.get(url2, headers=headers, timeout=10)
    print(f"状态码: {resp.status_code}, 长度: {len(resp.text)}")
    
    # 查看script标签中的数据
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', resp.text, re.DOTALL)
    for i, s in enumerate(scripts[:3]):
        if 'mp.weixin' in s or 'biz' in s or 'url' in s:
            print(f"\nScript {i}: {s[:500]}")
except Exception as e:
    print(f"错误: {e}")
