import os
md_path = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\lobster-team\research\daily\2026-05-13.md'
with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()
# Extract news items (lines with 🔴 or 📌)
lines = content.split('\n')
for line in lines:
    if line.startswith('🔴') or line.startswith('📌'):
        print(line[:200])
