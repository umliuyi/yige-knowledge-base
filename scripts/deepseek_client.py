#!/usr/bin/env python3
"""DeepSeek API 调用工具"""
import urllib.request
import json

API_KEY = "sk-c66ce8dc7e8049d99cb977a978b6095c"
MODEL = "deepseek-chat"
BASE_URL = "https://api.deepseek.com/v1"

def chat(messages, model=None, temperature=0.7, max_tokens=2000):
    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model or MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

def generate(prompt, system=None, temperature=0.7, max_tokens=2000):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    result = chat(messages, temperature=temperature, max_tokens=max_tokens)
    return result["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print("Testing DeepSeek API...")
    try:
        result = generate("Say hello in one sentence.")
        print("OK - API connected!")
        print(result)
    except Exception as e:
        print(f"FAILED: {e}")