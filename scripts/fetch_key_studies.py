import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def pubmed_fetch_one(pmid):
    fetch_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json'
    req = urllib.request.Request(fetch_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    result = data.get('result', {}).get(pmid, {})
    return result

def pubmed_linkout(pmid):
    return f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/'

# 重点获取详细数据的文章
key_pmids = [
    # 糖尿病
    ('糖尿病MSC-系统综述', '41639868'),
    ('糖尿病MSC-UC-MSC安全有效', '39905688'),
    # NK肿瘤
    ('NK肺癌Meta分析', '41350490'),
    # 膝关节
    ('膝关节MSC系统综述2026', '41863718'),
    ('膝关节脂肪MSC三期KOA', '42049633'),
]

print('Fetching key study details...\n')
for name, pmid in key_pmids:
    result = pubmed_fetch_one(pmid)
    print(f'=== {name} ===')
    print(f'PMID: {pmid}')
    print(f'Title: {result.get("title", "")}')
    print(f'Authors: {[a.get("name","") for a in result.get("authors",[])[:3]]}')
    print(f'Journal: {result.get("source","")} ({result.get("pubdate","")})')
    doi = result.get('elocationid', '')
    if doi.startswith('doi:'):
        doi = doi[4:]
    if doi:
        print(f'DOI: {doi}')
    print(f'PubMed Link: {pubmed_linkout(pmid)}')
    print()

print('Done')