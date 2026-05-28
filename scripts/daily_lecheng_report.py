# -*- coding: utf-8 -*-
import urllib.request, ssl, xml.etree.ElementTree as ET, sys, json
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

FEISHU_USER_ID = "ou_33dffd40ad59a555c256ff5e989f6bd7"

RSS_SOURCES = [
    "https://36kr.com/feed",
    "https://www.chiwitz.com/feed",
]

KEYWORDS = ["乐城", "海南博鳌", "干细胞", "免疫治疗", "CAR-T", "基因治疗", "新药械", "特许药械", "NMPA", "FDA审批", "临床试验"]

def fetch_rss():
    items = []
    for url in RSS_SOURCES:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=10, context=ctx)
            # ET needs bytes
            raw = resp.read()
            feed = ET.fromstring(raw)
            for item in feed.iter("item"):
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                desc = item.findtext("description", "")
                pubdate = item.findtext("pubDate", "")
                if not title:
                    continue
                for kw in KEYWORDS:
                    if kw in title or kw in desc:
                        items.append({"title": title, "link": link, "desc": desc[:150], "pubdate": pubdate})
                        break
        except Exception as e:
            print(f"RSS failed {url}: {e}")
    return items

def main():
    items = fetch_rss()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M}] Fetched {len(items)} items")
    for it in items:
        print(f"[ITEM] {it['title']}")
        print(f"  {it['link']}")
        print(f"  {it['desc'][:80]}")
    return items

if __name__ == "__main__":
    main()
