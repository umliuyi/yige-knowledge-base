#!/usr/bin/env python3
"""生成视频完整配音"""
import asyncio, edge_tts, os

OUTPUT = r"C:\Users\Administrator\Downloads\voiceover.mp3"

TEXT = """我叫刘一，精算师。做了15年金融，我算过无数家庭的财务风险——大病来了，有几个家庭能承受得住？然后我发现了一件很残忍的事。

2023年，我离开金融行业，去了海南乐城。很多人问我：你疯了吗？

我给你们算个数。2023年，中国新增癌症患者480万。其中不到30%的人，能用到新药。为什么？两个原因：第一，新药在美国、欧洲、日本上市，但中国还没批；第二，用得起。一个新药，年费用往往是家庭收入的5到10倍。普通家庭，一病返贫。

我做了15年精算。我帮人算过养老账、风险账、教育金账。但我算来算去，发现一件事：健康的人不算账，生病的人才算。而算的时候，往往已经晚了。

所以我去乐城，不是转型，是转身。乐城有中国唯一的"医疗特区"政策。海外已上市的新药，在乐城可以第一时间用。我做的事，是把这件事变得普通家庭也能触及。

如果你或家人正在经历"有病难医"——关注我，我帮你算清楚这笔账。刘一｜精算师聊健康，我们下条见。"""

async def main():
    print("正在生成配音...")
    communicate = edge_tts.Communicate(TEXT, "zh-CN-YunxiNeural")
    await communicate.save(OUTPUT)
    size = os.path.getsize(OUTPUT)
    print(f"配音已生成: {OUTPUT} ({size} bytes)")

if __name__ == "__main__":
    asyncio.run(main())
