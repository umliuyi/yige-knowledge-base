#!/usr/bin/env python3
"""生成早报TTS配音"""

import subprocess
import os
import asyncio

NARRATIONS = [
    "干细胞疗法三大新突破，精算师视角，每日健康资讯。",
    "麦吉尔大学团队开发出一种可立即与宿主血管整合的胰岛素分泌细胞移植装置，绕过传统移植需先建立血供的难题，同时降低免疫排异风险。",
    "瑞典卡罗林斯卡医学院研究团队在多个干细胞系中稳定产生高质量胰岛素分泌细胞，移植后逆转糖尿病并维持血糖调控数月，为临床转化提供支撑。",
    "Sana Biotechnology公司的UP421基因编辑贝塔细胞疗法，在Ⅰ型糖尿病患者移植后14个月仍持续存活并产生胰岛素，全程无需免疫抑制剂。这一结果证明无排异贝塔细胞疗法路径可行。",
    "关注我，用精算逻辑管理健康风险。"
]

async def main():
    output_dir = "C:/Users/Administrator/.openclaw-autoclaw/workspace/covers_v4"
    audio_dir = output_dir + "/audio"
    os.makedirs(audio_dir, exist_ok=True)
    
    for i, text in enumerate(NARRATIONS):
        output_file = f"{audio_dir}/narration_{i:02d}.mp3"
        cmd = [
            "edge-tts",
            "-v", "zh-CN-YunxiNeural",
            "-t", text,
            "--write-media", output_file
        ]
        print(f"生成配音 {i+1}: {text[:20]}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  成功: {output_file}")
        else:
            print(f"  失败: {result.stderr}")
    
    print("\n配音生成完成!")

if __name__ == "__main__":
    asyncio.run(main())
