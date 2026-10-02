"""Read full tours and contract paths outside four fixed corner squares."""
import json
from pathlib import Path
from collections import defaultdict
from check import MOVES

def signature(d):
    g=d['tour'];n=len(g);z=d['info']['Z']
    def free(p): return (p[0]<z or p[0]>=n-z) and (p[1]<z or p[1]>=n-z)
    def norm(p): return (int(p[0]>=n-z),int(p[1]>=n-z), min(p[0],n-1-p[0]),min(p[1],n-1-p[1]))
    adj={}
    for r in range(n):
        for c in range(n):
            if not free((r,c)):
                adj[r,c]=tuple((r+MOVES[int(k)][0],c+MOVES[int(k)][1]) for k in g[r][c])
    pairs=[];seen=set()
    for p,qq in adj.items():
        if p in seen: continue
        ends=[q for q in qq if free(q)]
        if not ends: continue
        start=ends[0];prev=start;cur=p
        while not free(cur):
            assert cur not in seen
            seen.add(cur)
            nex=next(q for q in adj[cur] if q!=prev)
            prev,cur=cur,nex
        pairs.append(tuple(sorted((norm(start),norm(cur)))))
    assert len(seen)==len(adj),'closed component outside corners'
    return tuple(sorted(pairs))

if __name__=='__main__':
    groups=defaultdict(list)
    for f in sorted(Path('w-integrator/tours').glob('*.json')):
        d=json.loads(f.read_text());groups[f.name[:4]].append((d['n'],signature(d)))
    report=[]
    for fam,rs in groups.items():
        for modulus in [8,24]:
            by=defaultdict(list)
            for n,s in rs: by[n%modulus].append((n,s))
            for r,rr in sorted(by.items()):
                line=f'{fam} mod {modulus} residue {r}: {len(set(s for n,s in rr))} distinct outside path matchings; sizes {sorted(set(len(s) for n,s in rr))}'
                print(line);report.append(line)
    Path('w-verifier/topology.txt').write_text('\n'.join(report)+'\n')
