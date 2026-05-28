import os, re

files = ['auto_search36kr.py', 'pubmed_verify.py', 'quality_checker.py']

for fname in files:
    path = os.path.join(r'C:\Users\Administrator\.openclaw-autoclaw\workspace\scripts', fname)
    if not os.path.exists(path):
        print(f'SKIP: {fname} not found')
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace requests imports
    if 'import requests' in content:
        content = content.replace('import requests', 'import urllib.request\nimport urllib.parse')
    # Replace requests.get/post calls
    content = re.sub(r"requests\.get\(", "urllib.request.urlopen(", content)
    content = re.sub(r"requests\.post\(", "urllib.request.urlopen(", content)
    # Replace r.text
    content = re.sub(r'\.text', '.read().decode("utf-8", errors="ignore")', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Fixed: {fname}')
    print(f'  - import requests: {"yes" if "import urllib" in content else "no"}')
    print(f'  - urllib calls: {content.count("urllib")}')
