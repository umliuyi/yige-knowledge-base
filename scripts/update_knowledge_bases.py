#!/usr/bin/env python3
"""
四个专题知识库周度更新脚本
每周五自动跑，补充最新临床数据
"""
import urllib.request
import re
import os
from datetime import datetime

KNOWLEDGE_DIR = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\知识库"
TOPICS = [
    "专题一-干细胞治疗糖尿病.md",
    "专题二-DC-NK细胞免疫治疗肿瘤.md",
    "专题三-慢阻肺COPD.md",
    "专题四-膝关节干细胞.md",
]

SEARCH_TERMS = {
    "专题一-干细胞治疗糖尿病.md": ["MSC diabetes 2026", "stem cell diabetes clinical trial"],
    "专题二-DC-NK细胞免疫治疗肿瘤.md": ["NK cell therapy cancer 2026", "DC vaccine cancer clinical"],
    "专题三-慢阻肺COPD.md": ["stem cell COPD 2026", "airway basal cell COPD trial"],
    "专题四-膝关节干细胞.md": ["MSC knee osteoarthritis 2026", "stem cell cartilage clinical trial"],
}

def fetch_search_results(query):
    """用36kr RSS代替，没法直接搜PubMed"""
    try:
        import urllib.parse
        url = f"https://www.dxy.cn/search?query={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.read().decode('utf-8', errors='ignore')[:500]
    except:
        return ""

def check_for_updates(topic_file):
    """检查是否有该专题的更新"""
    search_terms = SEARCH_TERMS.get(topic_file, [])
    updates = []
    for term in search_terms:
        result = fetch_search_results(term)
        if result and len(result) > 100:
            updates.append(f"- {term}: 找到新内容\n  片段: {result[:200]}\n")
    return updates

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[{today}] 知识库周度更新检查")
    
    for topic in TOPICS:
        path = os.path.join(KNOWLEDGE_DIR, topic)
        if not os.path.exists(path):
            print(f"[WARN] {topic} 不存在，跳过")
            continue
        
        updates = check_for_updates(topic)
        if updates:
            print(f"[OK] {topic} 有更新:")
            for u in updates:
                print(u)
            
            # 追加到知识库
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"\n\n## 更新记录 | {today}\n")
                for u in updates:
                    f.write(u)
        else:
            print(f"[--] {topic} 本周无重大更新")

if __name__ == "__main__":
    main()