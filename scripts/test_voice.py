# -*- coding: utf-8 -*-
import os, sys, asyncio
sys.path.insert(0, r"C:\Users\Administrator\.openclaw-autoclaw\workspace")
import edge_tts

async def test():
    out = os.path.join(r"C:\Users\Administrator\.openclaw-autoclaw\workspace", "temp_slides", "test_voice.mp3")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    comm = edge_tts.Communicate("欢迎收看大健康早报", "zh-CN-YunyangNeural", rate="+0%", pitch="+0Hz")
    await comm.save(out)
    print("TTS OK:", os.path.getsize(out), "bytes")

asyncio.run(test())