"""
抖音数据采集工具
功能：抓取视频数据和账号基本信息，保存为 CSV/JSON 格式
用法：
    python douyin_scraper.py --video https://www.douyin.com/video/xxxxx
    python douyin_scraper.py --account 123456789
    python douyin_scraper.py --video https://www.douyin.com/video/xxxxx --cookie "sessionid=xxx"
    python douyin_scraper.py --account 123456789 --output json
"""

import argparse
import json
import csv
import re
import time
import random
import sys
import os
from datetime import datetime

try:
    import requests
except ImportError:
    print("❌ 缺少 requests 库，请先安装：pip install requests")
    sys.exit(1)

# ─────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.douyin.com/",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

SESSION = requests.Session()
SESSION.headers.update(DEFAULT_HEADERS)

# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def random_delay(min_sec: float = 1.0, max_sec: float = 3.0):
    """随机延时，防止频率过高被风控"""
    t = random.uniform(min_sec, max_sec)
    print(f"   ⏳ 延时 {t:.1f}s ...")
    time.sleep(t)


def extract_video_id(url: str) -> str:
    """从视频 URL 中提取视频 ID（支持短链和长链）"""
    # 短链格式: https://v.douyin.com/xxx
    if "v.douyin.com" in url:
        resp = SESSION.head(url, allow_redirects=True, timeout=10)
        final_url = resp.url
    else:
        final_url = url

    # 提取 video/ 后面的数字
    match = re.search(r'/video/(\d+)', final_url)
    if match:
        return match.group(1)

    # 尝试直接匹配纯数字字符串（也当作 video ID）
    match = re.search(r'(\d{15,30})', url)
    if match:
        return match.group(1)

    raise ValueError(f"❌ 无法从 URL 中提取视频 ID: {url}")


def extract_account_sec_uid(url_or_id: str) -> str:
    """从账号 URL 或直接传入 sec_uid"""
    if url_or_id.startswith("http"):
        # 解析短链
        resp = SESSION.head(url_or_id, allow_redirects=True, timeout=10)
        final_url = resp.url
        # 匹配 sec_uid=xxx 或 /user/xxx
        match = re.search(r'sec_uid=([\w]+)', final_url)
        if match:
            return match.group(1)
        match = re.search(r'/user/([\w]+)', final_url)
        if match:
            return match.group(1)
    elif "=" in url_or_id and "sec_uid" in url_or_id:
        match = re.search(r'sec_uid=([\w]+)', url_or_id)
        if match:
            return match.group(1)
    elif url_or_id.startswith("MS4wLjAB"):
        return url_or_id
    else:
        # 认为是纯数字账号ID，暂不支持，需要用户传入 sec_uid
        pass
    raise ValueError(
        f"❌ 无法从 '{url_or_id}' 提取 sec_uid。\n"
        f"   请提供完整账号主页 URL（如 https://www.douyin.com/user/xxx）\n"
        f"   或直接提供 sec_uid。"
    )


def parse_visible_count(count_str: str) -> int:
    """将 '1.2万' '3.4亿' 格式转为整数"""
    if not count_str or count_str in ['--', 'null', '']:
        return 0
    s = str(count_str).strip().replace(',', '')
    if '亿' in s:
        return int(float(s.replace('亿', '')) * 1e8)
    if '万' in s:
        return int(float(s.replace('万', '')) * 1e4)
    try:
        return int(float(s))
    except ValueError:
        return 0


# ─────────────────────────────────────────────
# API 抓取函数
# ─────────────────────────────────────────────

def fetch_video_data(video_id: str, cookie: str = None) -> dict:
    """
    通过抖音公开 API 获取视频详情
    接口：https://www.douyin.com/aweme/v1/web/aweme/detail/
    """
    url = "https://www.douyin.com/aweme/v1/web/aweme/detail/"
    params = {
        "aweme_id": video_id,
        "version_code": "170400",
        "version_name": "17.4.0",
    }
    headers = {}
    if cookie:
        headers["Cookie"] = cookie

    random_delay(1.0, 2.5)
    print(f"   🌐 请求视频 {video_id} ...")

    resp = SESSION.get(url, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    aweme_detail = data.get("aweme_detail") or data.get("aweme_info") or {}
    if not aweme_detail:
        raise ValueError(f"❌ API 未返回有效数据，响应: {data}")

    stats = aweme_detail.get("statistics", {})
    video_info = aweme_detail.get("video", {})
    author = aweme_detail.get("author", {})

    result = {
        "video_id": video_id,
        "标题": aweme_detail.get("desc", ""),
        "作者昵称": author.get("nickname", ""),
        "作者抖音号": author.get("unique_id", ""),
        "作者 sec_uid": author.get("sec_uid", ""),
        "播放量": stats.get("play_count", 0),
        "点赞数": stats.get("digg_count", 0),
        "评论数": stats.get("comment_count", 0),
        "收藏数": stats.get("collect_count", 0),
        "分享数": stats.get("share_count", 0),
        "转发数": stats.get("forward_count", 0),
        "视频时长(秒)": video_info.get("duration", 0) // 1000 if video_info.get("duration") else 0,
        "发布时间": aweme_detail.get("create_time", ""),
        "音乐标题": aweme_detail.get("music", {}).get("title", ""),
        "音乐作者": aweme_detail.get("music", {}).get("author", ""),
        "话题标签": " | ".join([t.get("hashtag_name", "") for t in aweme_detail.get("cha_list", [])]),
        "采集时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "数据来源": "抖音公开API",
    }
    return result


def fetch_account_data(sec_uid: str, cookie: str = None) -> dict:
    """
    通过抖音公开 API 获取账号基本信息
    接口：https://www.douyin.com/aweme/v1/web/user/profile/follow/other/
    """
    url = "https://www.douyin.com/aweme/v1/web/user/profile/follow/other/"
    params = {
        "sec_user_id": sec_uid,
        "version_code": "170400",
        "version_name": "17.4.0",
    }
    headers = {}
    if cookie:
        headers["Cookie"] = cookie

    random_delay(1.0, 2.5)
    print(f"   🌐 请求账号 sec_uid={sec_uid} ...")

    resp = SESSION.get(url, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    user = data.get("user", {}) or data.get("user_data", {})
    if not user:
        raise ValueError(f"❌ API 未返回有效账号数据，响应: {data}")

    result = {
        "sec_uid": sec_uid,
        "昵称": user.get("nickname", ""),
        "抖音号": user.get("unique_id", ""),
        "粉丝数": user.get("follower_count", 0),
        "关注数": user.get("following_count", 0),
        "获赞数": user.get("total_favorited", 0),
        "作品数": user.get("aweme_count", 0),
        "喜欢数": user.get("favoriting_count", 0),
        "等级": user.get("level", ""),
        "性别": user.get("gender", 0),  # 1=女 2=男 0=未知
        "签名": user.get("signature", ""),
        "IP属地": user.get("ip_location", ""),
        "认证信息": user.get("enterprise_verify_reason", ""),
        "学校": user.get("school_name", ""),
        "采集时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "数据来源": "抖音公开API",
    }
    return result


# ─────────────────────────────────────────────
# 备用：网页解析模式（当 API 不稳定时使用）
# ─────────────────────────────────────────────

def fetch_video_data_by_html(video_url: str, cookie: str = None) -> dict:
    """
    备用方案：解析抖音视频分享页 HTML 获取数据
    适合无法调用 API 时使用
    """
    headers = {}
    if cookie:
        headers["Cookie"] = cookie

    random_delay(2.0, 4.0)
    print(f"   🌐 抓取网页 {video_url} ...")

    resp = SESSION.get(video_url, headers=headers, timeout=20)
    resp.raise_for_status()
    html = resp.text

    # 从页面 JSON 数据中提取 RENDER_DATA
    match = re.search(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', html)
    if not match:
        raise ValueError("❌ 页面中未找到 RENDER_DATA，无法解析")

    import urllib.parse
    json_str = urllib.parse.unquote(match.group(1))
    page_data = json.loads(json_str)

    # 定位视频数据（结构因版本可能变化，做兼容）
    aweme_detail = (
        page_data.get("detail", {})
        or page_data.get("aweme", {})
        or page_data.get("video", {})
        or list(page_data.get("__DEFAULT_SCOPE__", {}).values())[0]
        if page_data else {}
    )

    stats = aweme_detail.get("statistics", {})
    author = aweme_detail.get("author", {})

    return {
        "video_id": extract_video_id(video_url),
        "标题": aweme_detail.get("desc", ""),
        "作者昵称": author.get("nickname", ""),
        "播放量": stats.get("play_count", 0),
        "点赞数": stats.get("digg_count", 0),
        "评论数": stats.get("comment_count", 0),
        "收藏数": stats.get("collect_count", 0),
        "分享数": stats.get("share_count", 0),
        "采集时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "数据来源": "网页解析",
    }


# ─────────────────────────────────────────────
# 保存函数
# ─────────────────────────────────────────────

def save_to_csv(data: list, filepath: str):
    if not data:
        print("⚠️  无数据可保存")
        return
    keys = list(data[0].keys())
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ 已保存 CSV: {filepath}")


def save_to_json(data: list, filepath: str):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存 JSON: {filepath}")


# ─────────────────────────────────────────────
# 主函数
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="抖音数据采集工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python douyin_scraper.py --video https://www.douyin.com/video/7328472093815717155
  python douyin_scraper.py --account https://www.douyin.com/user/MS4wLjABAAAAxxx
  python douyin_scraper.py --video 7328472093815717155 --cookie "sessionid=xxx" --output json
  python douyin_scraper.py --account MS4wLjABAAAAxxx --cookie "sessionid=xxx"
        """
    )
    parser.add_argument("--video", type=str, help="抖音视频 URL 或纯视频 ID")
    parser.add_argument("--account", type=str, help="抖音账号主页 URL 或 sec_uid")
    parser.add_argument("--cookie", type=str, default=None, help="登录态 Cookie（可选）")
    parser.add_argument("--output", type=str, default="csv", choices=["csv", "json"], help="输出格式，默认 csv")
    parser.add_argument("--file", type=str, default=None, help="自定义输出文件名（不含扩展名）")
    parser.add_argument("--html-fallback", action="store_true", help="API 失败时自动降级到网页解析模式")

    args = parser.parse_args()

    if not args.video and not args.account:
        parser.print_help()
        sys.exit(1)

    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ── 视频数据采集 ──
    if args.video:
        video_id = extract_video_id(args.video)
        print(f"\n🎬 开始采集视频: {video_id}")

        try:
            video_data = fetch_video_data(video_id, cookie=args.cookie)
        except Exception as e:
            print(f"⚠️  API 模式失败: {e}")
            if args.html_fallback:
                print("   🔄 切换到网页解析模式...")
                video_data = fetch_video_data_by_html(args.video, cookie=args.cookie)
            else:
                print("   💡 可添加 --html-fallback 参数启用自动降级")
                raise

        results.append(video_data)
        print(f"   ✅ 播放量:{video_data['播放量']:,} | 点赞:{video_data['点赞数']:,} | 评论:{video_data['评论数']:,}")

    # ── 账号数据采集 ──
    if args.account:
        sec_uid = extract_account_sec_uid(args.account)
        print(f"\n👤 开始采集账号: sec_uid={sec_uid}")

        account_data = fetch_account_data(sec_uid, cookie=args.cookie)
        results.append(account_data)
        print(f"   ✅ 粉丝:{account_data['粉丝数']:,} | 关注:{account_data['关注数']:,} | 获赞:{account_data['获赞数']:,}")

    # ── 保存 ──
    os.makedirs("scripts", exist_ok=True)
    if args.file:
        base = args.file
    else:
        prefix = "video" if args.video else "account"
        base = f"scripts/douyin_{prefix}_{timestamp}"

    if args.output == "csv":
        save_to_csv(results, base + ".csv")
    else:
        save_to_json(results, base + ".json")

    print(f"\n🎉 采集完成！共 {len(results)} 条记录")


if __name__ == "__main__":
    main()
