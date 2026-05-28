#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
网络数据爬虫工具
功能：抓取网页标题/正文、提取关键信息、保存为JSON/CSV、支持多页面爬取
依赖：requests, beautifulsoup4, lxml
"""

import argparse
import csv
import json
import logging
import random
import re
import time
import urllib.robotparser
from datetime import datetime
from typing import Any

import requests
from bs4 import BeautifulSoup

# ===================== 日志配置 =====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ===================== 反爬策略 =====================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 "
    "Firefox/125.0",
]


def get_headers() -> dict[str, str]:
    """返回随机UA的请求头"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


# ===================== robots.txt 检查 =====================
class RobotsChecker:
    """robots.txt 缓存管理器"""

    def __init__(self, cache_ttl: int = 3600):
        self._cache: dict[str, tuple[urllib.robotparser.RobotFileParser, float]] = {}
        self._cache_ttl = cache_ttl

    def can_fetch(self, url: str) -> bool:
        """检查是否允许抓取（返回 True = 允许，False = 不允许或出错）"""
        try:
            from urllib.parse import urlparse
            base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        except Exception:
            return True  # 解析失败时保守放行

        now = time.time()
        if base in self._cache:
            rp, cached_at = self._cache[base]
            if now - cached_at < self._cache_ttl:
                return rp.can_fetch("*", url)

        rp = urllib.robotparser.RobotFileParser()
        robots_url = base + "/robots.txt"
        try:
            resp = requests.get(robots_url, timeout=5, headers=get_headers())
            resp.raise_for_status()
            rp.parse(resp.text.splitlines())
            self._cache[base] = (rp, now)
        except Exception as e:
            logger.debug("robots.txt 获取失败 [%s]: %s", robots_url, e)
            self._cache[base] = (rp, now)

        return rp.can_fetch("*", url)


_robots_checker: RobotsChecker | None = None


def set_robots_checker(checker: RobotsChecker | None):
    global _robots_checker
    _robots_checker = checker


# ===================== 内容提取 =====================
def extract_title(soup: BeautifulSoup) -> str:
    """提取页面标题"""
    # 优先 og:title → <title> → <h1>
    for tag in ["meta[property='og:title']", "meta[name='twitter:title']", "title", "h1"]:
        el = soup.select_one(tag)
        if el:
            val = el.get("content", "") or el.get_text().strip()
            if val:
                return val
    return "无标题"


def extract_pub_date(soup: BeautifulSoup) -> str | None:
    """提取发布日期"""
    patterns = [
        # meta 标签
        {"tag": "meta[property='article:published_time']", "attr": "content"},
        {"tag": "meta[name='publishdate']", "attr": "content"},
        {"tag": "meta[name='date']", "attr": "content"},
        {"tag": "meta[name='pubdate']", "attr": "content"},
        # time 标签
        {"tag": "time[datetime]", "attr": "datetime"},
        {"tag": "time", "attr": None},
    ]
    for p in patterns:
        el = soup.select_one(p["tag"])
        if el:
            val = el.get(p["attr"], "").strip() if p["attr"] else el.get_text().strip()
            if val:
                return val
    return None


def extract_price(text: str) -> list[str]:
    """从文本中提取价格（人民币/美元/通用格式）"""
    patterns = [
        r"￥\s*([0-9,，.]+\d)",
        r"CNY\s*([0-9,，.]+\d)",
        r"\$\s*([0-9,，.]+\d)",
        r"USD\s*([0-9,，.]+\d)",
        r"(\d+\.?\d*)\s*(?:元|块|円)",
    ]
    results = []
    for pat in patterns:
        results.extend(re.findall(pat, text))
    return results


def extract_links(soup: BeautifulSoup, base_url: str) -> list[dict[str, str]]:
    """提取页面所有链接"""
    from urllib.parse import urljoin
    links = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full = urljoin(base_url, href)
        if full not in seen and full.startswith("http"):
            seen.add(full)
            links.append({
                "text": a.get_text().strip()[:100],
                "url": full,
            })
    return links


def extract_images(soup: BeautifulSoup, base_url: str) -> list[str]:
    """提取所有图片 src"""
    from urllib.parse import urljoin
    urls = []
    seen = set()
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src", "")
        if src:
            full = urljoin(base_url, src)
            if full not in seen and full.startswith("http"):
                seen.add(full)
                urls.append(full)
    return urls


def extract_main_content(soup: BeautifulSoup) -> str:
    """提取正文内容（去掉脚本、样式、导航等）"""
    # 尝试常见内容容器
    for selector in [
        "article",
        "[role='main']",
        "main",
        ".content",
        "#content",
        ".post",
        ".article",
        ".entry",
        ".post-content",
        ".article-content",
    ]:
        container = soup.select_one(selector)
        if container:
            return container.get_text(separator="\n", strip=True)
    # 兜底：body
    body = soup.find("body")
    if body:
        return body.get_text(separator="\n", strip=True)
    return soup.get_text(separator="\n", strip=True)


def extract_key_info(soup: BeautifulSoup, text: str) -> dict[str, Any]:
    """提取各类关键信息"""
    return {
        "pub_date": extract_pub_date(soup),
        "prices": extract_price(text),
        "links_count": len(soup.find_all("a", href=True)),
        "images_count": len(soup.find_all("img")),
        "has_form": bool(soup.find("form")),
    }


# ===================== 单页抓取 =====================
def scrape_page(
    url: str,
    timeout: int = 10,
    delay: float = 1.0,
    check_robots: bool = True,
) -> dict[str, Any] | None:
    """抓取单个页面，返回结构化数据字典"""
    if check_robots:
        global _robots_checker
        if _robots_checker is None:
            _robots_checker = RobotsChecker()
        if not _robots_checker.can_fetch(url):
            logger.warning("[robots.txt] 禁止抓取: %s", url)
            return None

    try:
        resp = requests.get(url, headers=get_headers(), timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        logger.error("请求失败 [%s]: %s", url, e)
        return None

    # 自动检测编码
    resp.encoding = resp.apparent_encoding or "utf-8"

    soup = BeautifulSoup(resp.text, "lxml")

    # 移除干扰标签
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    plain_text = extract_main_content(soup)

    record = {
        "url": url,
        "title": extract_title(soup),
        "pub_date": extract_pub_date(soup),
        "content_preview": plain_text[:500],
        "content_length": len(plain_text),
        "prices": extract_price(plain_text),
        "links": extract_links(soup, url),
        "images": extract_images(soup, url),
        "key_info": extract_key_info(soup, plain_text),
        "http_status": resp.status_code,
        "fetched_at": datetime.now().isoformat(),
    }
    return record


# ===================== 多页爬取 =====================
def scrape_multiple(
    urls: list[str],
    delay: float = 1.0,
    check_robots: bool = True,
    max_workers: int = 1,
) -> list[dict[str, Any]]:
    """顺序爬取多个页面（delay 秒间隔）"""
    results = []
    for i, url in enumerate(urls, 1):
        logger.info("[%d/%d] 抓取: %s", i, len(urls), url)
        result = scrape_page(url, check_robots=check_robots)
        if result:
            results.append(result)
        if i < len(urls):
            time.sleep(delay)
    return results


# ===================== 持久化 =====================
def save_json(data: list[dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info("JSON 保存完成: %s (%d 条)", path, len(data))


def save_csv(data: list[dict], path: str):
    if not data:
        return
    flat = []
    for rec in data:
        flat.append({
            "url": rec.get("url", ""),
            "title": rec.get("title", ""),
            "pub_date": rec.get("pub_date", ""),
            "prices": "|".join(rec.get("prices", [])),
            "links_count": len(rec.get("links", [])),
            "images_count": len(rec.get("images", [])),
            "content_length": rec.get("content_length", 0),
            "http_status": rec.get("http_status", ""),
            "fetched_at": rec.get("fetched_at", ""),
        })
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=flat[0].keys())
        writer.writeheader()
        writer.writerows(flat)
    logger.info("CSV 保存完成: %s (%d 条)", path, len(data))


# ===================== CLI =====================
def main():
    parser = argparse.ArgumentParser(
        description="网络数据爬虫工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python web_scraper.py -u https://news.example.com -o result.json
  python web_scraper.py -u https://a.com https://b.com -o out.csv -f csv
  python web_scraper.py -u https://shop.example.com -o items.json --no-robots
        """,
    )
    parser.add_argument(
        "-u", "--url",
        nargs="+",
        required=True,
        help="目标 URL（支持多个，空格分隔）",
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="输出文件路径（.json 或 .csv）",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["json", "csv", "auto"],
        default="auto",
        help="输出格式（默认 auto，按文件扩展名自动判断）",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="请求间隔秒数（默认 1.0）",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="请求超时秒数（默认 10）",
    )
    parser.add_argument(
        "--no-robots",
        action="store_true",
        help="跳过 robots.txt 检查",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="输出详细日志",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    fmt = args.format
    if fmt == "auto":
        fmt = "json" if args.output.endswith(".json") else "csv"

    # 逐页抓取
    records = []
    for i, url in enumerate(args.url, 1):
        logger.info("[%d/%d] 抓取: %s", i, len(args.url), url)
        result = scrape_page(
            url,
            timeout=args.timeout,
            delay=args.delay,
            check_robots=not args.no_robots,
        )
        if result:
            records.append(result)
        if i < len(args.url):
            time.sleep(args.delay)

    if not records:
        logger.warning("未抓取到任何数据")
        return

    if fmt == "json":
        save_json(records, args.output)
    else:
        save_csv(records, args.output)

    logger.info("抓取完成！共获取 %d 条记录 → %s", len(records), args.output)


if __name__ == "__main__":
    main()
