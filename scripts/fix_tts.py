import asyncio, os
from pathlib import Path

SLIDES_DIR = Path(r"C:\Users\Administrator\Downloads\videos\daily_news")

audio_texts = [
    ("audio_00.mp3", "精算师视角，大健康早报。2026年5月26日。今天聊两件事：糖尿病和膝关节。"),
    ("audio_01.mp3", "我算过一个50岁糖尿病人的账。到80岁，终生治疗费用约50到80万。其中60%花在并发症上：心梗、脑梗、肾衰。MSC治疗，17.94万一个疗程。文献数据：91例随机对照，MSC组糖化血红蛋白从8.5%降至6.9%，胰岛素用量减少50%。17.94万，换5年不得并发症。算清楚了吗？"),
    ("audio_02.mp3", "三项临床研究支撑这个判断。第一项：Cai等人2023年发表，91例随机对照，MSC组糖化血红蛋白从8.5%降到6.9%，胰岛素用量减少50%。第二项：Bhansali等人2021年Meta分析，5项RCT271例患者，空腹血糖显著降低，胰岛功能改善。第三项：张等人2022年研究，53例患者，30例脱离胰岛素，23例减量超过50%。"),
    ("audio_03.mp3", "膝盖不好的病人，最终往往走到关节置换。关节置换，6到10万，寿命15到20年。MSC治疗，3.6万一针，适合KL 2到3期患者。这个阶段治疗，能让软骨再生，延缓置换。3.6万换少做一次关节置换，节省6到10万。精算师的账，帮你算清楚。"),
    ("audio_04.mp3", "糖尿病和膝关节，看似两个病，其实是一个逻辑。得病之后，钱花在并发症上、花在最后那一步手术上。干细胞的作用，是让你不走那一步。这就是精算师视角下的健康决策。关注我，用精算师的眼光，看懂大健康。"),
]

async def gen_tts(out_path, text):
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, "zh-CN-YunxiNeural")
        await communicate.save(out_path)
        return os.path.exists(out_path)
    except Exception as e:
        print(f"  TTS error: {e}")
        return False

async def main():
    for fname, text in audio_texts:
        afile = SLIDES_DIR / fname
        ok = await gen_tts(str(afile), text)
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {fname} ({os.path.getsize(afile) if ok and os.path.exists(afile) else 0} bytes)")
        await asyncio.sleep(0.5)

asyncio.run(main())
print("TTS done")