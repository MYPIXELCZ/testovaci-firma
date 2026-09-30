import requests, json, time, sys, urllib.parse
S=requests.Session()
S.headers['User-Agent']='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
S.get('https://trends.google.com/trends/?geo=CZ',timeout=30)
def get(url,params):
    for i in range(6):
        try: r=S.get(url,params=params,timeout=30)
        except Exception as e:
            print('EXC',e.__class__.__name__,file=sys.stderr); time.sleep(10); continue
        if r.status_code==200: return json.loads(r.text[r.text.index('{'):] if r.text.startswith(')') else r.text[5:])
        print('HTTP',r.status_code,'retry',file=sys.stderr); time.sleep(20*(i+1))
    raise SystemExit('fail')
def series(kws,time_='today 5-y'):
    req={"comparisonItem":[{"keyword":k,"geo":"CZ","time":time_} for k in kws],"category":0,"property":""}
    ex=get('https://trends.google.com/trends/api/explore',{'hl':'cs','tz':'-120','req':json.dumps(req)})
    w=[w for w in ex['widgets'] if w['id']=='TIMESERIES'][0]
    d=get('https://trends.google.com/trends/api/widgetdata/multiline',{'hl':'cs','tz':'-120','req':json.dumps(w['request']),'token':w['token']})
    return [(p['formattedAxisTime'] if 'formattedAxisTime' in p else p['time'], p['time'], p['value']) for p in d['default']['timelineData']]
if __name__=='__main__':
    import os
    groups=json.load(open(sys.argv[1])); out=json.load(open(sys.argv[2])) if os.path.exists(sys.argv[2]) else {}
    for name,kws in groups.items():
        if name in out and 'data' in out[name]: continue
        try: out[name]={'kws':kws,'data':series(kws)}
        except SystemExit as e: out[name]={'kws':kws,'error':str(e)}
        print(name,'ok' if 'data' in out[name] else 'ERR',file=sys.stderr); time.sleep(6); json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False)
    json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False)
