import urllib.request
import json

api_key = "sk-api-UTv9N1XfUYjJLBWtHRhSnR45eCaRlTyqOBaf4QSV2zV5SZSfFksEihkHaqdkuH44WLHVwveZnPIJV0BwDGPVFeZcg6VQb0eJErx8T0uyhJdd_oISKuu4gBk"

# Submit a new test task
submit_url = "https://api.minimax.chat/v1/video_generation"

payload = json.dumps({
    "model": "MiniMax-Hailuo-2.3",
    "prompt": "A doctor in a modern hospital in Hainan, China, explaining medical innovation",
    "duration": 6
}).encode()

req = urllib.request.Request(submit_url, data=payload)
req.add_header("Authorization", f"Bearer {api_key}")
req.add_header("Content-Type", "application/json")

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print("Submit response:", json.dumps(result, indent=2))
        task_id = result.get("task_id") or result.get("data", {}).get("task_id")
        print("Task ID:", task_id)
        
        if task_id:
            # Wait and query
            import time
            time.sleep(5)
            
            query_url = f"https://api.minimax.chat/v1/query/video_generation?task_id={task_id}"
            req2 = urllib.request.Request(query_url)
            req2.add_header("Authorization", f"Bearer {api_key}")
            with urllib.request.urlopen(req2, timeout=30) as resp2:
                query_result = json.loads(resp2.read().decode("utf-8"))
                print("Query response:", json.dumps(query_result, indent=2))
                
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Body:", e.read().decode("utf-8")[:1000])
except Exception as e:
    print("Error:", e)