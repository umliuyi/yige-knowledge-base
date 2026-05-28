# -*- coding: utf-8 -*-
"""
小红书数据采集工具
功能：
  1. 抓取笔记/视频基础数据（标题、点赞、收藏、评论数、发布者信息等）
  2. 抓取指定账号的粉丝数、获赞数、笔记数
  3. 保存为 CSV 或 JSON 格式

用法：
  # 抓取单条笔记
  python xiaohongshu_scraper.py --note-url "https://www.xiaohongshu.com/explore/xxxxx"

  # 抓取账号主页数据
  python xiaohongshu_scraper.py --user-url "https://www.xiaohongshu.com/user/profile/xxxxx"

  # 指定输出格式和文件
  python xiaohongshu_scraper.py --note-url "..." --format json --output result.json

  # 使用 Cookie 登录态（提升数据完整度）
  python xiaohongshu_scraper.py --note-url "..." --cookie "your_cookie_here"

  # 使用代理
  python xiaohongshu_scraper.py --note-url "..." --proxy "http://127.0.0.1:7890"

依赖：
  pip install requests beautifulsoup4 lxml pandas
"""

import argparse
import json
import random
import re
import sys
import time
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────
# 配置区
# ─────────────────────────────────────────────
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
DEFAULT_HEADERS = {
    "User-Agent": DEFAULT_UA,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.xiaohongshu.com/",
    "Origin": "https://www.xiaohongshu.com",
}

# 小红书 API 端点（可能随版本变动）
API_NOTE_DETAIL = "https://www.xiaohongshu.com/api/sns/web/v1/feed"
API_USER_INFO   = "https://www.xiaohongshu.com/api/sns/web/v1/user/info"
API_USER_POSTS  = "https://www.xiaohongshu.com/api/sns/web/v1/user_post"

# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def random_delay(min_sec: float = 3.0, max_sec: float = 5.0):
    """随机延时，模拟真人访问节奏。"""
    t = random.uniform(min_sec, max_sec)
    print(f"  [延时] 等待 {t:.1f}s ...")
    time.sleep(t)


def build_session(cookie: str = None, proxy: str = None) -> requests.Session:
    """构建带 UA、Cookie、代理的 requests Session。"""
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    if cookie:
        session.headers["Cookie"] = cookie
    if proxy:
        session.proxies = {"http": proxy, "https": proxy}
    return session


def extract_note_id(url: str) -> str:
    """从笔记 URL 中提取 note_id。"""
    # 兼容格式：
    # https://www.xiaohongshu.com/explore/xxxxx
    # https://www.xiaohongshu.com/discovery/item/xxxxx
    patterns = [
        r"/explore/([a-f0-9]+)",
        r"/discovery/item/([a-f0-9]+)",
        r"noteId=([a-f0-9]+)",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    raise ValueError(f"无法从 URL 中提取 note_id：{url}")


def extract_user_id(url: str) -> str:
    """从账号主页 URL 中提取 user_id。"""
    patterns = [
        r"/user/profile/([a-f0-9]+)",
        r"userId=([a-f0-9]+)",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    raise ValueError(f"无法从 URL 中提取 user_id：{url}")


def parse_json_response(resp: requests.Response) -> dict:
    """尝试解析 JSON 响应，带容错。"""
    try:
        data = resp.json()
    except Exception as e:
        print(f"  [警告] JSON 解析失败：{e}")
        print(f"  [响应内容前200字符]：{resp.text[:200]}")
        return {}
    if data.get("code") != 0 and data.get("success") is not True:
        msg = data.get("msg") or data.get("message") or "未知错误"
        print(f"  [警告] 接口返回错误：{msg}")
    return data.get("data") or {}


# ─────────────────────────────────────────────
# 核心采集函数
# ─────────────────────────────────────────────

def scrape_note(session: requests.Session, note_url: str) -> dict:
    """
    通过笔记 URL 抓取单条笔记的基础数据。

    返回字段：
      note_id, title, desc, liked_count, collected_count, comment_count,
      share_count, tags, author_id, author_name, author_follower_count,
      publish_time, note_type (normal/video), image_urls
    """
    note_id = extract_note_id(note_url)
    print(f"\n[笔记] 开始抓取 note_id={note_id}")

    # 方式一：调用 feed 接口
    try:
        params = {"source_note_id": note_id, "image_formats": ["jpg", "webp", "avif"]}
        resp = session.get(API_NOTE_DETAIL, params=params, timeout=15)
        data = parse_json_response(resp)

        if data and "items" in data and len(data["items"]) > 0:
            note = data["items"][0].get("note_card", {})
            return _parse_note_card(note)

        # 方式二：解析 HTML 页面作为兜底
        print("  [兜底] API 未返回数据，尝试解析 HTML 页面 ...")
        return _scrape_note_html(session, note_url)

    except requests.RequestException as e:
        print(f"  [错误] 网络请求异常：{e}")
        # 兜底 HTML
        return _scrape_note_html(session, note_url)


def _parse_note_card(card: dict) -> dict:
    """从 note_card 结构中提取字段。"""
    interact = card.get("interact_info", {}) or {}
    user = card.get("user", {}) or {}

    return {
        "note_id":        card.get("note_id", ""),
        "title":          card.get("title", "") or card.get("desc", ""),
        "desc":           card.get("desc", ""),
        "liked_count":    _safe_int(interact.get("liked_count")),
        "collected_count":_safe_int(interact.get("collected_count")),
        "comment_count":  _safe_int(interact.get("comment_count")),
        "share_count":    _safe_int(interact.get("share_count")),
        "tags":           card.get("tag_list", []),
        "author_id":      user.get("user_id", ""),
        "author_name":    user.get("nickname", ""),
        "publish_time":   card.get("time", ""),
        "note_type":      card.get("type", "normal"),
        "image_urls":     _extract_images(card),
        "source_url":     f"https://www.xiaohongshu.com/explore/{card.get('note_id','')}",
        "crawl_time":     datetime.now().isoformat(),
    }


def _extract_images(card: dict) -> list:
    """从卡片中提取图片列表。"""
    urls = []
    # 兼容不同版本的图片字段结构
    for key in ["image_list", "images", "imageUrls"]:
        imgs = card.get(key, [])
        if isinstance(imgs, list):
            for img in imgs:
                url = img.get("url") or img.get("webp_url") or img.get("original_url") or img.get("trace_id","")
                if url and url not in urls:
                    urls.append(url)
    return urls


def _scrape_note_html(session: requests.Session, note_url: str) -> dict:
    """HTML 页面解析作为兜底方案。"""
    print(f"  [HTML解析] 请求页面：{note_url}")
    try:
        resp = session.get(note_url, timeout=15)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "lxml")

        # 尝试从 script 标签中提取 JSON 数据
        result = {}
        scripts = soup.find_all("script")
        for script in scripts:
            text = script.string or ""
            if '"noteId"' in text or '"note_id"' in text:
                # 提取 JSON 对象
                m = re.search(r'\{[^{}]{100,5000}\}', text)
                if m:
                    try:
                        obj = json.loads(m.group())
                        result = _extract_from_raw_json(obj)
                        if result.get("note_id"):
                            return result
                    except Exception:
                        pass

        # 兜底：直接解析 HTML 结构
        title = (soup.select_one("h1") or soup.select_one(".title") or
                 soup.select_one("[class*='title']") or soup.select_one("title"))
        title = title.get_text(strip=True) if title else ""

        return {
            "note_id":    extract_note_id(note_url),
            "title":      title,
            "desc":       "",
            "liked_count": 0, "collected_count": 0, "comment_count": 0,
            "share_count": 0, "tags": [], "author_id": "", "author_name": "",
            "publish_time": "", "note_type": "normal", "image_urls": [],
            "source_url": note_url,
            "crawl_time": datetime.now().isoformat(),
            "note": "数据需要登录态才能完整获取，请使用 --cookie 参数",
        }
    except Exception as e:
        print(f"  [错误] HTML 解析失败：{e}")
        return {"error": str(e), "source_url": note_url}


def _extract_from_raw_json(obj: dict) -> dict:
    """从原始 JSON 对象中提取笔记字段。"""
    # 递归查找含 noteId 的节点
    if isinstance(obj, dict):
        if obj.get("noteId") or obj.get("note_id"):
            nid = obj.get("noteId") or obj.get("note_id")
            return {
                "note_id": nid,
                "title": obj.get("title") or obj.get("desc", ""),
                "desc": obj.get("desc", ""),
                "liked_count": _safe_int(obj.get("likedCount") or obj.get("liked_count")),
                "collected_count": _safe_int(obj.get("collectedCount") or obj.get("collected_count")),
                "comment_count": _safe_int(obj.get("commentCount") or obj.get("comment_count")),
                "share_count": _safe_int(obj.get("shareCount") or obj.get("share_count")),
                "tags": obj.get("tags") or [],
                "author_id": obj.get("userId") or obj.get("user_id") or "",
                "author_name": obj.get("nickname") or obj.get("author", ""),
                "publish_time": obj.get("time") or obj.get("publishTime") or "",
                "note_type": obj.get("type", "normal"),
                "image_urls": [],
                "source_url": f"https://www.xiaohongshu.com/explore/{nid}",
                "crawl_time": datetime.now().isoformat(),
            }
        for v in obj.values():
            if isinstance(v, (dict, list)):
                res = _extract_from_raw_json(v)
                if res:
                    return res
    elif isinstance(obj, list):
        for item in obj:
            res = _extract_from_raw_json(item)
            if res:
                return res
    return {}


def scrape_user(session: requests.Session, user_url: str) -> dict:
    """
    通过账号主页 URL 抓取账号基础数据。

    返回字段：
      user_id, nickname, description, fans_count, following_count,
      liked_count, notes_count, tags, publish_time, avatar
    """
    user_id = extract_user_id(user_url)
    print(f"\n[账号] 开始抓取 user_id={user_id}")

    # 调用用户信息接口
    try:
        params = {"user_id": user_id}
        resp = session.get(API_USER_INFO, params=params, timeout=15)
        data = parse_json_response(resp)

        if data:
            basic = data.get("basic_info", {}) or {}
            intro = data.get("introduce_info", {}) or {}
            return {
                "user_id":        user_id,
                "nickname":       basic.get("nickname", ""),
                "description":    intro.get("desc", ""),
                "fans_count":     _safe_int(basic.get("fans", basic.get("fans_count"))),
                "following_count":_safe_int(basic.get("follow", basic.get("following_count"))),
                "liked_count":    _safe_int(data.get("liked_count")),
                "notes_count":    _safe_int(data.get("notes_count") or data.get("note_count")),
                "tags":           data.get("tags") or [],
                "avatar":         basic.get("avatar", ""),
                "source_url":     user_url,
                "crawl_time":     datetime.now().isoformat(),
            }

        # 兜底：解析 HTML
        print("  [兜底] API 未返回数据，尝试解析 HTML ...")
        return _scrape_user_html(session, user_url, user_id)

    except requests.RequestException as e:
        print(f"  [错误] 网络请求异常：{e}")
        return _scrape_user_html(session, user_url, user_id)


def _scrape_user_html(session: requests.Session, user_url: str, user_id: str) -> dict:
    """HTML 页面解析作为用户信息兜底。"""
    print(f"  [HTML解析] 请求页面：{user_url}")
    try:
        resp = session.get(user_url, timeout=15)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "lxml")

        nickname = ""
        desc = ""
        fans = following = notes = 0

        # 尝试从 script 提取 JSON
        scripts = soup.find_all("script")
        for script in scripts:
            text = script.string or ""
            if "user_id" in text or "nickname" in text:
                m = re.search(r'\{[^{}]{200,8000}\}', text)
                if m:
                    try:
                        obj = json.loads(m.group())
                        nickname = obj.get("nickname", nickname)
                        desc = obj.get("desc", desc)
                        fans = _safe_int(obj.get("fans") or obj.get("fans_count"))
                        following = _safe_int(obj.get("follow") or obj.get("following_count"))
                        notes = _safe_int(obj.get("notes_count") or obj.get("note_count"))
                        if nickname:
                            break
                    except Exception:
                        pass

        # 兜底：HTML 元素
        if not nickname:
            tag = soup.select_one("[class*='user-name']") or soup.select_one("[class*='nickname']")
            nickname = tag.get_text(strip=True) if tag else ""

        stat_blocks = soup.select("[class*='stat']")
        if len(stat_blocks) >= 3:
            try:
                notes = int(re.sub(r"\D", "", stat_blocks[0].get_text(strip=True)))
                fans  = int(re.sub(r"\D", "", stat_blocks[1].get_text(strip=True)))
                following = int(re.sub(r"\D", "", stat_blocks[2].get_text(strip=True)))
            except Exception:
                pass

        return {
            "user_id": user_id,
            "nickname": nickname,
            "description": desc,
            "fans_count": fans,
            "following_count": following,
            "liked_count": 0,
            "notes_count": notes,
            "tags": [],
            "avatar": "",
            "source_url": user_url,
            "crawl_time": datetime.now().isoformat(),
            "note": "数据需要登录态才能完整获取，请使用 --cookie 参数",
        }
    except Exception as e:
        print(f"  [错误] HTML 解析失败：{e}")
        return {"error": str(e), "user_id": user_id, "source_url": user_url}


def _safe_int(val) -> int:
    """安全转换为整数，处理 None、空字符串、异常。"""
    if val is None:
        return 0
    if isinstance(val, int):
        return val
    if isinstance(val, float):
        return int(val)
    if isinstance(val, str):
        val = re.sub(r"[万wW]", "", val)
        try:
            return int(float(val))
        except Exception:
            return 0
    try:
        return int(val)
    except Exception:
        return 0


# ─────────────────────────────────────────────
# 输出保存
# ─────────────────────────────────────────────

def save_output(data: dict, output_path: str, fmt: str = "csv"):
    """将采集结果保存为 CSV 或 JSON 文件。"""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    if fmt == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 结果已保存为 JSON：{output_path}")
    else:
        import csv
        # 展平嵌套字段
        flat = _flatten_dict(data)
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=flat.keys())
            w.writeheader()
            w.writerow(flat)
        print(f"\n✅ 结果已保存为 CSV：{output_path}")


def _flatten_dict(d: dict, parent_key: str = "", sep: str = "_") -> dict:
    """将嵌套字典展平为单层，键之间用 sep 连接。"""
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(_flatten_dict(v, new_key, sep))
        elif isinstance(v, list):
            items[new_key] = "|".join(str(x) for x in v) if v else ""
        else:
            items[new_key] = v
    return items


# ─────────────────────────────────────────────
# 命令行入口
# ─────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="小红书数据采集工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python xiaohongshu_scraper.py --note-url "https://www.xiaohongshu.com/explore/abc123"
  python xiaohongshu_scraper.py --user-url "https://www.xiaohongshu.com/user/profile/xyz456"
  python xiaohongshu_scraper.py --note-url "..." --format json --output result.json
  python xiaohongshu_scraper.py --note-url "..." --cookie "web_session=xxxx"
  python xiaohongshu_scraper.py --note-url "..." --proxy "http://127.0.0.1:7890"
        """,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--note-url", help="笔记详情页 URL")
    group.add_argument("--user-url", help="账号主页 URL")

    parser.add_argument("--cookie",    default=os.getenv("XHS_COOKIE", ""),
                        help="登录 Cookie（提升数据完整度，可通过环境变量 XHS_COOKIE 传入）")
    parser.add_argument("--proxy",     default=os.getenv("XHS_PROXY", ""),
                        help="HTTP 代理，如 http://127.0.0.1:7890")
    parser.add_argument("--format",   choices=["csv", "json"], default="csv",
                        help="输出格式（默认 csv）")
    parser.add_argument("--output",    default="",
                        help="输出文件路径（默认自动生成）")
    parser.add_argument("--delay-min", type=float, default=3.0,
                        help="随机延时下限（秒，默认 3.0）")
    parser.add_argument("--delay-max", type=float, default=5.0,
                        help="随机延时上限（秒，默认 5.0）")
    parser.add_argument("--no-delay",  action="store_true",
                        help="禁用延时（仅用于调试）")

    return parser.parse_args()


def auto_output_path(note_url: str = "", user_url: str = "", fmt: str = "csv") -> str:
    """根据采集对象自动生成默认文件名。"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    if note_url:
        nid = extract_note_id(note_url)
        return f"xhs_note_{nid}_{ts}.{fmt}"
    elif user_url:
        uid = extract_user_id(user_url)
        return f"xhs_user_{uid}_{ts}.{fmt}"
    return f"xhs_result_{ts}.{fmt}"


def main():
    args = parse_args()

    # 参数校验
    if args.delay_min > args.delay_max:
        print("[错误] --delay-min 不能大于 --delay-max")
        sys.exit(1)

    delay_range = (args.delay_min, args.delay_max) if not args.no_delay else (0, 0)

    print("=" * 50)
    print("  小红书数据采集工具")
    print(f"  模式：{'笔记' if args.note_url else '账号'}")
    print(f"  输出格式：{args.format}")
    print(f"  Cookie：{'已提供 ✓' if args.cookie else '未提供（数据可能不完整）'}")
    print(f"  代理：{'已配置' if args.proxy else '未配置'}")
    print(f"  延时：{'禁用' if args.no_delay else f'{delay_range[0]}~{delay_range[1]}s'}")
    print("=" * 50)

    session = build_session(cookie=args.cookie or None, proxy=args.proxy or None)

    if args.note_url:
        if not args.no_delay:
            random_delay(*delay_range)
        result = scrape_note(session, args.note_url)
    else:
        if not args.no_delay:
            random_delay(*delay_range)
        result = scrape_user(session, args.user_url)

    # 打印结果摘要
    print("\n── 采集结果摘要 ──")
    if "note_id" in result:
        print(f"  标题：{result.get('title','')[:60]}")
        print(f"  点赞：{result.get('liked_count',0)}")
        print(f"  收藏：{result.get('collected_count',0)}")
        print(f"  评论：{result.get('comment_count',0)}")
        print(f"  作者：{result.get('author_name','')}")
    elif "user_id" in result:
        print(f"  昵称：{result.get('nickname','')}")
        print(f"  粉丝：{result.get('fans_count',0)}")
        print(f"  获赞：{result.get('liked_count',0)}")
        print(f"  笔记：{result.get('notes_count',0)}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    # 保存
    output = args.output or auto_output_path(args.note_url, args.user_url, args.format)
    save_output(result, output, args.format)
    print(f"\n文件已保存：{os.path.abspath(output)}")


if __name__ == "__main__":
    main()
