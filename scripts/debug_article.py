import requests
import re

# 测试直接抓取微信公众号文章
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# 测试几篇已知文章
test_urls = [
    "https://mp.weixin.qq.com/s/abc123",  # 通用格式测试
]

# 实际测试 - 尝试获取文章内容
article_url = "https://mp.weixin.qq.com/s/n0BJPD-bsH9IYgNCI-rJ-A"
print(f"测试URL: {article_url}")

try:
    resp = requests.get(article_url, headers=headers, timeout=10)
    print(f"状态码: {resp.status_code}")
    
    if resp.status_code == 200:
        # 提取标题
        title = re.search(r'<title>([^<]+)</title>', resp.text)
        if title:
            print(f"标题: {title.group(1)}")
        
        # 检查是否需要授权
        if "环境异常" in resp.text:
            print("⚠️ 环境异常，需要微信授权")
        elif "验证环境" in resp.text:
            print("⚠️ 需要验证环境")
        elif "겜焰煵쒑" in resp.text or "验证" in resp.text:
            print("⚠️ 可能需要验证")
        else:
            print(f"✓ 内容获取成功，长度: {len(resp.text)}")
            # 打印部分内容
            print("\n前500字符:")
            print(resp.text[:500])
    else:
        print(f"响应: {resp.text[:500]}")
except Exception as e:
    print(f"错误: {e}")

# 测试搜索RSSHub备用地址
print("\n\n测试RSSHub备用:")
rsshub_urls = [
    "https://rsshub.app/weixin/mp.bizplaceholder",
]
for url in rsshub_urls:
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        print(f"{url}: {resp.status_code}")
    except Exception as e:
        print(f"{url}: 错误 - {e}")
