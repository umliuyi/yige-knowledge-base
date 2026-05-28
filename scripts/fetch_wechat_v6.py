import urllib.request, ssl, re, json, html as html_module
from datetime import datetime
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://mp.weixin.qq.com/s/S5p6ssSQfGLRenxeGCmPuw'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://mp.weixin.qq.com/'
})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw_bytes = resp.read()
raw_utf8 = raw_bytes.decode('utf-8', errors='ignore')
raw_gbk = raw_bytes.decode('gbk', errors='ignore')

utf8_c = len(re.findall(r'[\u4e00-\u9fff]', raw_utf8))
gbk_c = len(re.findall(r'[\u4e00-\u9fff]', raw_gbk))

# Use whichever has more Chinese for body text
raw_body = raw_utf8 if utf8_c > gbk_c else raw_gbk
print('Body encoding:', 'UTF-8' if utf8_c > gbk_c else 'GBK', f'({utf8_c} vs {gbk_c} CJK chars)')

# For title: find in body text directly (not meta tag)
# The first H1-like text or first paragraph with title-like content
first_h = re.search(r'<h1[^>]*>(.*?)</h1>', raw_body, re.DOTALL)
title_from_h1 = re.sub(r'<[^>]+>', '', first_h.group(1)).strip() if first_h else ''

# Also try first bold text
first_b = re.search(r'<strong[^>]*>(.*?)</strong>', raw_body, re.DOTALL)
title_from_b = re.sub(r'<[^>]+>', '', first_b.group(1)).strip() if first_b else ''

# Extract text paragraphs
texts = re.findall(r'<(?:p|span)[^>]*>(.*?)</(?:p|span)>', raw_body, re.DOTALL)
clean = []
for t in texts:
    txt = re.sub(r'<[^>]+>', '', t).strip()
    if len(txt) >= 10 and re.search(r'[\u4e00-\u9fff]', txt):
        txt = html_module.unescape(txt)
        clean.append(txt)

# Try to get og:title from BOTH encodings and pick the one with more readable Chinese
for enc_name, raw in [('UTF-8', raw_utf8), ('GBK', raw_gbk)]:
    m = re.search(r'<meta property="og:title" content="([^"]+)"', raw)
    if m:
        cand = m.group(1)
        chinese_in_cand = len(re.findall(r'[\u4e00-\u9fff]', cand))
        print(f'og:title from {enc_name}: {repr(cand[:60])} ({chinese_in_cand} CJK chars)')

# Use h1 if it has Chinese
if title_from_h1 and len(re.findall(r'[\u4e00-\u9fff]', title_from_h1)) >= 3:
    title = html_module.unescape(title_from_h1)
    print('Using H1 title:', title[:60])
elif title_from_b and len(re.findall(r'[\u4e00-\u9fff]', title_from_b)) >= 3:
    title = html_module.unescape(title_from_b)
    print('Using bold title:', title[:60])
else:
    # Try from meta, pick the one with more Chinese
    best_title = ''
    for enc_name, raw in [('UTF-8', raw_utf8), ('GBK', raw_gbk)]:
        m = re.search(r'<meta property="og:title" content="([^"]+)"', raw)
        if m:
            cand = m.group(1)
            if len(re.findall(r'[\u4e00-\u9fff]', cand)) > len(re.findall(r'[\u4e00-\u9fff]', best_title)):
                best_title = cand
    title = html_module.unescape(best_title)
    print('Using og:title:', title[:60])

# Get desc from UTF-8 (meta tags usually UTF-8)
og_d = re.search(r'<meta property="og:description" content="([^"]+)"', raw_utf8)
og_i = re.search(r'<meta property="og:image" content="([^"]+)"', raw_utf8)
desc = og_d.group(1) if og_d else ''
img = og_i.group(1) if og_i else ''

print('Final title:', title)
print('Desc:', desc[:60])
print()
print('Paragraphs:', len(clean), 'chars:', len(''.join(clean)))
print()
print('--- FIRST 5 ---')
for p in clean[:5]: print(p)
print()
print('--- LAST 3 ---')
for p in clean[-3:]: print(p)

# Save
out_raw = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_raw_0525.txt'
out_json = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_struct_0525.json'
with open(out_raw, 'w', encoding='utf-8') as f:
    f.write('Title: ' + title + '\nURL: ' + url + '\nDate: ' + datetime.now().strftime('%Y-%m-%d') + '\n\n' + '\n'.join(clean))
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({'title': title, 'desc': desc, 'url': url, 'img': img, 'date': datetime.now().strftime('%Y-%m-%d'), 'paragraphs': clean}, f, ensure_ascii=False, indent=2)
print('Saved')