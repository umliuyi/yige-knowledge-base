# -*- coding: utf-8 -*-
"""
信息来源质量评级脚本
读取输入文件，逐行对比专题关键词，输出评级结果
用法: python quality_checker.py <输入文件路径>
"""

import sys
import os
from datetime import datetime

# Windows控制台UTF-8支持
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 四大专题关键词
TOPIC_KEYWORDS = [
    "糖尿病", "肿瘤", "癌症", "COPD", "慢阻肺", "膝关节", "膝盖", "软骨",
    "乐城", "细胞治疗", "免疫治疗", "CAR-T", "NK细胞", "干细胞", "新药", "NMPA"
]

# 强权重关键词（高度相关）
STRONG_KEYWORDS = ["乐城", "细胞治疗", "免疫治疗", "糖尿病", "肿瘤", "CAR-T", "NK细胞", "膝盖", "软骨", "慢阻肺"]

# 弱权重关键词（一般相关）
WEAK_KEYWORDS = ["COPD", "膝关节", "医疗", "健康", "新药", "NMPA", "审批", "膝盖", "软骨", "干细胞"]


def rate_line(line_text):
    """
    对一行内容进行评级
    返回: (rating, reason)
    rating: ✅可信 / ⚠️存疑 / ❌不用
    """
    text = line_text.strip()
    if not text:
        return ("❌不用", "空行")

    # 统计关键词匹配
    matched_strong = [kw for kw in STRONG_KEYWORDS if kw in text]
    matched_weak = [kw for kw in WEAK_KEYWORDS if kw in text]
    matched_topic = [kw for kw in TOPIC_KEYWORDS if kw in text]

    # 判断逻辑
    if not matched_topic:
        return ("❌不用", "无专题关键词匹配")

    if matched_strong:
        # 有强关键词，但需要判断是否为边缘情况
        if "医疗" in matched_weak and len(matched_strong) == 1 and "医疗" in str(matched_weak):
            # 只有"医疗"这一个弱词配强关键词，可能存疑
            return ("⚠️存疑", f"匹配关键词: {', '.join(matched_topic)}，但仅有弱关联词'医疗'")
        return ("✅可信", f"匹配专题关键词: {', '.join(matched_topic)}")

    if matched_weak and not matched_strong:
        # 只有弱关键词
        return ("⚠️存疑", f"仅匹配弱关联词: {', '.join(matched_topic)}，建议人工核实")

    return ("⚠️存疑", f"匹配关键词: {', '.join(matched_topic)}，但无法明确判断")


def main():
    if len(sys.argv) < 2:
        print("用法: python quality_checker.py <输入文件路径>")
        print("示例: python quality_checker.py C:\\temp\\news_list.txt")
        sys.exit(1)

    input_path = sys.argv[1]

    if not os.path.exists(input_path):
        print(f"文件不存在: {input_path}")
        sys.exit(1)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始质量评级...")
    print(f"输入文件: {input_path}")
    print(f"专题关键词: {TOPIC_KEYWORDS}\n")

    # 读取输入文件
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 过滤空行和注释行
    content_lines = [
        (i + 1, line.rstrip("\n\r"))
        for i, line in enumerate(lines)
        if line.strip() and not line.strip().startswith("#")
    ]

    print(f"待评级内容行: {len(content_lines)} 行\n")

    results = []
    for lineno, line_text in content_lines:
        rating, reason = rate_line(line_text)
        results.append((lineno, line_text, rating, reason))

    # 统计
    counts = {"✅可信": 0, "⚠️存疑": 0, "❌不用": 0}
    for _, _, rating, _ in results:
        counts[rating] += 1

    # 生成输出文件名
    input_dir = os.path.dirname(os.path.abspath(input_path))
    input_filename = os.path.splitext(os.path.basename(input_path))[0]
    output_file = os.path.join(input_dir, f"{input_filename}_quality.txt")

    # 写入结果
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# 信息质量评级结果\n")
        f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# 输入文件: {input_path}\n")
        f.write(f"# 专题关键词: {', '.join(TOPIC_KEYWORDS)}\n")
        f.write(f"# 统计: ✅可信 {counts['✅可信']} 条 | ⚠️存疑 {counts['⚠️存疑']} 条 | ❌不用 {counts['❌不用']} 条\n")
        f.write("#" + "="*70 + "\n\n")

        for lineno, line_text, rating, reason in results:
            f.write(f"{rating} [行{lineno}] {reason}\n")
            f.write(f"    {line_text}\n\n")

    print(f"结果已保存到: {output_file}")
    print(f"\n=== 评级统计 ===")
    print(f"✅可信: {counts['✅可信']} 条")
    print(f"⚠️存疑: {counts['⚠️存疑']} 条")
    print(f"❌不用: {counts['❌不用']} 条")

    # 控制台输出结果摘要
    print("\n=== 结果摘要 ===")
    for lineno, line_text, rating, reason in results:
        preview = line_text[:60] + ("..." if len(line_text) > 60 else "")
        print(f"{rating} [行{lineno}] {preview}")


if __name__ == "__main__":
    main()