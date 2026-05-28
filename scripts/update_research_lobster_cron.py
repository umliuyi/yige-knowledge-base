# -*- coding: utf-8 -*-
"""
更新调研龙虾的cron任务prompt - 改为RSS搜索方式
"""

import json

# 读取jobs.json
with open(r"C:\Users\Administrator\.openclaw-autoclaw\cron\jobs.json", "r", encoding="utf-8") as f:
    content = f.read()

# 尝试修复编码问题后解析
data = json.loads(content)

# 新的每日调研龙虾prompt（RSS搜索方式）
daily_prompt = """你是2号调研龙虾（Research Lobster），负责为海南首位健康科技有限公司提供每日行业调研简报。

【重要】从2026-05-18起，搜索方式改为RSS订阅，不再依赖百度/Bing API。

【第一步】读取工作规范
读取：C:\\Users\\Administrator\\.openclaw-autoclaw\\workspace\\lobster-team\\specs\\02-research-lobster.md

【第二步】RSS搜索（主要搜索方式）
使用Python requests或feedparser抓取以下RSS源获取新闻：

```python
import requests
import re
from datetime import datetime, timedelta

RSS_SOURCES = {
    "36kr科技": "https://36kr.com/feed",
    "丁香园": "http://www.dxy.cn/rss/home.xml",
    "动脉网": "https://vcbeat.top/Rss/News",
}

def fetch_rss(source_name, url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        return resp.text
    except Exception as e:
        return None
```

关键词过滤（与规范中的搜索关键词一致）：
- 乐城政策："博鳌乐城"、"乐城先行区"、"乐城管理局"、"乐城 新技术"、"乐城 新药械"
- 新药审批："NMPA 批准"、"FDA 批准"、"新药审批"、"CART"、"免疫治疗"
- 生物技术："基因编辑"、"CRISPR"、"细胞治疗"、"干细胞"、"AI医疗"
- 竞品："惠民保"、"特药险"、"权益卡"

【第三步】整理输出
- 写日报到：C:\\Users\\Administrator\\.openclaw-autoclaw\\workspace\\lobster-team\\research\\daily\\YYYY-MM-DD.md
- 更新乐城动态：C:\\Users\\Administrator\\.openclaw-autoclaw\\workspace\\lobster-team\\research\\lecheng-daily.md

【第四步】发送
使用 feishu_im_user_message 发送到：
- receive_id: ou_33dffd40ad59a555c256ff5e989f6bd7
- msg_type: text
"""

# 新的每周调研龙虾prompt
weekly_prompt = """你是2号调研龙虾。请读取工作规范 lobster-team/specs/02-research-lobster.md，然后执行每周详细报告任务。

【重要】从2026-05-18起，搜索方式改为RSS订阅，不再依赖百度/Bing API。

【搜索方式】使用Python feedparser或requests抓取RSS源：
```python
import requests
RSS_SOURCES = {
    "36kr科技": "https://36kr.com/feed",
    "丁香园": "http://www.dxy.cn/rss/home.xml",
    "动脉网": "https://vcbeat.top/Rss/News",
}
```

按规范生成详细周报，保存到 lobster-team/research/weekly/ 目录（文件名用YYYY-WXX格式），然后通过消息发送给一哥。
"""

# 更新两个调研龙虾的prompt
for job in data["jobs"]:
    if job["id"] == "ccfa1206-4c7d-4add-b64a-96985fa11992":
        job["payload"]["message"] = daily_prompt
        print(f"已更新每日调研龙虾: {job['name']}")
    elif job["id"] == "340f9ce4-9086-4a07-8820-8e33fe8d1ce3":
        job["payload"]["message"] = weekly_prompt
        print(f"已更新每周调研龙虾: {job['name']}")

# 写回文件
with open(r"C:\Users\Administrator\.openclaw-autoclaw\cron\jobs.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ 已更新cron jobs.json，调研龙虾改为RSS搜索方式")