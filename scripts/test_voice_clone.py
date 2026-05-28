import requests, os, json

API_KEY = 'sk-api-6UprnKT6vp6gFgoquJtFx3FKcC-03AJ3E8wv6BRZNiDPh9VwWoWOmer_L-F14JtIsTghCbhEcKDK1jQpKlpnoeLOoTmXW46Z7P5AJ5UaKdKvIl9wRuaNJzU'
AUDIO_FILE = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\voice_sample\liu_yi_voice.m4a'

print('=== Step 1: Upload audio for voice cloning ===')
print('File size:', os.path.getsize(AUDIO_FILE) // 1024, 'KB')

# Step 1: Upload
with open(AUDIO_FILE, 'rb') as f:
    files = {'file': ('liu_yi_voice.m4a', f, 'audio/mp4')}
    data = {'purpose': 'voice_clone'}
    headers = {'Authorization': 'Bearer ' + API_KEY}
    r = requests.post('https://api.minimaxi.com/v1/files/upload',
                      headers=headers, data=data, files=files, timeout=30)
print('Upload status:', r.status_code)
print('Response:', r.text[:600])

if r.status_code == 200:
    resp = r.json()
    file_id = resp.get('file', {}).get('file_id')
    print('file_id:', file_id)
    
    # Step 2: Clone the voice
    if file_id:
        print()
        print('=== Step 2: Clone voice ===')
        clone_data = {
            'voice_type': 'voice_clone',
            'file_id': file_id,
            'speed_factor': 1.0
        }
        r2 = requests.post('https://api.minimaxi.com/v1/clone_voice',
                          headers=headers, json=clone_data, timeout=30)
        print('Clone status:', r2.status_code)
        print('Response:', r2.text[:600])
else:
    print('Upload failed')
