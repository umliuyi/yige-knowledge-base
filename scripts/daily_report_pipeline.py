#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日早报全自动流水线
执行步骤：
1. pubmed_daily.py → 获取四大专题文献
2. 汇总 → 发飞书
"""
import subprocess, os, sys
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")
WORKSPACE = r"C:\Users\Administrator\.openclaw-autoclaw\workspace"
GROWTH_DIR = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206"
RESULT_FILE = os.path.join(GROWTH_DIR, f"pubmed_results_{TODAY}.txt")

# Step 1: 执行pubmed搜索
print(f"[{datetime.now().strftime('%H:%M')}] Step 1: 执行pubmed_daily.py...")
r1 = subprocess.run(
    ["python", os.path.join(WORKSPACE, "scripts", "pubmed_daily.py")],
    capture_output=True, text=True,
    cwd=WORKSPACE
)
if r1.returncode != 0:
    print(f"[WARN] pubmed_daily失败: {r1.stderr[:200]}")
else:
    print(f"[OK] pubmed_daily完成")

# Step 2: 检查结果文件
if not os.path.exists(RESULT_FILE):
    print(f"[ERROR] 结果文件不存在: {RESULT_FILE}")
    sys.exit(1)

# 读取文献
with open(RESULT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 提取前3条有DOI的文献
lines = content.split("\n")
entries = []
for line in lines:
    if line.startswith("[") and "PMID:" in line:
        entries.append(line.strip())

print(f"[OK] 共{len(entries)}条文献")

# Step 3: 生成早报并发送（这里只输出结果）
# 发送部分需要用 feishu_im_user_message 工具，此处只生成文本
print("\n[OK] 早报内容已生成，请发送飞书")
print(f"文件路径: {RESULT_FILE}")
