#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快手数据采集工具 (Kuaishou Scraper)
功能：抓取快手作品数据、账号信息，保存为CSV/JSON格式

依赖：pip install requests fake-useragent
用法：
    python kuaishou_scraper.py --url "https://www.kuaishou.com/short-video/xxx"
    python kuaishou_scraper.py --user-id "1234567890"
    python kuaishou_scraper.py --url "..." --cookie "ks_session=xxx"
"""

import argparse
import csv
import json
import random
import re
import sys
import time
from datetime import datetime
from typing import Optional

import requests

# ============================================================
# 配置区
# ============================================================
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.kuaishou.com/",
    "Origin": "https://www.kuaishou.com",
}

# 常用 UA 池（备用）
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
]

# ============================================================
# 工具函数
# ============================================================
def random_delay(min_sec: float = 1.0, max_sec: float = 3.0) -> None:
    """随机延时，模拟人类行为，避开反爬"""
    time.sleep(random.uniform(min_sec, max_sec))

def random_ua() -> str:
    return random.choice(USER_AGENTS)

def build_session(cookie: Optional[str] = None) -> requests.Session:
    """构建带 UA 和 cookie 的 session"""
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    session.headers["User-Agent"] = random_ua()
    if cookie:
        session.headers["Cookie"] = cookie
    return session

def parse_short_video_id(url: str) -> Optional[str]:
    """从短链接提取作品 ID（photoId）"""
    # https://www.kuaishou.com/short-video/xxxxxxxxx
    match = re.search(r'/short-video/([A-Za-z0-9_-]+)', url)
    if match:
        return match.group(1)
    # 旧版分享链接 ?fid=xxx 或 &videoId=xxx
    match = re.search(r'(?:fid|videoId|video_id)[=&](\w+)', url, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def parse_user_id(url_or_id: str) -> Optional[str]:
    """判断是 URL 还是纯 ID，提取用户 ID"""
    # 如果是 URL，尝试提取 eeee 或 userId
    if "kuaishou.com" in url_or_id:
        # /profile/xxxxxx 形式
        match = re.search(r'/profile/([A-Za-z0-9_-]+)', url_or_id)
        if match:
            return match.group(1)
        match = re.search(r'(?:userId|user_id|authorId)[=&](\w+)', url_or_id, re.IGNORECASE)
        if match:
            return match.group(1)
    return url_or_id.strip()

# ============================================================
# API 采集函数
# ============================================================
class KuaishouAPI:
    """快手数据采集核心类"""

    # 公开 API 端点（参考公开文档，随时可能变动）
    BASE_API = "https://www.kuaishou.com"

    def __init__(self, session: requests.Session):
        self.session = session

    def _get(self, url: str, params: dict = None, retry: int = 3) -> Optional[dict]:
        """带重试的 GET 请求"""
        for attempt in range(retry):
            try:
                random_delay()
                resp = self.session.get(url, params=params, timeout=15)
                if resp.status_code == 200:
                    try:
                        return resp.json()
                    except json.JSONDecodeError:
                        return None
                elif resp.status_code == 403:
                    print(f"[警告] 访问被拒绝 (403)，可能触发了反爬机制")
                    random_delay(3, 6)
                elif resp.status_code == 429:
                    print(f"[警告] 请求过于频繁 (429)，等待更长时间...")
                    random_delay(5, 10)
                else:
                    print(f"[警告] HTTP {resp.status_code}")
            except requests.RequestException as e:
                print(f"[错误] 请求失败: {e}")
                random_delay(2, 5)
        return None

    def get_video_detail(self, photo_id: str) -> Optional[dict]:
        """
        通过快手分享页面 HTML 解析作品数据（备用方案）
        当 API 不稳定时使用
        """
        url = f"{self.BASE_API}/short-video/{photo_id}"
        try:
            random_delay()
            resp = self.session.get(url, timeout=15)
            if resp.status_code != 200:
                return None
            html = resp.text
            # 尝试从 HTML 中提取 JSON 数据（快手前端常把数据埋在这里）
            match = re.search(r'window\.__INIT_PROPS__\s*=\s*(\{.*?\})\s*</script>', html, re.DOTALL)
            if not match:
                # 另一种埋数据方式
                match = re.search(r'"photoId"\s*:\s*"' + photo_id + r'"[^}]+}', html)
            # 也尝试 og:description 等 meta 标签
            data = {
                "photo_id": photo_id,
                "url": url,
                "title": self._extract_meta(html, "og:title", ""),
                "description": self._extract_meta(html, "og:description", ""),
                "author": self._extract_meta(html, "author", ""),
            }
            # 从 HTML 中提取播放量
            view_match = re.search(r'"viewCount"\s*:\s*"?(\d+)"?', html)
            if view_match:
                data["view_count"] = int(view_match.group(1))
            like_match = re.search(r'"likeCount"\s*:\s*"?(\d+)"?', html)
            if like_match:
                data["like_count"] = int(like_match.group(1))
            return data if data.get("title") or data.get("description") else None
        except Exception as e:
            print(f"[错误] 解析作品页面失败: {e}")
            return None

    def get_user_profile(self, user_id: str) -> Optional[dict]:
        """
        通过快手个人主页 HTML 解析账号信息
        """
        url = f"{self.BASE_API}/profile/{user_id}"
        try:
            random_delay()
            resp = self.session.get(url, timeout=15)
            if resp.status_code != 200:
                return None
            html = resp.text
            # 从 HTML 中提取用户信息
            data = {
                "user_id": user_id,
                "url": url,
                "name": self._extract_meta(html, "profile:username", "") or self._extract_regex(html, r'"name"\s*:\s*"([^"]+)"'),
            }
            # 粉丝数
            fan_match = re.search(r'"fans"\s*:\s*"?(\d+)"?', html)
            if fan_match:
                data["fans_count"] = int(fan_match.group(1))
            # 关注数
            follow_match = re.search(r'"following"\s*:\s*"?(\d+)"?', html)
            if follow_match:
                data["following_count"] = int(follow_match.group(1))
            # 作品数
            video_match = re.search(r'"videoCount"\s*:\s*"?(\d+)"?', html)
            if video_match:
                data["video_count"] = int(video_match.group(1))
            return data
        except Exception as e:
            print(f"[错误] 解析用户页面失败: {e}")
            return None

    def _extract_meta(self, html: str, prop: str, default: str = "") -> str:
        match = re.search(rf'<meta\s+(?:property|name)="{re.escape(prop)}"\s+content="([^"]+)"', html)
        return match.group(1) if match else default

    def _extract_regex(self, text: str, pattern: str) -> str:
        match = re.search(pattern, text)
        return match.group(1) if match else ""


# ============================================================
# 数据保存
# ============================================================
def save_json(data: list, filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[保存] JSON → {filepath}")

def save_csv(data: list, filepath: str) -> None:
    if not data:
        return
    keys = list(data[0].keys())
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"[保存] CSV → {filepath}")


# ============================================================
# CLI 入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="快手数据采集工具 - 采集作品数据和账号信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python kuaishou_scraper.py --url "https://www.kuaishou.com/short-video/xxx" --format json
  python kuaishou_scraper.py --user-id "eeee123456" --format csv
  python kuaishou_scraper.py --url "..." --cookie "ks_session=abc123" --output result.json
        """
    )
    parser.add_argument("--url", help="作品链接 (https://www.kuaishou.com/short-video/xxx)")
    parser.add_argument("--user-id", help="账号ID或主页链接")
    parser.add_argument("--cookie", help="登录态 Cookie (可选，播放量等数据可能需要)")
    parser.add_argument("--format", choices=["csv", "json", "both"], default="json", help="输出格式 (默认 json)")
    parser.add_argument("--output", help="输出文件路径 (不含扩展名，工具自动加 .csv/.json)")
    parser.add_argument("--delay-min", type=float, default=1.0, help="请求间隔最小秒数 (默认 1.0)")
    parser.add_argument("--delay-max", type=float, default=3.0, help="请求间隔最大秒数 (默认 3.0)")

    args = parser.parse_args()

    if not args.url and not args.user_id:
        parser.print_help()
        sys.exit(1)

    # 构建 session
    session = build_session(args.cookie)

    # 合并延时配置
    delay_min = args.delay_min
    delay_max = args.delay_max

    # 全局随机延时函数用闭包捕获
    global random_ua
    orig_random_delay = random_delay
    def _random_delay():
        time.sleep(random.uniform(delay_min, delay_max))
    # 替换模块级延时函数（hacky，但不影响其他模块）
    import types
    random_delay_module = sys.modules[__name__]
    random_delay_module.random_delay = _random_delay

    api = KuaishouAPI(session)
    results = []

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # -------- 采集作品 --------
    if args.url:
        print(f"\n[采集] 作品: {args.url}")
        photo_id = parse_short_video_id(args.url)
        if not photo_id:
            print("[错误] 无法从 URL 提取作品 ID")
            sys.exit(1)
        print(f"[解析] photo_id = {photo_id}")
        data = api.get_video_detail(photo_id)
        if data:
            results.append(data)
            print(f"[成功] title={data.get('title', 'N/A')}, view={data.get('view_count', 'N/A')}, like={data.get('like_count', 'N/A')}")
        else:
            print("[失败] 未能获取作品数据（可能接口已变动或需要登录态）")

    # -------- 采集账号 --------
    if args.user_id:
        print(f"\n[采集] 账号: {args.user_id}")
        uid = parse_user_id(args.user_id)
        print(f"[解析] user_id = {uid}")
        data = api.get_user_profile(uid)
        if data:
            results.append(data)
            print(f"[成功] name={data.get('name','N/A')}, fans={data.get('fans_count','N/A')}, videos={data.get('video_count','N/A')}")
        else:
            print("[失败] 未能获取账号数据（可能接口已变动或需要登录态）")

    if not results:
        print("\n[结果] 未采集到任何数据，请检查链接或cookie是否有效")
        sys.exit(0)

    # -------- 保存 --------
    if not args.output:
        prefix = f"kuaishou_{timestamp}"
    else:
        prefix = args.output

    if args.format in ("json", "both"):
        save_json(results, f"{prefix}.json")
    if args.format in ("csv", "both"):
        # CSV 只保存第一个表（作品或账号）
        save_csv(results if len(results) == 1 else [results[0]], f"{prefix}.csv")

    print(f"\n[完成] 共采集 {len(results)} 条记录")


if __name__ == "__main__":
    main()