"""Independent integer checker. Standard library only; no worker code imports."""
import json
import hashlib
from pathlib import Path
from collections import defaultdict

MOVES = ((-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1))

def orient(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def proper(e,f):
    a,b=e;c,d=f
    return orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0

def crossing_count(edges):
    # Inclusive bounding boxes in 4x4 bins. Every intersection shares a bin.
    bins=defaultdict(list); total=0
    for i,e in enumerate(edges):
        a,b=e
        keys=[(x,y) for x in range(min(a[0],b[0])//4,max(a[0],b[0])//4+1)
                    for y in range(min(a[1],b[1])//4,max(a[1],b[1])//4+1)]
        candidates=set(j for k in keys for j in bins[k])
        total+=sum(proper(e,edges[j]) for j in candidates)
        for k in keys: bins[k].append(i)
    return total

def check(g):
    n=len(g); assert n>0 and all(len(row)==n for row in g),'not square'
    adj={}; turns=0
    for r,row in enumerate(g):
        for c,s in enumerate(row):
            assert isinstance(s,str) and len(s)==2 and all(x in '01234567' for x in s),('bad code',r,c,s)
            assert s[0]!=s[1],('duplicate edge',r,c)
            p=(r,c); adj[p]=tuple((r+MOVES[int(k)][0],c+MOVES[int(k)][1]) for k in s)
            assert all(0<=q[0]<n and 0<=q[1]<n for q in adj[p]),('off board',p)
            turns+=orient(adj[p][0],p,adj[p][1])!=0
    for p,ns in adj.items():
        for q in ns: assert p in adj[q],('not reciprocal',p,q)
    seen=set(); prev=None; p=(0,0)
    while p not in seen:
        seen.add(p); q=next(q for q in adj[p] if q!=prev); prev,p=p,q
    assert p==(0,0) and len(seen)==n*n,('not one cycle',len(seen),n*n)
    edges=[(p,q) for p,ns in adj.items() for q in ns if p<q]
    assert len(edges)==n*n
    return crossing_count(edges),turns

def main():
    rows=[]
    for f in sorted(Path('w-integrator/tours').glob('*.json')):
        raw=f.read_bytes();d=json.loads(raw)
        try:
            x,t=check(d['tour'])
            assert len(d['tour'])==d['n'],'n mismatch'
            assert x==d['crossings'] and t==d['turns'],('count mismatch',x,t,d['crossings'],d['turns'])
            if 'Xbrute' in d: assert x==d['Xbrute']
            row=dict(file=f.name,n=d['n'],X=x,T=t,b=x-9*d['n'],Z=d['info']['Z'],valid=True,sha256=hashlib.sha256(raw).hexdigest())
        except Exception as e: row=dict(file=f.name,valid=False,error=str(e))
        rows.append(row)
    Path('w-verifier/results.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('files',len(rows),'failures',[r for r in rows if not r['valid']])
    for family in ['H16a','H16b']:
        for residue in range(0,8,2):
            rr=sorted([r for r in rows if r['valid'] and r['file'].startswith(family) and r['n']%8==residue],key=lambda r:r['n'])
            print(family,residue,'ns',[r['n'] for r in rr],'b',sorted({r['b'] for r in rr}),'Z',sorted({r['Z'] for r in rr}),'slopes',sorted({(b['X']-a['X'])/(b['n']-a['n']) for a,b in zip(rr,rr[1:]) if b['n']!=a['n']}))
if __name__=='__main__': main()
