import urllib.request
import urllib.parse
import json

print("Testing search APIs...")

# Test DuckDuckGo (no key needed)
try:
    params = urllib.parse.urlencode({
        'q': '乐城 医疗 新闻',
        'format': 'json',
        'no_html': '1'
    })
    url = 'https://api.duckduckgo.com/?' + params
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        results = data.get('RelatedTopics', [])[:5]
        print(f'DuckDuckGo OK: {len(results)} results')
        for r in results:
            text = r.get('Text', '')
            if text:
                print(f'  - {text[:80]}')
except Exception as e:
    print(f'DuckDuckGo FAIL: {e}')

# Test Bing Search
try:
    query = urllib.parse.urlencode({'q': '乐城 医疗 新闻', 'count': 3})
    url = 'https://api.bing.microsoft.com/v7.0/search?' + query
    req = urllib.request.Request(url, headers={'Ocp-Apim-Subscription-Key': 'test_key'})
    with urllib.request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        pages = data.get('webPages', {}).get('value', [])[:3]
        print(f'Bing OK: {len(pages)} results')
except Exception as e:
    print(f'Bing FAIL: {e}')
