with open(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\MEMORY.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if '调研龙虾' in line or '龙虾团队' in line or 'ccfa1206' in line or '任务计划' in line:
        print(f'{i}: {line.rstrip()[:120]}')