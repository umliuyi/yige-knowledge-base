with open(r"C:\Users\Administrator\.openclaw-autoclaw\workspace\lobster-team\specs\02-research-lobster.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "搜索" in line or "必应" in line or "bing" in line.lower() or "autoglm" in line.lower() or "browser" in line.lower() or "web_search" in line.lower() or "搜索渠道" in line or "渠道" in line:
        print(f"{i}: {line.rstrip()}")
