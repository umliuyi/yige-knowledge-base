import urllib.request, json, time, os

API_KEY = "sk-api-UTv9N1XfUYjJLBWtHRhSnR45eCaRlTyqOBaf4QSV2zV5SZSfFksEihkHaqdkuH44WLHVwveZnPIJV0BwDGPVFeZcg6VQb0eJErx8T0uyhJdd_oISKuu4gBk"

payload = {
    "prompt": "Aerial drone view of tropical Hainan coastline at golden hour, modern medical buildings in Lecheng Pilot Zone, palm trees, golden sunlight, cinematic drone shot, documentary style, lush greenery",
    "model": "MiniMax-Hailuo-2.3",
    "duration": 6,
    "resolution": "768P"
}

data = json.dumps(payload).encode()
req = urllib.request.Request(
    "https://api.minimaxi.com/v1/video_generation",
    data=data,
    headers={"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"}
)

print("Submitting video generation request...")
with urllib.request.urlopen(req, timeout=30) as resp:
    result = json.loads(resp.read())
    print("SUBMIT_RAW:", json.dumps(result))
    print("SUBMIT_OK:", json.dumps(result)[:500])

# 兼容两种响应格式
task_id = result.get("data", {}).get("task_id") or result.get("task_id")
print("Extracted task_id:", task_id)

if not task_id:
    print("No task_id found in response!")
else:
    print("Polling task_id:", task_id)
    for i in range(30):
        time.sleep(10)
        # 正确的查询端点: GET /v1/video_generation/query?task_id=xxx
        query_url = f"https://api.minimaxi.com/v1/video_generation/query?task_id={task_id}"
        try:
            req2 = urllib.request.Request(
                query_url,
                headers={"Authorization": "Bearer " + API_KEY}
            )
            with urllib.request.urlopen(req2, timeout=15) as resp2:
                r2 = json.loads(resp2.read())
                status = r2.get("data", {}).get("status") or r2.get("status")
                print(f"Check {i+1}: status={status} | resp={json.dumps(r2)[:300]}")
                if status == "success":
                    file_url = r2.get("data", {}).get("file_url")
                    print(f"SUCCESS! file_url: {file_url}")
                    if file_url:
                        output_path = r"C:\Users\Administrator\.openclaw-autoclaw\media\test_cover.mp4"
                        print(f"Downloading video to {output_path}...")
                        urllib.request.urlretrieve(file_url, output_path)
                        fs = os.path.getsize(output_path)
                        print(f"Download complete: {output_path} ({fs} bytes)")
                    break
                elif status == "failed":
                    print(f"FAILED: {json.dumps(r2)}")
                    break
                # else: processing, continue polling
        except Exception as e:
            print(f"Check {i+1}: ERROR: {e}")
    else:
        print("Timeout: 30 checks reached, task not completed.")
