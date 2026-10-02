"""Check F3, explicit closed cycles, and colour defect charges; no solver."""
import sys
from pathlib import Path
from collections import Counter,defaultdict
sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parents[1]/'w-lowerbounds')]
from fold_complete2 import base
from kt.core import seg_cross

def ek(a,b):return tuple(sorted((a,b)))
def explicit(s):
    inner=[(2*k,s+k) for k in range(s+1)]+[(2*s-j,2*s-2*j) for j in range(1,s+1)]
    outer=[(1+2*k,s+2+k) for k in range(s+2)]+[(2*s+3-j,2*s+3-2*j) for j in range(1,s+2)]
    walk=inner+list(reversed(outer))
    assert len(set(walk))==len(walk)==4*s+4
    return {ek(walk[i],walk[(i+1)%len(walk)]) for i in range(len(walk))}
for n in (48,96):
    E,deg=base(n);h=n//2;bad={(x,y):2-deg[x,y] for x in range(n) for y in range(n) if deg[x,y]!=2}
    near=defaultdict(set)
    for e in E:
        for p in e:near[p].add(e)
    crosspairs=set()
    for e in E:
        p=e[0]
        for dx in range(-4,5):
            for dy in range(-4,5):
                for f in near.get((p[0]+dx,p[1]+dy),()):
                    if e<f and seg_cross(*e,*f):crosspairs.add((e,f))
    assert len(crosspairs)==4*n-24
    print("raw defect count",n,len(bad),flush=True)
    used=set();num=0
    for r in range(4):
        def rot(p):
            x,y=p
            for _ in range(r):x,y=n-1-y,x
            return x,y
        for s in range(1,n//4-2):
            cyc={ek(rot(a),rot(b)) for a,b in explicit(s)}
            assert cyc<=E
            vs={p for e in cyc for p in e}
            assert all(deg[p]==2 for p in vs)
            assert not vs&used
            used|=vs;num+=1
    def label(p):
        return ''.join('L' if v<n//4 else 'H' if v>3*n//4 else 'M' for v in p)
    charges=Counter()
    for p,d in bad.items():charges[label(p)]+=(-1 if sum(p)%2 else 1)*d
    print('n',n,'crossings',len(crosspairs),'bad cells',len(bad),'explicit disjoint cycles',num,'charges',dict(sorted(charges.items())),flush=True)
