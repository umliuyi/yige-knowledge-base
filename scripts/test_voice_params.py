# -*- coding: utf-8 -*-
"""测试edge-tts配音参数"""
import asyncio, os
import edge_tts

async def main():
    text = '各位朋友大家好，这里是刘一的健康早报。今天有3条重要资讯，干货很多。'
    out_dir = r'C:\Users\Administrator\.openclaw-autoclaw\media'
    os.makedirs(out_dir, exist_ok=True)
    
    print("=== 语速测试 ===")
    for rate in ['-10%', '+0%', '+10%']:
        fname = 'voice_r' + rate.replace('%','p').replace('+','plus').replace('-','minus') + '.mp3'
        out = os.path.join(out_dir, fname)
        try:
            tts = edge_tts.Communicate(text=text, voice='zh-CN-YunxiNeural', rate=rate)
            await tts.save(out)
            print('rate=' + rate + ' OK ' + str(os.path.getsize(out)//1024) + 'KB')
        except Exception as e:
            print('rate=' + rate + ' ERROR: ' + str(e)[:80])
    
    print("=== 声音测试 ===")
    for voice in ['zh-CN-YunxiNeural', 'zh-CN-XiaoxiaoNeural', 'zh-CN-YunyangNeural']:
        out = os.path.join(out_dir, 'voice_' + voice + '.mp3')
        try:
            tts = edge_tts.Communicate(text=text, voice=voice, rate='+0%')
            await tts.save(out)
            print('voice=' + voice + ' OK ' + str(os.path.getsize(out)//1024) + 'KB')
        except Exception as e:
            print('voice=' + voice + ' ERROR: ' + str(e)[:80])
    
    print("=== 完成 ===")

asyncio.run(main())
