#!/usr/bin/env python3
"""
飞书日报同步脚本
将今日早报同步到飞书云文档

用法: python sync_to_feishu.py YYYY-MM-DD
"""
import os, sys, re
from datetime import datetime

REPORT_DIR = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206"

def read_report(date_str):
    """读取日报文件"""
    path = os.path.join(REPORT_DIR, f"{date_str}.md")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def md_to_lark(text):
    """简单MD转飞书Markdown"""
    # 标题
    text = re.sub(r'^### (.*)$', '### \\1', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*)$', '## \\1', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*)$', '# \\1', text, flags=re.MULTILINE)
    # 粗体
    text = re.sub(r'\*\*(.*?)\*\*', '**\\1**', text)
    # 链接
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', '\\1', text)
    return text

def sync(date_str):
    content = read_report(date_str)
    if not content:
        print(f"[ERROR] 未找到日报: {date_str}.md")
        return False

    title = f"早报 {date_str} | 刘一精算师"
    md = f"# {title}\n\n> 自动同步自每日调研龙虾报告\n\n" + md_to_lark(content)
    print(f"[OK] 已准备好同步文档，共 {len(md)} 字符")
    print("下一步：请用 feishu_create_doc 工具创建飞书文档")
    print(f"文档内容前200字：\n{md[:200]}")
    return True

if __name__ == "__main__":
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    sync(date)