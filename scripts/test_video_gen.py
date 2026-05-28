import requests, json, os

API_KEY = 'sk-api-6UprnKT6vp6gFgoquJtFx3FKcC-03AJ3E8wv6BRZNiDPh9VwWoWOmer_L-F14JtIsTghCbhEcKDK1jQpKlpnoeLOoTmXW46Z7P5AJ5UaKdKvIl9wRuaNJzU'
headers = {'Authorization': 'Bearer ' + API_KEY, 'Content-Type': 'application/json'}

# Check video generation endpoints
print('=== Checking video generation ===')
r = requests.get('https://api.minimax.io/v1/video_generation', headers=headers, timeout=10)
print('GET video_generation:', r.status_code, r.text[:300])

# Try I2V (image to video)
# First upload an image
img_path = r'C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11-v3\pg0.png'
print('Image size:', os.path.getsize(img_path) // 1024, 'KB')

# Upload image first
print()
print('=== Upload image for I2V ===')
with open(img_path, 'rb') as f:
    files = {'file': ('slide.png', f, 'image/png')}
    data = {'purpose': 'video_generate'}
    r = requests.post('https://api.minimaxi.com/v1/files/upload',
                      headers={'Authorization': 'Bearer ' + API_KEY},
                      data=data, files=files, timeout=30)
print('Upload image status:', r.status_code)
print('Response:', r.text[:500])
