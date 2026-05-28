# -*- coding: utf-8 -*-
"""
飞书消息工具 (Feishu/Lark Message Tool)
=========================================
支持：
  1. 发送文本消息（Webhook 推送 / API 发送）
  2. 富文本消息（Post 格式）
  3. 发送文件 / 图片
  4. 读取群消息历史

依赖：pip install requests

使用方式：
  python feishu_message_tool.py

配置（顶部 CONFIG）：
  - WEBHOOK_URL      : 机器人 Webhook 地址（用于推送模式，无需 token）
  - APP_ID           : 应用 App ID（API 模式需要）
  - APP_SECRET       : 应用 App Secret（API 模式需要）
  - USER_ACCESS_TOKEN: 用户访问令牌（可选，API 模式需要）

作者：AutoClaw
"""

import json
import os
import base64
import mimetypes
import urllib.parse
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Union

import requests

# ============================================================
# 配置区 — 请根据实际情况修改
# ============================================================
CONFIG = {
    # --- Webhook 模式（最简单，仅用于推送）---
    # 在飞书群机器人设置中获取 Webhook 地址
    "WEBHOOK_URL": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx",

    # --- API 模式（需要自建应用）---
    # 在飞书开放平台创建应用后获取
    "APP_ID": "cli_xxxxxxxxxxxxxxxx",
    "APP_SECRET": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",

    # --- 可选：用户级 Token（读取消息历史需要）---
    # 通过 OAuth 或用户授权获取
    "USER_ACCESS_TOKEN": "",

    # --- 默认接收者（方便调试）---
    "DEFAULT_CHAT_ID": "",   # 群 ID，oc_xxx 格式
    "DEFAULT_OPEN_ID": "",   # 用户 open_id，ou_xxx 格式
}

# API 基础地址
BASE_URL = "https://open.feishu.cn/open-apis"


# ============================================================
# 工具函数
# ============================================================

class FeishuError(Exception):
    """飞书 API 错误"""
    def __init__(self, code: int, msg: str, raw: Optional[Dict] = None):
        self.code = code
        self.msg = msg
        self.raw = raw or {}
        super().__init__(f"[{code}] {msg}")


def _getTenantAccessToken(app_id: str, app_secret: str) -> str:
    """获取 tenant_access_token（应用级 Token）"""
    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    payload = {"app_id": app_id, "app_secret": app_secret}
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise FeishuError(data.get("code", -1), data.get("msg", "获取 Token 失败"), data)
    return data["tenant_access_token"]


def _headers(token: Optional[str] = None) -> Dict[str, str]:
    """构建 HTTP 请求头"""
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _call_api(method: str, path: str, token: Optional[str] = None,
              json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
    """通用 API 调用封装"""
    url = f"{BASE_URL}{path}"
    headers = _headers(token)
    resp = requests.request(method, url, headers=headers, json=json_data, params=params, timeout=30)
    try:
        data = resp.json()
    except Exception:
        resp.raise_for_status()
        raise FeishuError(-1, f"响应解析失败 [{resp.status_code}]: {resp.text[:200]}")

    if data.get("code") != 0:
        raise FeishuError(data.get("code", -1), data.get("msg", "API 调用失败"), data)
    return data.get("data", {})


# ============================================================
# 1. Webhook 推送（最简单，无需 Token）
# ============================================================

def send_text_via_webhook(webhook_url: str, text: str) -> Dict:
    """
    通过 Webhook 发送纯文本消息到群。
    Webhook 机器人只能在群里使用，无法发送给个人。

    Args:
        webhook_url: 机器人 Webhook 地址
        text: 消息内容

    Returns:
        API 返回数据
    """
    payload = {
        "msg_type": "text",
        "content": {"text": text}
    }
    resp = requests.post(webhook_url, json=payload, timeout=10)
    try:
        data = resp.json()
    except Exception:
        resp.raise_for_status()
        raise FeishuError(-1, f"响应解析失败 [{resp.status_code}]: {resp.text[:200]}", {})

    if data.get("code") != 0:
        raise FeishuError(data.get("code", -1), data.get("msg", "Webhook 发送失败"), data)
    return data


def send_rich_text_via_webhook(webhook_url: str, title: str, content: List[List[Dict]]) -> Dict:
    """
    通过 Webhook 发送富文本消息（Post）。

    Args:
        webhook_url: 机器人 Webhook 地址
        title: 消息标题
        content: 富文本内容，二维数组。
                 每行是一个段落，每段是多个标签的列表。
                 标签示例：
                   {"tag": "text", "text": "普通文本"}
                   {"tag": "a", "text": "链接文字", "href": "https://..."}
                   {"tag": "at", "text": "@某人", "user_id": "ou_xxx"}

    Returns:
        API 返回数据
    """
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": content
                }
            }
        }
    }
    resp = requests.post(webhook_url, json=payload, timeout=10)
    try:
        data = resp.json()
    except Exception:
        resp.raise_for_status()
        raise FeishuError(-1, f"响应解析失败 [{resp.status_code}]: {resp.text[:200]}", {})

    if data.get("code") != 0:
        raise FeishuError(data.get("code", -1), data.get("msg", "Webhook 富文本发送失败"), data)
    return data


def send_image_via_webhook(webhook_url: str, image_key: str) -> Dict:
    """
    通过 Webhook 发送图片（需先上传图片获取 image_key）。

    Args:
        webhook_url: 机器人 Webhook 地址
        image_key: 图片 key，通过 upload_image 获取

    Returns:
        API 返回数据
    """
    payload = {"msg_type": "image", "content": {"image_key": image_key}}
    resp = requests.post(webhook_url, json=payload, timeout=10)
    try:
        data = resp.json()
    except Exception:
        resp.raise_for_status()
        raise FeishuError(-1, f"响应解析失败 [{resp.status_code}]: {resp.text[:200]}", {})

    if data.get("code") != 0:
        raise FeishuError(data.get("code", -1), data.get("msg", "Webhook 图片发送失败"), data)
    return data


# ============================================================
# 2. API 方式发送（需要 App ID/Secret，支持发送给个人）
# ============================================================

def send_text_message(chat_id: Optional[str] = None,
                      open_id: Optional[str] = None,
                      text: str = "",
                      token: Optional[str] = None) -> Dict:
    """
    通过 API 发送纯文本消息（可发给群或用户）。

    Args:
        chat_id: 群 ID（oc_xxx），发给群时使用
        open_id: 用户 open_id（ou_xxx），发给用户时使用
        text: 消息文本
        token: tenant_access_token 或 user_access_token

    Returns:
        包含 message_id 的数据
    """
    if not token:
        token = _getTenantAccessToken(CONFIG["APP_ID"], CONFIG["APP_SECRET"])

    receive_id_type = "chat_id" if chat_id else "open_id"
    receive_id = chat_id or open_id

    payload = {
        "receive_id": receive_id,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    return _call_api("POST", "/im/v1/messages", token=token, json_data=payload,
                     params={"receive_id_type": receive_id_type})


def send_rich_text_message(chat_id: Optional[str] = None,
                           open_id: Optional[str] = None,
                           title: str = "",
                           content: Optional[List[List[Dict]]] = None,
                           token: Optional[str] = None) -> Dict:
    """
    通过 API 发送富文本消息（Post）。

    Args:
        chat_id: 群 ID
        open_id: 用户 open_id
        title: 标题
        content: 富文本内容，同 Webhook 版
        token: 访问令牌

    Returns:
        包含 message_id 的数据
    """
    if not token:
        token = _getTenantAccessToken(CONFIG["APP_ID"], CONFIG["APP_SECRET"])

    receive_id_type = "chat_id" if chat_id else "open_id"
    receive_id = chat_id or open_id
    content = content or []

    post_content = {
        "post": {
            "zh_cn": {
                "title": title,
                "content": content
            }
        }
    }
    payload = {
        "receive_id": receive_id,
        "msg_type": "post",
        "content": json.dumps(post_content)
    }
    return _call_api("POST", "/im/v1/messages", token=token, json_data=payload,
                     params={"receive_id_type": receive_id_type})


def send_file_message(chat_id: Optional[str] = None,
                      open_id: Optional[str] = None,
                      file_path: str = "",
                      token: Optional[str] = None) -> Dict:
    """
    通过 API 上传并发送文件。

    Args:
        chat_id: 群 ID
        open_id: 用户 open_id
        file_path: 本地文件路径
        token: 访问令牌

    Returns:
        包含 message_id 的数据
    """
    if not token:
        token = _getTenantAccessToken(CONFIG["APP_ID"], CONFIG["APP_SECRET"])

    if not os.path.exists(file_path):
        raise FeishuError(-1, f"文件不存在: {file_path}")

    receive_id_type = "chat_id" if chat_id else "open_id"
    receive_id = chat_id or open_id

    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    file_size = os.path.getsize(file_path)

    # Step 1: 获取上传 URL
    file_type_map = {
        "video": "video",
        "audio": "audio",
        "file": "file",
        "image": "image",
    }
    file_type = "file"
    for k, v in file_type_map.items():
        if mime_type.startswith(k):
            file_type = v
            break

    upload_payload = {
        "file_name": filename,
        "file_type": file_type,
        "file_size": file_size,
    }
    upload_data = _call_api("POST", "/im/v1/files", token=token, json_data=upload_payload)
    upload_url = upload_data.get("upload_url", "")
    file_key = upload_data.get("file_key", "")

    if not upload_url:
        raise FeishuError(-1, "获取文件上传 URL 失败")

    # Step 2: 上传文件到飞书
    with open(file_path, "rb") as f:
        files = {"file": (filename, f, mime_type)}
        upload_resp = requests.post(upload_url, files=files, timeout=60)
        if upload_resp.status_code not in (200, 201):
            raise FeishuError(-1, f"文件上传失败 [{upload_resp.status_code}]: {upload_resp.text[:200]}")

    # Step 3: 发送消息
    payload = {
        "receive_id": receive_id,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key})
    }
    return _call_api("POST", "/im/v1/messages", token=token, json_data=payload,
                     params={"receive_id_type": receive_id_type})


def send_image_message(chat_id: Optional[str] = None,
                      open_id: Optional[str] = None,
                      image_path: str = "",
                      token: Optional[str] = None) -> Dict:
    """
    上传图片并发送。

    Args:
        chat_id: 群 ID
        open_id: 用户 open_id
        image_path: 本地图片路径
        token: 访问令牌

    Returns:
        包含 message_id 的数据
    """
    if not token:
        token = _getTenantAccessToken(CONFIG["APP_ID"], CONFIG["APP_SECRET"])

    if not os.path.exists(image_path):
        raise FeishuError(-1, f"图片文件不存在: {image_path}")

    receive_id_type = "chat_id" if chat_id else "open_id"
    receive_id = chat_id or open_id

    # Step 1: 上传图片
    with open(image_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()
        mime_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"
        image_payload = {
            "image_type": "message",
            "image": img_data
        }
        upload_data = _call_api("POST", "/im/v1/images", token=token, json_data=image_payload)
        image_key = upload_data.get("image_key", "")

    if not image_key:
        raise FeishuError(-1, "图片上传失败，未获取到 image_key")

    # Step 2: 发送消息
    payload = {
        "receive_id": receive_id,
        "msg_type": "image",
        "content": json.dumps({"image_key": image_key})
    }
    return _call_api("POST", "/im/v1/messages", token=token, json_data=payload,
                     params={"receive_id_type": receive_id_type})


# ============================================================
# 3. 读取消息历史
# ============================================================

def get_chat_messages(chat_id: str,
                      container_id_type: str = "chat",
                      container_id: Optional[str] = None,
                      start_time: Optional[str] = None,
                      end_time: Optional[str] = None,
                      page_size: int = 50,
                      sort_type: str = "ByCreateTimeDesc",
                      token: Optional[str] = None) -> Dict:
    """
    拉取群消息历史。

    Args:
        chat_id: 群 ID（oc_xxx）
        container_id_type: 容器类型，默认 chat
        container_id: 容器 ID（同 chat_id）
        start_time: 起始时间，ISO 8601 或 10位时间戳（秒）
        end_time: 结束时间，ISO 8601 或 10位时间戳（秒）
        page_size: 每页数量（1-50）
        sort_type: ByCreateTimeDesc（最新优先）/ ByCreateTimeAsc（最旧优先）
        token: 访问令牌

    Returns:
        包含 messages 列表和 has_more / page_token
    """
    if not token:
        token = _getTenantAccessToken(CONFIG["APP_ID"], CONFIG["APP_SECRET"])

    if container_id is None:
        container_id = chat_id

    params = {
        "container_id_type": container_id_type,
        "container_id": container_id,
        "page_size": min(page_size, 50),
        "sort_type": sort_type,
    }

    if start_time:
        params["start_time"] = start_time
    if end_time:
        params["end_time"] = end_time

    return _call_api("GET", "/im/v1/messages", token=token, params=params)


def search_messages(query: str,
                    chat_id: Optional[str] = None,
                    start_time: Optional[str] = None,
                    end_time: Optional[str] = None,
                    page_size: int = 50,
                    token: Optional[str] = None) -> Dict:
    """
    搜索消息内容。

    Args:
        query: 搜索关键词
        chat_id: 限定在某个群搜索（可选）
        start_time: 起始时间
        end_time: 结束时间
        page_size: 每页数量
        token: 访问令牌

    Returns:
        包含 messages 列表
    """
    if not token:
        token = _getTenantAccessToken(CONFIG["APP_ID"], CONFIG["APP_SECRET"])

    payload = {
        "query": query,
        "page_size": min(page_size, 50),
    }
    if chat_id:
        payload["chat_ids"] = [chat_id]
    if start_time:
        payload["start_time"] = start_time
    if end_time:
        payload["end_time"] = end_time

    return _call_api("POST", "/im/v1/messages/search", token=token, json_data=payload)


def parse_message_content(msg: Dict) -> Dict:
    """
    解析消息内容，返回可读文本。

    Args:
        msg: 原始消息对象

    Returns:
        包含 msg_type, text, sender 等字段的字典
    """
    msg_type = msg.get("msg_type", "")
    body = msg.get("body", {})
    content = body.get("content", "{}")

    try:
        content = json.loads(content)
    except Exception:
        content = {"raw": content}

    text = ""
    if msg_type == "text":
        text = content.get("text", "")
    elif msg_type == "post":
        # 提取富文本内容
        posts = content.get("post", {})
        zh_cn = posts.get("zh_cn", {})
        title = zh_cn.get("title", "")
        lines = []
        for para in zh_cn.get("content", []):
            line_texts = []
            for item in para:
                if item.get("tag") == "text":
                    line_texts.append(item.get("text", ""))
                elif item.get("tag") == "at":
                    line_texts.append(f"@{item.get('name', item.get('user_id', ''))}")
                elif item.get("tag") == "a":
                    line_texts.append(f"{item.get('text', '')}({item.get('href', '')})")
                elif item.get("tag") == "img":
                    line_texts.append(f"[图片: {item.get('image_key', '')}]")
            if line_texts:
                lines.append("".join(line_texts))
        text = title + "\n" + "\n".join(lines) if title else "\n".join(lines)
    elif msg_type == "image":
        text = f"[图片消息] image_key: {content.get('image_key', '')}"
    elif msg_type == "file":
        text = f"[文件消息] file_name: {content.get('file_name', '')}"
    elif msg_type == "audio":
        text = "[语音消息]"
    elif msg_type == "video":
        text = "[视频消息]"
    elif msg_type == "share_chat":
        text = f"[群名片] chat_id: {content.get('chat_id', '')}"
    elif msg_type == "share_user":
        text = f"[个人名片] user_id: {content.get('user_id', '')}"
    else:
        text = json.dumps(content, ensure_ascii=False)

    sender = msg.get("sender", {})
    sender_id = sender.get("id", "")
    sender_type = sender.get("sender_type", "")

    return {
        "message_id": msg.get("message_id", ""),
        "msg_type": msg_type,
        "text": text,
        "sender_id": sender_id,
        "sender_type": sender_type,
        "create_time": msg.get("create_time", ""),
        "update_time": msg.get("update_time", ""),
        "chat_id": msg.get("chat_id", ""),
        "isEdited": msg.get("is_edited", False),
    }


def format_message_list(messages: List[Dict]) -> str:
    """格式化消息列表为可读字符串"""
    if not messages:
        return "（无消息）"

    lines = []
    for i, msg in enumerate(messages, 1):
        parsed = parse_message_content(msg)
        sender = f"[{parsed['sender_type']}] {parsed['sender_id']}"
        time_str = parsed["create_time"]
        lines.append(
            f"--- 消息 {i} ---\n"
            f"ID: {parsed['message_id']}\n"
            f"类型: {parsed['msg_type']} | 发送者: {sender}\n"
            f"时间: {time_str}\n"
            f"内容: {parsed['text'][:200]}"
        )
    return "\n\n".join(lines)


# ============================================================
# 演示 / 示例用法
# ============================================================

def demo():
    """演示各种发送和读取方式"""
    print("=" * 50)
    print("飞书消息工具 演示")
    print("=" * 50)

    webhook = CONFIG["WEBHOOK_URL"]

    # --- 1. Webhook 发送文本 ---
    print("\n[1] Webhook 发送文本...")
    try:
        result = send_text_via_webhook(webhook, "🤖 测试消息：你好，这是一条来自 Python 脚本的推送！")
        print(f"    ✅ 发送成功: {result}")
    except FeishuError as e:
        print(f"    ❌ 发送失败: {e}")

    # --- 2. Webhook 富文本 ---
    print("\n[2] Webhook 发送富文本...")
    try:
        rich_content = [
            [
                {"tag": "text", "text": "📢 重要通知\n"},
                {"tag": "text", "text": "这是一条"},
                {"tag": "text", "text": "加粗", "bold": True},
                {"tag": "text", "text": "和"},
                {"tag": "text", "text": "链接", "italic": True},
                {"tag": "text", "text": "的文本。"},
            ],
            [
                {"tag": "a", "text": "👉 点击这里了解更多", "href": "https://feishu.cn"},
            ],
        ]
        result = send_rich_text_via_webhook(webhook, "飞书机器人通知", rich_content)
        print(f"    ✅ 发送成功: {result}")
    except FeishuError as e:
        print(f"    ❌ 发送失败: {e}")

    # --- 3. API 发送文本到群 ---
    print("\n[3] API 发送文本到群...")
    try:
        token = _getTenantAccessToken(CONFIG["APP_ID"], CONFIG["APP_SECRET"])
        result = send_text_message(
            chat_id=CONFIG.get("DEFAULT_CHAT_ID"),
            text="🤖 API 方式发送的消息！",
            token=token
        )
        print(f"    ✅ 发送成功: message_id = {result.get('message_id')}")
    except FeishuError as e:
        print(f"    ❌ 发送失败: {e}")

    # --- 4. API 发送富文本 ---
    print("\n[4] API 发送富文本...")
    try:
        rich_content = [
            [
                {"tag": "text", "text": "📊 今日数据报告\n"},
                {"tag": "text", "text": "新增用户: 128人\n"},
                {"tag": "text", "text": "活跃用户: 95人"},
            ],
        ]
        result = send_rich_text_message(
            chat_id=CONFIG.get("DEFAULT_CHAT_ID"),
            title="📈 数据日报",
            content=rich_content,
            token=token
        )
        print(f"    ✅ 发送成功: message_id = {result.get('message_id')}")
    except FeishuError as e:
        print(f"    ❌ 发送失败: {e}")

    # --- 5. 读取群消息历史 ---
    print("\n[5] 读取群消息历史...")
    try:
        chat_id = CONFIG.get("DEFAULT_CHAT_ID") or os.environ.get("FEISHU_CHAT_ID")
        if chat_id:
            data = get_chat_messages(
                chat_id=chat_id,
                page_size=5,
                token=token
            )
            messages = data.get("items", [])
            print(f"    拉取到 {len(messages)} 条消息：")
            print(format_message_list(messages))
        else:
            print("    ⚠️ 未配置 DEFAULT_CHAT_ID，跳过")
    except FeishuError as e:
        print(f"    ❌ 读取失败: {e}")

    print("\n" + "=" * 50)
    print("演示结束")
    print("=" * 50)


if __name__ == "__main__":
    demo()
