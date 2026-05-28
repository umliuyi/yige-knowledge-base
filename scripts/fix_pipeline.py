import re, os

# Fix 1: hardcoded date in assemble_daily_news.py
asm_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\scripts\assemble_daily_news.py"
with open(asm_path, "r", encoding="utf-8") as f:
    asm = f.read()

# Fix output filename to use today's date
from datetime import datetime
today_str = datetime.now().strftime("%Y%m%d")
asm = asm.replace(
    '"daily_news_20260509.mp4"',
    f'"daily_news_{today_str}.mp4"'
)
with open(asm_path, "w", encoding="utf-8") as f:
    f.write(asm)
print(f"Fixed output filename -> daily_news_{today_str}.mp4")

# Fix 2: extract more news items from MD
md_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\lobster-team\research\daily\2026-05-13.md"
with open(md_path, "r", encoding="utf-8") as f:
    md = f.read()

# Extract all ## and 🔴/📌 headings
lines = md.split("\n")
items = []
for line in lines:
    line = line.strip()
    if line.startswith("##") and len(line) > 4:
        # ## 标题 -> 标题
        title = line.lstrip("#").strip()
        title = re.sub(r'^[🔴📌]\s*\*?\*?', '', title).strip("* ")
        if title and len(title) > 3:
            items.append(title)
    elif line.startswith("🔴") or line.startswith("📌"):
        title = re.sub(r'^[🔴📌]\s*\*?\*?', '', line).strip("* ")
        if title and len(title) > 3:
            items.append(title)

print(f"Extracted {len(items)} items: {items}")

# Fix 3: also need to update the narration in assemble_daily_news
# The SLIDES_AUDIO was updated to today's narrations
# But we also need to update the daily_news_slides SOURCE_FILE
slides_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\scripts\daily_news_slides.py"
with open(slides_path, "r", encoding="utf-8") as f:
    sl = f.read()

sl = re.sub(
    r'SOURCE_FILE\s*=\s*r"[^"]*"',
    'SOURCE_FILE = r"' + md_path.replace('\\', '\\\\') + '"',
    sl
)
with open(slides_path, "w", encoding="utf-8") as f:
    f.write(sl)
print("Fixed SOURCE_FILE in daily_news_slides.py")
