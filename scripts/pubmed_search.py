import urllib.request
import urllib.parse
import json
import ssl

# 忽略SSL验证（Windows环境问题）
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def pubmed_search(query, max_results=5):
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    search_url = base_url + 'esearch.fcgi?db=pubmed&term=' + urllib.parse.quote(query) + '&retmax=' + str(max_results) + '&retmode=json'
    req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
        search_data = json.loads(resp.read().decode('utf-8'))
    ids = search_data.get('esearchresult', {}).get('idlist', [])
    return ids

def pubmed_fetch(pmids):
    if not pmids:
        return []
    ids_str = ','.join(pmids[:5])
    fetch_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids_str}&retmode=json'
    req = urllib.request.Request(fetch_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    results = []
    for pid in pmids[:5]:
        result = data.get('result', {}).get(pid, {})
        title = result.get('title', '')
        authors = [a.get('name', '') for a in result.get('authors', [])[:3]]
        source = result.get('source', '')
        pubdate = result.get('pubdate', '')
        vol = result.get('volume', '')
        pages = result.get('pages', '')
        doi = result.get('elocationid', '')
        if doi.startswith('doi:'):
            doi = doi[4:]
        results.append({
            'pmid': pid,
            'title': title,
            'authors': ', '.join(authors),
            'source': source,
            'pubdate': pubdate,
            'vol': vol,
            'pages': pages,
            'doi': doi
        })
    return results

queries = [
    ('糖尿病MSC', 'mesenchymal stem cell type 2 diabetes HbA1c randomized controlled trial'),
    ('NK肿瘤', 'NK cell immunotherapy solid tumor randomized'),
    ('慢阻肺干细胞', 'stem cell COPD pulmonary function randomized'),
    ('膝关节MSC', 'mesenchymal stem cell knee osteoarthritis randomized controlled trial'),
]

for name, query in queries:
    print(f'\n=== {name}: {query[:50]} ===')
    try:
        ids = pubmed_search(query, max_results=3)
        if not ids:
            print('  No results found')
            continue
        articles = pubmed_fetch(ids)
        for art in articles:
            print(f"  PMID: {art['pmid']}")
            print(f"  Title: {art['title'][:120]}")
            print(f"  Authors: {art['authors']}")
            print(f"  Journal: {art['source']} ({art['pubdate']}) Vol:{art['vol']} Pages:{art['pages']}")
            if art['doi']:
                print(f"  DOI: {art['doi']}")
            print()
    except Exception as e:
        print(f'  ERROR: {e}')

print('\nDone')