import re, os, sys
from datetime import datetime

md_path = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206\2026-05-14.md"
with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract all ## headings
lines = content.split("\n")
headings = []
for line in lines:
    line = line.strip()
    if line.startswith("##"):
        title = line.lstrip("#").strip()
        if len(title) > 2:
            headings.append(title)

print(f"Found {len(headings)} headings:")
for h in headings:
    print(f"  - {h[:80]}")

# Extract bullet points under ## blocks
in_block = False
current_block = ""
blocks = []
for line in lines:
    line_stripped = line.strip()
    if line_stripped.startswith("##"):
        if current_block:
            blocks.append(current_block)
        current_block = line_stripped
    elif line_stripped.startswith("**") and current_block:
        current_block += "\n" + line_stripped
    elif line_stripped.startswith("- 来源"):
        blocks.append(current_block)
        current_block = ""

if current_block:
    blocks.append(current_block)

# Extract key sentences from blocks
key_sentences = []
for block in blocks:
    for line in block.split("\n"):
        line = line.strip()
        # Get bullet points
        if line.startswith("-") and not line.startswith("- 来源") and len(line) > 15:
            text = line.lstrip("-").strip()
            if len(text) > 10:
                key_sentences.append(text[:100])

print(f"\nExtracted {len(key_sentences)} bullet points:")
for s in key_sentences[:10]:
    print(f"  - {s[:80]}")
