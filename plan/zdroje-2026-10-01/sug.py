import requests,json,sys,time,urllib.parse
S=requests.Session()
seeds=[l.strip() for l in open(sys.argv[1]) if l.strip()]
out={}
for q in seeds:
    g=S.get('https://suggestqueries.google.com/complete/search',params={'client':'firefox','hl':'cs','gl':'cz','q':q},timeout=20).json()[1]
    sz=S.get('https://suggest.seznam.cz/fulltext/cs',params={'phrase':q,'count':15},timeout=20).json().get('result',[])
    szl=[(''.join(t['text'] for t in r['text']),r.get('userData',{}).get('_count')) for r in sz]
    out[q]={'google':g,'seznam':szl}
    print('##',q); print('  G:',' | '.join(g)); print('  S:',' | '.join(f'{a} ({c})' for a,c in szl)); time.sleep(0.5)
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False)
