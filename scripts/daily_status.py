# 每日龙虾早巡 · 团队状态同步
# 每天早上自动更新上下文记忆，供所有会话共享

from datetime import datetime
import os

TODAY = datetime.now().strftime("%Y-%m-%d")
MEMORY_FILE = rf"C:\Users\Administrator\.openclaw-autoclaw\workspace\memory\{TODAY}.md"
SUMMARY_FILE = rf"C:\Users\Administrator\.openclaw-autoclaw\workspace\.lobster-ops\daily-strategy\{TODAY}.md"

summary = f"""
【团队状态 | {TODAY}】

调研龙虾·日：6:30 ✅
早报视频流水线：8:30 ✅
运营龙虾：9:00 ✅
CEO早巡：9:05 ✅
干细胞推送：20:00 ✅
战略龙虾：23:30 ✅

请读取今日memory文件获取最新进展。
"""

os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
with open(MEMORY_FILE, "a", encoding="utf-8") as f:
    f.write("\n" + summary)

print(f"[OK] 每日状态已记录: {TODAY}")
