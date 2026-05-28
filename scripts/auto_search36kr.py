#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""36kr RSS健康新闻采集脚本（扩展版：36kr为主+补充中文医学RSS）"""
import urllib.request
import urllib.parse
import re
import os
import ssl
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TODAY = datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206\raw"
HEALTH_KW = ["乐城", "医疗", "健康", "癌症", "肿瘤", "干细胞",
              "免疫", "CAR-T", "ADC", "新药", "NMPA", "审批",
              "腺岛", "糖尿病", "肺", "膝", "骨关节", "肝", "心", "NK细胞",
              "慢阻肺", "软骨", "膝盖", "间充质", "细胞治疗", "免疫治疗"]

os.makedirs(OUTPUT_DIR, exist_ok=True)

# 多RSS源配置：36kr + 补充健康源
RSS_SOURCES = [
    # 36kr主源（科技，但含健康内容）
    ("36kr", "https://36kr.com/feed", "gbk"),
    # 中华健康网（已验证有效的健康RSS）
    ("中华健康网", "https://www.cnk2009.com/rss", "utf-8"),
]

def fetch_rss(url, encoding="utf-8"):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        raw = resp.read()
    return raw.decode(encoding, errors="ignore")

def parse_items(content, source_name):
    items = re.findall(r"<item>(.*?)</item>", content, re.DOTALL)
    results = []
    for it in items:
        t_m = re.search(r"<title>(.*?)</title>", it, re.DOTALL)
        l_m = re.search(r"<link><!\[CDATA\[(.*?)\]\]></link>", it)
        if not l_m:
            l_m = re.search(r"<link>(https?://.*?)</link>", it)
        d_m = re.search(r"<pubDate>(.*?)</pubDate>", it)
        if t_m:
            title = t_m.group(1).strip()
            link = l_m.group(1).strip() if l_m else ""
            pubdate = d_m.group(1).strip() if d_m else ""
            results.append((title, link, pubdate, source_name))
    return results

def filter_health(items):
    filtered = []
    for title, link, pubdate, source in items:
        if any(kw in title for kw in HEALTH_KW):
            filtered.append((title, link, pubdate, source))
    return filtered

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始抓取RSS...")
    all_items = []
    for name, url, enc in RSS_SOURCES:
        try:
            content = fetch_rss(url, enc)
            items = parse_items(content, name)
            print(f"  [{name}] 总条目: {len(items)}")
            all_items.extend(items)
        except Exception as e:
            print(f"  [{name}] 抓取失败: {e}")
    health = filter_health(all_items)
    print(f"  健康相关: {len(health)}")

    out_file = os.path.join(OUTPUT_DIR, "36kr_results.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"# 健康新闻 | {TODAY}\n")
        f.write(f"# 来源: {', '.join([n for n,_,_ in RSS_SOURCES])}\n\n")
        for title, link, pubdate, source in health:
            f.write(f"{title}|{link}|{pubdate}|{source}\n")

    print(f"[OK] 保存到: {out_file}")
    return out_file

if __name__ == "__main__":
    main()
