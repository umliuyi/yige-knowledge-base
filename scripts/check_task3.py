import urllib.request
import urllib.parse
import json

api_key = "sk-api-UTv9N1XfUYjJLBWtHRhSnR45eCaRlTyqOBaf4QSV2zV5SZSfFksEihkHaqdkuH44WLHVwveZnPIJV0BwDGPVFeZcg6VQb0eJErx8T0uyhJdd_oISKuu4gBk"
task_id = "750423112241001267"

url = f"https://api.minimax.chat/v1/query/video_generation?task_id={task_id}"

req = urllib.request.Request(url)
req.add_header("Authorization", f"Bearer {api_key}")
req.add_header("Content-Type", "application/json")

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read().decode("utf-8")
        print("Status:", resp.status)
        print("Response:", data[:3000])
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Body:", e.read().decode("utf-8")[:1000])
except Exception as e:
    print("Error:", e)