#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PubMed文献快速采集 - 四大专题最新文献（摘要版）
策略：用esummary快速获取，efetch只取top2摘要，控制在3个请求内完成"""
import urllib.request
import urllib.parse
import json
import ssl
import os
import re
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TODAY = datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = r"C:\Users\Administrator\.openclaw-autoclaw\workspace\growth\daily\ccfa1206"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 四大专题搜索词（扩展版：用 OR 连接同义词，扩大覆盖面）
QUERIES = [
    (
        "糖尿病干细胞",
        "(stem cell[Title/Abstract] OR MSC[Title/Abstract] OR mesenchymal stromal[Title/Abstract] OR adipose-derived stem[Title/Abstract]) AND (diabetes[Title/Abstract] OR diabetic[Title/Abstract] OR HbA1c[Title/Abstract] OR glucose metabolism[Title/Abstract])"
    ),
    (
        "肿瘤免疫细胞",
        "(NK cell[Title/Abstract] OR natural killer[Title/Abstract] OR T cell[Title/Abstract] OR CAR-T[Title/Abstract] OR immunotherapy[Title/Abstract]) AND (cancer[Title/Abstract] OR tumor[Title/Abstract] OR carcinoma[Title/Abstract] OR malignancy[Title/Abstract])"
    ),
    (
        "慢阻肺干细胞",
        "(stem cell[Title/Abstract] OR MSC[Title/Abstract] OR endothelial progenitor[Title/Abstract]) AND (COPD[Title/Abstract] OR chronic obstructive pulmonary[Title/Abstract] OR emphysema[Title/Abstract] OR chronic bronchitis[Title/Abstract])"
    ),
    (
        "膝关节干细胞",
        "(stem cell[Title/Abstract] OR MSC[Title/Abstract] OR stromal vascular fraction[Title/Abstract]) AND (knee[Title/Abstract] OR osteoarthritis[Title/Abstract] OR cartilage[Title/Abstract] OR joint[Title/Abstract])"
    ),
]

def esearch(query, max_results=3):
    url = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        f"?db=pubmed&term={urllib.parse.quote(query)}"
        f"&retmax={max_results}&retmode=json&sort=date"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("esearchresult", {}).get("idlist", [])

def esummary(pmids):
    if not pmids:
        return {}
    ids_str = ",".join(str(p) for p in pmids)
    url = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        f"?db=pubmed&id={ids_str}&retmode=json"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    results = {}
    for pid in pmids:
        r = data.get("result", {}).get(str(pid), {})
        doi_el = r.get("elocationid", "")
        doi = doi_el[4:] if doi_el.startswith("doi:") else ""
        results[pid] = {
            "title": r.get("title", ""),
            "journal": r.get("source", ""),
            "pubdate": r.get("pubdate", ""),
            "doi": doi,
            "pmid": str(pid),
        }
    return results

def efetch_abstract(pmid):
    url = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        f"?db=pubmed&id={pmid}&retmode=xml"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
        content = resp.read().decode("utf-8", errors="ignore")
    abstract_m = re.search(r"<AbstractText[^>]*>(.*?)</AbstractText>", content, re.DOTALL)
    return abstract_m.group(1).strip() if abstract_m else ""

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] PubMed文献采集开始...")
    all_results = []

    for topic, query in QUERIES:
        print(f"\n[{topic}] 搜索: {query[:40]}...")
        ids = esearch(query, max_results=3)
        if not ids:
            print(f"  无结果")
            continue
        print(f"  PMID: {ids}")
        papers = esummary(ids)

        # 只取第一个有DOI的文献获取摘要
        abstract = ""
        for pid in ids:
            p = papers.get(int(pid), {})
            if p.get("doi"):
                abstract = efetch_abstract(pid)
                print(f"  有摘要: PMID:{pid} | {p['journal']} {p['pubdate']}")
                print(f"  {p['title'][:60]}")
                break

        for pid in ids:
            p = papers.get(int(pid), {})
            all_results.append({
                "topic": topic,
                "pmid": p.get("pmid", ""),
                "title": p.get("title", ""),
                "journal": p.get("journal", ""),
                "pubdate": p.get("pubdate", ""),
                "doi": p.get("doi", ""),
                "abstract": abstract if p.get("pmid") == pid else "",
            })

    # 写文件
    out_file = os.path.join(OUTPUT_DIR, f"pubmed_results_{TODAY}.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"# PubMed四大专题文献 | {TODAY}\n\n")
        current_topic = ""
        for r in all_results:
            if r["topic"] != current_topic:
                f.write(f"\n## {r['topic']}\n")
                current_topic = r["topic"]
            f.write(f"[{r['journal']} {r['pubdate']}] PMID:{r['pmid']} | DOI:{r['doi'] or '无'}\n")
            f.write(f"{r['title']}\n")
            if r.get("abstract"):
                f.write(f"摘要: {r['abstract'][:200]}\n")
            f.write("\n")

    print(f"\n[OK] 共{len(all_results)}篇文献，保存到: {out_file}")
    return out_file

if __name__ == "__main__":
    main()
