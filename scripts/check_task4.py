import urllib.request
import json

api_key = "sk-api-UTv9N1XfUYjJLBWtHRhSnR45eCaRlTyqOBaf4QSV2zV5SZSfFksEihkHaqdkuH44WLHVwveZnPIJV0BwDGPVFeZcg6VQb0eJErx8T0uyhJdd_oISKuu4gBk"

# Try different endpoints and params
tests = [
    ("GET", "https://api.minimax.chat/v1/query/video_generation?task_id=750423112241001267", None),
    ("GET", "https://api.minimax.chat/v1/query/video_generation?group_id=750423112241001267", None),
    ("GET", "https://api.minimax.chat/v1/video_generation?task_id=750423112241001267", None),
]

for method, url, data in tests:
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    if data:
        req.data = data.encode()
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = resp.read().decode("utf-8")
            print(f"URL: {url}")
            print(f"Status: {resp.status}")
            print(f"Response: {result[:500]}")
            print("---")
    except urllib.error.HTTPError as e:
        print(f"URL: {url}")
        print(f"HTTP Error: {e.code}")
        print(f"Body: {e.read().decode('utf-8')[:500]}")
        print("---")
    except Exception as e:
        print(f"URL: {url}")
        print(f"Error: {e}")
        print("---")