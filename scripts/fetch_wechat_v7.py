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

# The WeChat page sends meta tags in the HTML page which is GBK encoded.
# But og:title content="..." in the page has the UTF-8 bytes of the title.
# When we decode the whole page as GBK, those UTF-8 bytes become garbled.
# We can recover: find the garbled string in GBK-decoded text,
# find those same bytes in the original raw_bytes, and re-decode as UTF-8.

# Pattern: find og:title in raw_gbk
garbled_pattern = re.search(r'<meta property="og:title" content="([^"]+)"', raw_gbk)
if garbled_pattern:
    garbled = garbled_pattern.group(1)
    print('Garbled:', repr(garbled[:60]))
    # Find position of garbled string in GBK-decoded text
    pos_gbk = raw_gbk.find(garbled)
    if pos_gbk >= 0:
        # Corresponding position in raw_bytes
        # Since raw_gbk[pos_gbk:pos_gbk+len(garbled)] are the GBK bytes,
        # we need to find the same character sequence in raw_bytes
        # The garbled text is GBK encoding of the UTF-8 title
        # Find the byte offset in raw_bytes corresponding to the start of the content attr
        # Search for the start of content="..."
        gbk_attr_start = raw_gbk.find('<meta property="og:title" content="')
        gbk_content_start = raw_gbk.find('"', gbk_attr_start + len('<meta property="og:title" content="'))
        gbk_content_end = raw_gbk.find('"', gbk_content_start + 1)
        # These are character positions in the GBK-decoded string.
        # Convert to byte positions: in GBK, most chars are 2 bytes
        # We need to find the byte offset of the title content in raw_bytes
        # by finding the sequence of bytes that correspond to the title in raw_bytes.
        # Approach: the title "干细..." in UTF-8 is E4 B8 80...
        # Search for that byte pattern in raw_bytes
        target_utf8_bytes = b'\xe4\xb8\x80'  # '干' in UTF-8
        idx = raw_bytes.find(target_utf8_bytes)
        print('UTF-8 "干" found at byte offset:', idx)
        if idx >= 0:
            # Read next 50 bytes as UTF-8 title candidate
            chunk = raw_bytes[idx:idx+100]
            try:
                recovered_title = chunk.decode('utf-8', errors='ignore')
                chinese = re.findall(r'[\u4e00-\u9fff]+', recovered_title)
                if chinese:
                    print('Recovered title words:', ''.join(chinese)[:40])
            except:
                pass

# Also try: find all visible Chinese text in first p/span and use as title
texts = re.findall(r'<(?:p|span)[^>]*>(.*?)</(?:p|span)>', raw_gbk, re.DOTALL)
clean = []
for t in texts:
    txt = re.sub(r'<[^>]+>', '', t).strip()
    if len(txt) >= 10 and re.search(r'[\u4e00-\u9fff]', txt):
        txt = html_module.unescape(txt)
        clean.append(txt)

# Try to find title from og:title in raw_utf8 after unescape
og_t_utf8 = re.search(r'<meta property="og:title" content="([^"]+)"', raw_utf8)
title_candidates = []
if og_t_utf8:
    cand = og_t_utf8.group(1)
    chinese_count = len(re.findall(r'[\u4e00-\u9fff]', cand))
    print(f'UTF-8 og:title ({chinese_count} CJK): {repr(cand[:40])}')
    title_candidates.append((chinese_count, 'utf8', cand))

# From raw_gbk
og_t_gbk = re.search(r'<meta property="og:title" content="([^"]+)"', raw_gbk)
if og_t_gbk:
    cand = og_t_gbk.group(1)
    chinese_count = len(re.findall(r'[\u4e00-\u9fff]', cand))
    print(f'GBK og:title ({chinese_count} CJK): {repr(cand[:40])}')
    title_candidates.append((chinese_count, 'gbk', cand))

# Also try: find h1 
h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', raw_gbk, re.DOTALL)
if h1_m:
    h1_text = re.sub(r'<[^>]+>', '', h1_m.group(1)).strip()
    h1_text = html_module.unescape(h1_text)
    chinese_count = len(re.findall(r'[\u4e00-\u9fff]', h1_text))
    print(f'H1 ({chinese_count} CJK): {repr(h1_text[:40])}')
    title_candidates.append((chinese_count, 'h1', h1_text))

# Pick best candidate
if title_candidates:
    title_candidates.sort(key=lambda x: x[0], reverse=True)
    best_score, best_source, best_title = title_candidates[0]
    print(f'Best title source: {best_source}, score: {best_score}, title: {best_title[:50]}')
else:
    best_title = clean[0] if clean else ''
    print('No title found, using first paragraph')

# Get desc and img from UTF-8 (usually correct)
og_d = re.search(r'<meta property="og:description" content="([^"]+)"', raw_utf8)
og_i = re.search(r'<meta property="og:image" content="([^"]+)"', raw_utf8)
desc = og_d.group(1) if og_d else ''
img = og_i.group(1) if og_i else ''

print()
print('Title:', best_title[:60])
print('Desc:', desc[:60])
print('Paragraphs:', len(clean))
print()
for p in clean[:5]:
    print(p)
print()
for p in clean[-3:]:
    print(p)

# Save
out_raw = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_raw_0525.txt'
out_json = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\wechat_struct_0525.json'
with open(out_raw, 'w', encoding='utf-8') as f:
    f.write('Title: ' + best_title + '\nURL: ' + url + '\nDate: ' + datetime.now().strftime('%Y-%m-%d') + '\n\n' + '\n'.join(clean))
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({'title': best_title, 'desc': desc, 'url': url, 'img': img, 'date': datetime.now().strftime('%Y-%m-%d'), 'paragraphs': clean}, f, ensure_ascii=False, indent=2)
print('Done')