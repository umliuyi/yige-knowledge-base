import urllib.request
import urllib.error
import json
import time
import os

api_key = "sk-api-UTv9N1XfUYjJLBWtHRhSnR45eCaRlTyqOBaf4QSV2zV5SZSfFksEihkHaqdkuH44WLHVwveZnPIJV0BwDGPVFeZcg6VQb0eJErx8T0uyhJdd_oISKuu4gBk"
task_id = "402054860718324"

print(f"Polling task {task_id}...")

for i in range(20):
    query_url = f"https://api.minimax.chat/v1/query/video_generation?task_id={task_id}"
    req = urllib.request.Request(query_url)
    req.add_header("Authorization", f"Bearer {api_key}")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            status = result.get("status", "")
            file_id = result.get("file_id", "")
            print(f"[{i+1}] Status: {status}, file_id: {file_id}")
            
            if status == "Complete" and file_id:
                print(f"✅ Video ready! file_id: {file_id}")
                # Try to download
                download_url = f"https://api.minimax.chat/v1/files/retrieve?file_id={file_id}"
                req2 = urllib.request.Request(download_url)
                req2.add_header("Authorization", f"Bearer {api_key}")
                try:
                    with urllib.request.urlopen(req2, timeout=60) as resp2:
                        content = resp2.read()
                        out_path = r"C:\Users\Administrator\Downloads\hailuo_test.mp4"
                        with open(out_path, "wb") as f:
                            f.write(content)
                        print(f"✅ Downloaded to {out_path}, size: {len(content)} bytes")
                except urllib.error.HTTPError as e2:
                    print(f"Download HTTP Error: {e2.code}")
                    print(f"Body: {e2.read().decode('utf-8')[:500]}")
                break
            elif status in ["Failed", "fail"]:
                print("❌ Task failed")
                break
    except urllib.error.HTTPError as e:
        print(f"Query HTTP Error: {e.code}")
        print(f"Body: {e.read().decode('utf-8')[:300]}")
        break
    
    time.sleep(10)
else:
    print("⏰ Timeout after 20 attempts")