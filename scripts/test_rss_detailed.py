import urllib.request
import re
import time

kw = ['乐城', '医疗', '健康', '癌症', '肿瘤', '干细胞', '免疫', 'CAR-T', 'ADC', '新药', 'NMPA', '审批']

# Test 丁香园 raw content
req = urllib.request.Request('http://www.dxy.cn/rss/home.xml', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=12) as resp:
    raw = resp.read()
    ct = resp.headers.get('Content-Type', '')
print(f"丁香园 Content-Type: {ct}")
print(f"丁香园 raw size: {len(raw)} bytes")
# Try utf-8 first
for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
    try:
        content = raw.decode(enc, errors='ignore')
        print(f"  {enc}: starts with '{content[:50]}'")
        # Count items
        items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
        if items:
            print(f"  {enc}: {len(items)} items found!")
            t = re.search(r'<title>(.*?)</title>', items[0])
            if t:
                print(f"  First title: {t.group(1)[:60]}")
            break
    except Exception as e:
        print(f"  {enc}: FAIL - {e}")

# Test 动脉网 raw content
req = urllib.request.Request('https://vcbeat.top/Rss/News', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=8) as resp:
    raw = resp.read()
    ct = resp.headers.get('Content-Type', '')
print(f"\n动脉网 Content-Type: {ct}")
print(f"动脉网 raw size: {len(raw)} bytes")
for enc in ['utf-8', 'gbk', 'gb18030']:
    try:
        content = raw.decode(enc, errors='ignore')
        print(f"  {enc}: starts with '{content[:50]}'")
        items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
        if items:
            print(f"  {enc}: {len(items)} items found!")
            break
    except Exception as e:
        print(f"  {enc}: FAIL - {e}")