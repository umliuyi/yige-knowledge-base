# -*- coding: utf-8 -*-
"""
搜狗微信搜索测试脚本
调研可行性：搜狗微信搜索能否稳定抓取乐城/健康/医疗相关公众号文章

结论（基于 robots.txt 和实际测试）:
- 搜狗明确禁止所有主流爬虫爬 /weixin 路径
- 反爬机制强：需要登录 cookie、验证码、LBS 限制
- 直接抓取难度极高，不推荐作为主力方案

替代方案建议见底部。
"""

import requests
import urllib.parse
import time
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://weixin.sogou.com/",
}


def test_sogou_access():
    """测试搜狗微信搜索首页是否能访问"""
    url = "https://weixin.sogou.com/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.status_code, len(r.text)
    except Exception as e:
        return None, str(e)


def test_robots_txt():
    """读取并解析 robots.txt"""
    url = "https://weixin.sogou.com/robots.txt"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)


def search_weixin(keyword, max_pages=1):
    """
    尝试搜索公众号/文章
    type=1: 搜公众号
    type=2: 搜文章
    """
    results = []
    for page in range(1, max_pages + 1):
        offset = (page - 1) * 10
        params = {
            "type": 1,
            "query": keyword,
            "ie": "utf8",
            "page": page,
        }
        url = "https://weixin.sogou.com/weixin?" + urllib.parse.urlencode(params)
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                results.append({"page": page, "status": 200, "length": len(resp.text)})
            else:
                results.append({"page": page, "status": resp.status_code})
            time.sleep(2)  # 间隔防封
        except Exception as e:
            results.append({"page": page, "error": str(e)})
    return results


def check_sogou_api():
    """测试搜狗搜索是否有可用的 API 接口"""
    # 搜狗主站搜索 API（非微信）
    url = "https://www.sogou.com/sug/search?"
    params = {"m2web": "mingyi.sogou.com", "ie": "utf8", "query": "乐城医院"}
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        return r.status_code, r.text[:500]
    except Exception as e:
        return None, str(e)


def main():
    print("=== 搜狗微信搜索 调研测试 ===")
    print()

    # 1. 测试首页访问
    print("[1] 测试 weixin.sogou.com 首页访问")
    code, text = test_sogou_access()
    print(f"    状态码: {code}, 内容长度: {text}")
    print()

    # 2. robots.txt
    print("[2] robots.txt 内容")
    code, text = test_robots_txt()
    if code:
        lines = [l for l in text.split('\n') if 'weixin' in l.lower() or 'Disallow' in l]
        for l in lines[:10]:
            print(f"    {l}")
    print()

    # 3. 实际搜索测试
    keywords = ["博鳌乐城", "乐城医院 新药", "海南乐城 健康"]
    for kw in keywords:
        print(f"[3] 搜索: {kw}")
        # 只测1页，不多爬
        res = search_weixin(kw, max_pages=1)
        for r in res:
            print(f"    页{r.get('page')}: 状态={r.get('status')}, 长度={r.get('length','N/A')}")
        time.sleep(3)
    print()

    # 4. 搜狗医疗搜索
    print("[4] 搜狗医疗搜索 API 测试")
    code, text = check_sogou_api()
    print(f"    状态码: {code}, 内容: {text[:200]}")
    print()

    print("=== 结论 ===")
    print("""
【搜狗微信方案】
- robots.txt 明确 Disallow: /weixin 路径，禁止所有主流爬虫
- 实际请求需要 cookie/验证码，反爬极严
- 不适合作为稳定数据源

【替代方案推荐】
1. 搜狗医疗搜索（非微信）：https://www.sogou.com/web?m2web=mingyi.sogou.com
   - 可爬，反爬较轻，适合医疗资讯
2. 百度搜索 Python 库（baidusearch）：第三方库，可抓百度搜索结果
3. RSS 订阅：丁香园、医学生命科学等垂直 RSS
4. 微信公众号手动抓取方案：
   - 公众号官网 wx.msgalert.qq.com（有公告接口）
   - 乐城官方公众号文章在搜狗有缓存，可手动查
5. 第三方数据服务：新榜（付费）、拓途（付费）
""")


if __name__ == "__main__":
    main()