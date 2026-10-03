"""Exact finite path types in the four period-six fold corridors."""
from pathlib import Path
from collections import defaultdict,Counter
import json
ROOT=Path(__file__).resolve().parents[2]
d=json.loads((ROOT/'w-integrator/corners/FOLD24_base_n96.json').read_text())
results=[]
def canon(v):
    k=v[0]//6;return (v[0]-6*k,v[1]-6*k),k
for r in range(4):
    E=set()
    for x in range(6):
        for j in range(3):
            a=(x,x+j)
            for dx,dy in d['template'][f'{r}:{(x-8)%6},{j}']:
                b=(x+dx,x+j+dy)
                ca,ka=canon(a);cb,kb=canon(b)
                forward=(ca,cb,kb-ka);reverse=(cb,ca,ka-kb)
                E.add(min(forward,reverse))
    adj=defaultdict(list)
    for i,(a,b,k) in enumerate(sorted(E)):
        adj[a].append((b,k,i));adj[b].append((a,-k,i))
    assert all(len(es)==2 for v,es in adj.items() if 0<=v[1]-v[0]<=2)
    assert all(len(es)<=2 for es in adj.values())
    seen=set();comps=[]
    for v in adj:
        if v in seen:continue
        todo=[v];seen.add(v);ends=[]
        for a in todo:
            if len(adj[a])==1:ends.append(a)
            for b,k,i in adj[a]:
                if b not in seen:seen.add(b);todo.append(b)
        assert len(ends)==2,('non-path component',r,todo)
        sides=['A' if a[1]-a[0]>2 else 'B' for a in ends]
        assert all(not 0<=a[1]-a[0]<=2 for a in ends)
        cur=ends[0];last=-1;shift=0;path=[cur]
        while cur!=ends[1]:
            nxt,k,i=next(z for z in adj[cur] if z[2]!=last)
            shift+=k;cur=nxt;last=i;path.append((cur[0]+6*shift,cur[1]+6*shift))
        entry=dict(type=''.join(sorted(sides)),vertices=len(todo),ends=ends,lifted_path=path)
        if entry['type']=='AA':
            cs=[v[0]-2*v[1] for v in (path[0],path[-1])]
            entry['line_labels']=cs
            entry['cheap_P_compatible']=(cs[1]==cs[0]+(3 if cs[0]%2 else -3))
        comps.append(entry)
    rec=dict(frame=r,edge_orbits=len(E),types=dict(Counter(c['type'] for c in comps)),components=comps)
    results.append(rec);print(rec)
(ROOT/'gap/verifier/claim36_corridor.json').write_text(json.dumps(results,indent=2))
