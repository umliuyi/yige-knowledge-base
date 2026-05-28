
# -*- coding: utf-8 -*-
"""由 pipeline 自动生成 - 2026-05-27"""
from daily_news_slides import *

if __name__ == "__main__":
    print("生成早报幻灯片 - 2026-05-27 ...")
    slides = []

    # 封面
    slides.append(make_cover(
        "2026-05-27",
        ""
    ))

    # 新闻页
    for i, title in enumerate(items[:5], 1):
        slides.append(make_news_slide(
            i, 5,
            "大健康",
            title[:30],
            ["• 详见今日早报内容", "• 关注我了解更多"]
        ))

    # 结尾
    slides.append(make_closing())
    print(f"共生成 7 页幻灯片")
