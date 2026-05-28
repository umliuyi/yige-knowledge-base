# -*- coding: utf-8 -*-
"""
RSS源测试脚本 - 调研龙虾专用
测试各RSS源是否能正常访问，筛选出可用的订阅源
"""

import urllib.request
import urllib.error
import ssl
import time
from datetime import datetime

# 忽略SSL证书验证（部分自签证书站点需要）
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 待测试RSS源列表
RSS_SOURCES = [
    # 健康/医疗
    {"name": "36kr科技", "url": "https://36kr.com/feed", "category": "科技/创业"},
    {"name": "财新健康", "url": "https://feed.caixin.com/", "category": "财经/健康"},
    {"name": "丁香园", "url": "http://www.dxy.cn/rss/home.xml", "category": "医疗/健康"},
    {"name": "医学界", "url": "http://www.yxj.org.cn/rss.xml", "category": "医疗/健康"},
    
    # 政府/政策
    {"name": "药监局公告", "url": "http://www.nmpa.gov.cn/WS04/CL2042/", "category": "政府/药监"},
    {"name": "国家卫健委", "url": "http://www.nhc.gov.cn/wjw/gwswjhylst/rss.xml", "category": "政府/卫生"},
    
    # 地方/海南
    {"name": "海南日报", "url": "https://hnrb.hinews.cn/rss.php", "category": "地方/海南"},
    {"name": "南海网", "url": "http://www.hinews.cn/rss.php", "category": "地方/海南"},
    
    # 行业媒体
    {"name": "动脉网", "url": "https://vcbeat.top/Rss/News", "category": "医疗/创投"},
    {"name": "八点健康闻", "url": "https://www.8点健康.com/rss", "category": "医疗/评论"},
    {"name": "健康界", "url": "https://www.cn-healthcare.com/rss/", "category": "医疗/资讯"},
    
    # 财经/综合
    {"name": "第一财经", "url": "https://www.yicai.com/rss/news.xml", "category": "财经"},
    {"name": "新浪财经", "url": "https://rss.sina.com.cn/news/marquee.xml", "category": "财经"},
    {"name": "腾讯财经", "url": "https://feed.aifinance.cn/", "category": "财经"},
    
    # 乐城相关
    {"name": "乐城先行区官网", "url": "http://www.lecheng.gov.cn/rss.xml", "category": "乐城"},
    {"name": "海南省医保局", "url": "http://hnyb.hetr.gov.cn/rss.xml", "category": "海南/医保"},
]

def test_rss_source(source):
    """测试单个RSS源"""
    name = source["name"]
    url = source["url"]
    category = source["category"]
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/rss+xml, application/xml, text/xml, */*',
            }
        )
        
        start_time = time.time()
        response = urllib.request.urlopen(req, timeout=10, context=ctx)
        elapsed = (time.time() - start_time) * 1000  # 毫秒
        
        content_length = response.headers.get('Content-Length', 'unknown')
        content_type = response.headers.get('Content-Type', 'unknown')
        raw_content = response.read(5000)  # 只读前5KB看结构
        response.close()
        
        # 检查是否包含RSS/Atom特征
        raw_str = raw_content.decode('utf-8', errors='ignore').lower()
        is_rss = any(tag in raw_str for tag in ['<rss', '<feed', '<xml'])
        
        return {
            "name": name,
            "url": url,
            "category": category,
            "status": "✅ 可用",
            "elapsed_ms": round(elapsed, 0),
            "content_length": content_length,
            "content_type": content_type,
            "is_rss": is_rss,
            "error": None,
            "notes": "RSS结构正常" if is_rss else "可能不是标准RSS"
        }
        
    except urllib.error.HTTPError as e:
        return {
            "name": name,
            "url": url,
            "category": category,
            "status": "⚠️ HTTP错误",
            "elapsed_ms": None,
            "content_length": None,
            "content_type": None,
            "is_rss": False,
            "error": f"HTTP {e.code}: {e.reason}",
            "notes": None
        }
    except urllib.error.URLError as e:
        return {
            "name": name,
            "url": url,
            "category": category,
            "status": "❌ 无法访问",
            "elapsed_ms": None,
            "content_length": None,
            "content_type": None,
            "is_rss": False,
            "error": str(e.reason),
            "notes": "可能被墙或URL不存在" if "timed out" in str(e) else "网络错误"
        }
    except Exception as e:
        return {
            "name": name,
            "url": url,
            "category": category,
            "status": "❌ 错误",
            "elapsed_ms": None,
            "content_length": None,
            "content_type": None,
            "is_rss": False,
            "error": str(e),
            "notes": None
        }

def main():
    print("=" * 60)
    print("RSS源测试脚本 - 调研龙虾专用")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    results = []
    for source in RSS_SOURCES:
        print(f"测试: {source['name']} ({source['url']}) ... ", end="", flush=True)
        result = test_rss_source(source)
        results.append(result)
        print(result["status"])
        time.sleep(0.5)  # 避免请求过快
    
    print()
    print("=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    available = [r for r in results if "✅" in r["status"]]
    warning = [r for r in results if "⚠️" in r["status"]]
    unavailable = [r for r in results if "❌" in r["status"]]
    
    print(f"\n✅ 可用源 ({len(available)}个):")
    for r in available:
        print(f"  - {r['name']} [{r['category']}] - {r['elapsed_ms']}ms")
    
    if warning:
        print(f"\n⚠️ 警告源 ({len(warning)}个):")
        for r in warning:
            print(f"  - {r['name']}: {r['error']}")
    
    if unavailable:
        print(f"\n❌ 不可用源 ({len(unavailable)}个):")
        for r in unavailable:
            print(f"  - {r['name']}: {r['error']}")
    
    print()
    print("=" * 60)
    print("推荐使用的RSS源（用于调研龙虾）")
    print("=" * 60)
    
    recommended = [r for r in results if "✅" in r["status"]]
    
    print("""
# 【推荐】调研龙虾RSS订阅源配置
# 使用 feedparser 库解析，或用 requests + re 解析XML

RSS_SOURCES = [
""")
    
    for r in recommended:
        print(f"    # {r['category']}")
        print(f"    \"{r['name']}\": \"{r['url']}\",")
        print()
    
    print("]")

if __name__ == "__main__":
    main()