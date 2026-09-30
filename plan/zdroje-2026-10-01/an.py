import json,datetime,sys,statistics as st
d=json.load(open(sys.argv[1]))
def mon(ts): return datetime.datetime.utcfromtimestamp(int(ts)).month
for n,v in d.items():
    if 'data' not in v: print(n,'ERR'); continue
    pts=v['data']; k=len(v['kws'])
    for i,kw in enumerate(v['kws']):
        vals=[p[2][i] for p in pts]; ts=[p[1] for p in pts]
        mm={m:round(st.mean([vals[j] for j in range(len(vals)) if mon(ts[j])==m] or [0]),1) for m in range(1,13)}
        n52=52
        first=st.mean(vals[:n52]); last=st.mean(vals[-n52:])
        oct_dec=st.mean([mm[m] for m in (10,11,12)]); yr=st.mean(mm.values())
        print(f"{n:18}{kw:32} avg5y={st.mean(vals):5.1f} y1={first:5.1f} y5={last:5.1f} trend={(last/first-1)*100 if first else 0:+5.0f}% OctDec/avg={oct_dec/yr if yr else 0:4.2f} peak={max(mm,key=mm.get)} low={min(mm,key=mm.get)} | "+" ".join(f"{int(mm[m])}" for m in range(1,13)))
