"""
测试搜狗微信搜索能否获取公众号文章URL列表
"""
import requests
import re
import json
from urllib.parse import quote

# 搜索关键字
keywords = ["乐城先行区", "博鳌乐城", "乐城医院"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://weixin.sogou.com/",
}

def test_sogou_search(keyword):
    """测试搜狗微信搜索"""
    print(f"\n{'='*60}")
    print(f"测试搜狗微信搜索: {keyword}")
    print('='*60)
    
    url = f"https://weixin.sogou.com/weixin?type=1&query={quote(keyword)}&ie=utf8"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        print(f"状态码: {response.status_code}")
        print(f"内容长度: {len(response.text)}")
        
        # 尝试提取文章URL
        # 搜狗微信搜索结果中的公众号文章链接格式
        urls = re.findall(r'https?://mp\.weixin\.qq\.com/s[^\s"\'<>]+', response.text)
        print(f"找到 mp.weixin.qq.com 链接数: {len(urls)}")
        
        if urls:
            for i, u in enumerate(urls[:5]):
                print(f"  URL {i+1}: {u}")
        
        # 尝试提取公众号名称
        names = re.findall(r'class="tit\w?[^"]*">([^<]+)</p>', response.text)
        if names:
            print(f"找到公众号名: {names[:3]}")
        
        # 打印部分HTML以便调试
        if len(response.text) < 2000:
            print("\n完整内容:")
            print(response.text[:2000])
        else:
            # 查找关键位置
            if "验证码" in response.text or "请输入验证码" in response.text:
                print("⚠️ 被要求输入验证码！")
            elif "访问过于频繁" in response.text:
                print("⚠️ 访问被限制，过于频繁！")
            else:
                print(f"\n内容中间部分 (500-1500字符):")
                print(response.text[500:1500])
                
        return response.text
        
    except Exception as e:
        print(f"错误: {e}")
        return None

def test_rsshub(keyword=""):
    """测试RSSHub微信公众号RSS"""
    print(f"\n{'='*60}")
    print(f"测试RSSHub")
    print('='*60)
    
    # RSSHub的微信订阅路由
    # 注意：RSSHub需要部署才能使用，这里测试官方公共服务
    test_urls = [
        f"https://rsshub.app/weixin/mp.bizplaceholder",  # 需要真实的biz
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"URL: {url}")
            print(f"状态码: {response.status_code}")
            print(f"内容: {response.text[:500]}")
        except Exception as e:
            print(f"错误 {url}: {e}")

def test_direct_article_fetch():
    """测试直接抓取微信公众号文章"""
    print(f"\n{'='*60}")
    print(f"测试直接抓取公众号文章")
    print('='*60)
    
    # 测试一篇已知文章
    test_urls = [
        "https://mp.weixin.qq.com/s/n0BJPD-bsH9IYgNCI-rJ-A",  # 示例文章
    ]
    
    article_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    
    for url in test_urls:
        try:
            response = requests.get(url, headers=article_headers, timeout=10)
            print(f"URL: {url}")
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                # 尝试提取标题
                title_match = re.search(r'<title>([^<]+)</title>', response.text)
                if title_match:
                    print(f"标题: {title_match.group(1)}")
                
                # 检查是否被重定向到授权页面
                if "还需要确认" in response.text or "验证环境" in response.text:
                    print("⚠️ 需要微信授权验证")
                elif len(response.text) > 10000:
                    print(f"✓ 成功获取内容，长度: {len(response.text)}")
                else:
                    print(f"内容过短，可能被拦截")
            else:
                print(f"响应: {response.text[:200]}")
                
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    print("="*60)
    print("微信公众号监控 - 测试脚本")
    print("="*60)
    
    # 测试各个方案
    for kw in keywords:
        test_sogou_search(kw)
    
    test_rsshub()
    test_direct_article_fetch()
    
    print("\n" + "="*60)
    print("测试完成")
    print("="*60)
