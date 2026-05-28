import re, sys
md_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\lobster-team\research\daily\2026-05-13.md"
with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

# 找所有标题行（## 开头 或 ** 开头 或 🔴📌 开头）
lines = content.split("\n")
for i, line in enumerate(lines):
    line = line.strip()
    if line and (line.startswith("##") or line.startswith("**") or line.startswith("🔴") or line.startswith("📌")):
        print(f"{i}: {line[:100]}")
