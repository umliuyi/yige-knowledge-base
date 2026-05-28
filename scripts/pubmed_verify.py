#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import ssl
import sys
import os
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TODAY = datetime.now().strftime("%Y-%m-%d")

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('utf-8', errors='replace').decode('utf-8'))

def pubmed_summary(pmids):
    if not pmids:
        return []
    ids_str = ','.join(str(p) for p in pmids)
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids_str}&retmode=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    results = []
    for pid in pmids:
        r = data.get('result', {}).get(str(pid), {})
        doi = r.get('elocationid', '')
        if doi.startswith('doi:'):
            doi = doi[4:]
        results.append({
            'pmid': str(pid),
            'title': r.get('title', ''),
            'authors': ', '.join(a.get('name', '') for a in r.get('authors', [])[:3]),
            'journal': r.get('source', ''),
            'pubdate': r.get('pubdate', ''),
            'doi': doi,
        })
    return results

def is_english(journal):
    non_eng = ['\u4e2d\u534e', '\u5b66\u62a5', '\u533b\u5b66', '\u4e2d\u56fd']
    return not any(x in journal for x in non_eng)

def grade_paper(p):
    has_doi = bool(p['doi'])
    is_eng = is_english(p['journal'])
    if has_doi and is_eng:
        return '[OK]'
    elif has_doi:
        return '[WARN]'
    else:
        return '[DROP]'

def main():
    if len(sys.argv) < 2:
        print('[用法] python pubmed_verify.py PMID1 PMID2 ...')
        print('[示例] python pubmed_verify.py 41639868 41350490 41863718')
        return

    pmids = [int(p.strip()) for p in sys.argv[1:] if p.strip().isdigit()]
    if not pmids:
        print('[ERROR] no valid PMIDs found')
        return

    safe_print(f'[{datetime.now().strftime("%H:%M:%S")}] Verifying {len(pmids)} PMIDs...')

    papers = pubmed_summary(pmids)

    out_lines = [f'# PubMed Verification | {TODAY}\n']
    out_lines.append(f'# PMIDs: {", ".join(str(p) for p in pmids)}\n\n')

    passed = 0
    for p in papers:
        g = grade_paper(p)
        if g == '[OK]':
            passed += 1
        safe_print(f'{g} PMID:{p["pmid"]} | {p["journal"]} ({p["pubdate"]})')
        safe_print(f'   {p["title"][:100]}')
        safe_print(f'   DOI: {p["doi"] or "none"}')
        out_lines.append(f'{g} PMID:{p["pmid"]} | {p["journal"]} ({p["pubdate"]})\n')
        out_lines.append(f'   {p["title"]}\n')
        out_lines.append(f'   DOI: {p["doi"] or "none"}\n\n')

    safe_print(f'\nPassed: {passed}/{len(papers)}')

    out_file = os.path.join(os.getcwd(), 'pubmed_verify_results.txt')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)
    safe_print(f'[OK] Saved to: {out_file}')

if __name__ == '__main__':
    main()
