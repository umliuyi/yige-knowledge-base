import json, os, re

files = ['openclaw.json', 'openclaw.runtime.json', 'config.json']
base = os.path.expanduser('~') + '\\.openclaw-autoclaw'

for fname in files:
    p = os.path.join(base, fname)
    if os.path.exists(p):
        try:
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'deepseek' in content.lower():
                masked = re.sub(r'sk-[A-Za-z0-9]{10,}', 'sk-***MASKED***', content)
                masked = re.sub(r'api[_-]?key[^,}\s"]{0,30}', 'api_key: ***MASKED***', masked)
                idx = masked.lower().find('deepseek')
                start = max(0, idx - 50)
                end = min(len(masked), idx + 300)
                print(f'=== {fname} (deepseek at pos {idx}) ===')
                print(masked[start:end])
                print()
        except Exception as e:
            print(f'{fname}: error - {e}')
    else:
        print(f'{fname}: not found')