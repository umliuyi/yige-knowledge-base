import urllib.request
import re
import time

kw = ['乐城', '医疗', '健康', '癌症', '肿瘤', '干细胞', '免疫', 'CAR-T', 'ADC', '新药', 'NMPA', '审批']

results = {}

# Test 丁香园
t0 = time.time()
try:
    req = urllib.request.Request('http://www.dxy.cn/rss/home.xml', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=12) as resp:
        raw = resp.read()
        enc = resp.headers.get('Content-Type', '')
        ct = 'gbk' if 'gbk' in enc else 'utf-8'
        content = raw.decode(ct, errors='ignore')
    items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
    health = [it for it in items if any(k in it for k in kw)]
    elapsed = int((time.time() - t0) * 1000)
    results['丁香园'] = {'total': len(items), 'health': len(health), 'ms': elapsed}
except Exception as e:
    results['丁香园'] = {'error': str(e)}

# Test 动脉网
t0 = time.time()
try:
    req = urllib.request.Request('https://vcbeat.top/Rss/News', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=8) as resp:
        raw = resp.read()
        content = raw.decode('utf-8', errors='ignore')
    items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
    health = [it for it in items if any(k in it for k in kw)]
    elapsed = int((time.time() - t0) * 1000)
    results['动脉网'] = {'total': len(items), 'health': len(health), 'ms': elapsed}
    if health:
        for it in health[:3]:
            t = re.search(r'<title>(.*?)</title>', it)
            if t:
                results['动脉网']['sample'] = t.group(1)[:60]
except Exception as e:
    results['动脉网'] = {'error': str(e)}

print("RSS Source Test Results:")
print("=" * 50)
for name, res in results.items():
    if 'error' in res:
        print(f"{name}: FAIL - {res['error']}")
    else:
        print(f"{name}: {res['total']} items, {res['health']} health-related, {res['ms']}ms")
        if 'sample' in res:
            print(f"  Sample: {res['sample']}")