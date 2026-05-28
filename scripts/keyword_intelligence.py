#!/usr/bin/env python3
"""
每日关键词情报监控
每天6:00自动跑，搜索核心关键词的当日新闻
输出到情报文件，供调研龙虾使用
"""
import urllib.request
import re
import time
import os
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206"
KEYWORDS = [
    "乐城先行区",
    "博鳌乐城",
    "细胞治疗",
    "免疫治疗",
    "干细胞新药",
    "CAR-T",
    "ADC抗体偶联",
    "NMPA审批",
    "海南大健康",
]

HEALTH_KW = [
    "乐城", "医疗", "健康", "癌症", "肿瘤", "干细胞",
    "免疫", "CAR-T", "ADC", "新药", "NMPA", "审批"
]

def fetch_36kr():
    """抓36kr RSS，返回健康相关条目"""
    try:
        url = 'https://36kr.com/feed'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw = resp.read()
        # 36kr returns GBK encoding
        content = raw.decode('gbk', errors='ignore')
        items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
        results = []
        for it in items:
            t_m = re.search(r'<title>(.*?)</title>', it, re.DOTALL)
            l_m = re.search(r'<link><!\[CDATA\[(https://36kr.com/.*?)\]\]></link>', it, re.DOTALL)
            d_m = re.search(r'<pubDate>(.*?)</pubDate>', it, re.DOTALL)
            if t_m:
                title = t_m.group(1).strip()
                link = l_m.group(1).strip() if l_m else ''
                date = d_m.group(1).strip() if d_m else ''
                if any(k in title for k in HEALTH_KW):
                    results.append((title, link, date))
        return results[:10]
    except Exception as e:
        return []

def fetch_dxy(query):
    """抓丁香园搜索页"""
    try:
        encoded_q = urllib.parse.quote(query)
        url = f'https://www.dxy.cn/search?query={encoded_q}&type=news'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
        # Extract titles from search results
        titles = re.findall(r'target="_blank"[^>]*>([^<]{5,60})</a>', content)
        links = re.findall(r'href="(https://www\.dxy\.cn/[^"]+)"', content)
        return [(t.strip(), l, '') for t, l in zip(titles[:5], links[:5]) if any(k in t for k in HEALTH_KW)]
    except:
        return []

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_file = os.path.join(OUTPUT_DIR, "intelligence", f"{TODAY}.md")
    os.makedirs(os.path.join(OUTPUT_DIR, "intelligence"), exist_ok=True)

    lines = [f"# 每日关键词情报 | {TODAY}\n\n"]

    # 抓36kr
    t0 = time.time()
    results_36kr = fetch_36kr()
    elapsed_36kr = int((time.time() - t0) * 1000)

    if results_36kr:
        lines.append(f"## 36kr RSS ({elapsed_36kr}ms)\n")
        for title, link, date in results_36kr:
            lines.append(f"- [{title}]({link})\n")
            if date:
                lines.append(f"  日期: {date}\n")
        lines.append(f"\n共找到 {len(results_36kr)} 条健康相关内容\n\n")
    else:
        lines.append(f"## 36kr RSS: 无结果或失败\n\n")

    # 抓丁香园关键词
    for kw in KEYWORDS[:5]:
        t0 = time.time()
        results_dxy = fetch_dxy(kw)
        elapsed = int((time.time() - t0) * 1000)
        if results_dxy:
            lines.append(f"## 丁香园搜索: {kw} ({elapsed}ms)\n")
            for title, link, _ in results_dxy[:5]:
                lines.append(f"- [{title}]({link})\n")
            lines.append("\n")

    lines.append(f"\n*生成时间: {TODAY}*\n")

    with open(out_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"[OK] 情报已写入: {out_file}")
    print(f"36kr: {len(results_36kr)} 条")
    return out_file

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        TODAY = sys.argv[1]
    main()