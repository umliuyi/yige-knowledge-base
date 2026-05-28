#!/usr/bin/env python3
"""
可灵AI图片自动下载脚本
从资产管理页面提取最新生成的图片并下载

前提：浏览器已打开 klingai.com 并生成了图片

浏览器执行步骤：
1. 打开 https://klingai.com/app/user-assets/materials?ac=1
2. 执行JS提取图片URL:
   imgs = document.querySelectorAll('img[src*="kling"]');
   if(imgs[0]) { console.log(imgs[0].src.replace('w_360','w_2160').replace('h_478','h_2880')); }
3. 将URL复制给此脚本下载
"""
import urllib.request
import sys
import os

def download_image(url, output_path):
    """下载图片"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://klingai.com/'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    with open(output_path, 'wb') as f:
        f.write(data)
    return len(data)

def main():
    if len(sys.argv) < 2:
        print("用法: python kling_download.py <图片URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    filename = url.split('/')[-1].split('?')[0] + '.png'
    output = os.path.join(r"C:\Users\Administrator\.openclaw-autoclaw\workspace", filename)
    
    print(f"下载: {url[:80]}...")
    size = download_image(url, output)
    print(f"完成: {output} ({size} bytes)")

if __name__ == "__main__":
    main()
