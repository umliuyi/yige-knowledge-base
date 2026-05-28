# -*- coding: utf-8 -*-
"""
用 edge-tts 为每页生成配音
"""
import asyncio, os

OUTPUT_DIR = r"C:\Users\Administrator\Downloads\videos\daily_news\2026-05-11"

# 每页配音文本
voice_texts = [
    ("cover", "大健康早报，2026年5月11日，星期一，医疗健康每日资讯"),
    ("01", "新闻一，正大天晴与葛兰素史克达成重磅战略合作，乙肝新药加速入华。中国生物制药旗下正大天晴，与全球制药巨头葛兰素史克达成独家战略合作，共同推动乙肝治疗药物bepirovirsen在中国内地的上市进程。该药属于反义寡核苷酸类创新药，针对慢性乙肝患者。中国乙肝感染者约7000万，用药需求巨大。"),
    ("02", "新闻二，美图公司AI无痕改字功能落地，支持中英日韩泰五语种。美图影像研究院6篇论文同时被ICLR、CVPR、ICML三大国际顶会录用，其中无痕改字AI功能已上线美图设计室App和美图秀秀PC版，突破传统改字的预设词表限制，能保持字体风格与画面质感一致。"),
    ("03", "新闻三，创业板指突破3900点，创逾10年新高。A股午盘创业板指涨近百分之2.75，突破3900点，为2015年6月以来新高。科创50指数涨逾百分之5，半导体、电脑硬件板块领涨，澜起科技涨停，涨超20%，兆易创新涨超12%，医疗科技板块同步走强。"),
    ("04", "新闻四，进出口化妆品新规12月1日起施行，上海率先试点电子标签。海关总署发布新修订的进出口化妆品检验检疫监督管理办法，新办法将于今年12月1日起正式施行。上海市率先启动进口化妆品电子标签试点，消费者可扫码验真，利好海淘和代购人群。"),
    ("05", "新闻五，广东省新增6款生成式AI服务登记，累计已达53款。据网信广东发布，截至2026年5月11日，广东省新增6款生成式人工智能服务完成登记，体现各地持续推进AI监管规范化，AI服务进入合规发展新阶段。"),
    ("99", "关注我，刘一，精算师聊健康，每早8点30，大健康资讯早知道。"),
]

async def generate_voice(slug, text):
    try:
        import edge_tts
    except ImportError:
        print("  edge-tts not installed, skipping voice generation")
        return None

    mp3_path = os.path.join(OUTPUT_DIR, f"{slug}.mp3")
    print(f"  [配音 {slug}] 生成中...")
    try:
        communicate = edge_tts.Communicate(text, voice="zh-CN-XiaoxiaoNeural")
        await communicate.save(mp3_path)
        print(f"  [配音 {slug}] 已保存: {mp3_path}")
        return mp3_path
    except Exception as e:
        print(f"  [配音 {slug}] 失败: {e}")
        return None

async def main():
    print("开始生成配音...")
    for slug, text in voice_texts:
        await generate_voice(slug, text)
    print("\n配音生成完成！")

if __name__ == "__main__":
    asyncio.run(main())