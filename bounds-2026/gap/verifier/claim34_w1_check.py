"""Independent exact-quarter, projected-map check of w1_compare R=1,2,3."""
from pathlib import Path
from itertools import product
from collections import defaultdict
import sys,json,time
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'w-verifier'))
from claim9_tiles import quarters
MOV=((1,2),(2,1),(2,-1),(1,-2)); PTS=list(product(range(3),repeat=2))
templates={d:quarters(((0,0),d)) for d in MOV}
def ekey(a,b):return tuple(sorted((a,b)))
stack=set()
for a,b in ((1,0),(0,1),(1,1),(1,-1)):
    moves=[(x,y) for x,y in product(range(-2,3),repeat=2)
           if sorted((abs(x),abs(y)))==[1,2] and a*x+b*y==1]
    levels=sorted({a*x+b*y+s for x,y in PTS for s in (-1,0)})
    for seq in product(moves,repeat=len(levels)):
        seq=dict(zip(levels,seq))
        stack.add(tuple(tuple(sorted((seq[a*x+b*y],tuple(-v for v in seq[a*x+b*y-1])))) for x,y in PTS))
assert len(stack)==156
results=[]
for R in (1,2,3):
    sq=set(product(range(-R,2+R),repeat=2));deg=set(product(range(1-R,2+R),repeat=2))
    cov={}
    for x,y in product(range(-R-3,R+5),repeat=2):
        for d in MOV:
            e=((x,y),(x+d[0],y+d[1]));qs={(x+i,y+j,k) for i,j,k in templates[d]}
            if any(q[:2] in sq for q in qs) or any(v in deg for v in e):cov[e]=qs
    m=cp_model.CpModel();X={e:m.new_bool_var('e') for e in cov};inc=defaultdict(list);own=defaultdict(list)
    for e,qs in cov.items():
        for v in e:inc[v].append(e)
        for q in qs:own[q].append(e)
    for x,y in sq:
        for k in range(4):m.add(sum(X[e] for e in own[x,y,k])==1)
    for v in deg:m.add(sum(X[e] for e in inc[v])==2)
    def forbid(key):
        es={ekey(p,(p[0]+d[0],p[1]+d[1])) for p,ds in zip(PTS,key) for d in ds}
        assert es<=X.keys();m.add(sum(X[e] for e in es)<=len(es)-1)
    for key in stack:forbid(key)
    # Each stack has a full-plane extension. Check its restriction explicitly,
    # using the same finite level choices; no need for 156 solver calls.
    extendible=set()
    for a,b in ((1,0),(0,1),(1,1),(1,-1)):
        moves=[(x,y) for x,y in product(range(-2,3),repeat=2)
               if sorted((abs(x),abs(y)))==[1,2] and a*x+b*y==1]
        levels=sorted({a*x+b*y+s for x,y in PTS for s in (-1,0)})
        for seq in product(moves,repeat=len(levels)):
            seq=dict(zip(levels,seq));c=lambda t:seq.get(t,moves[0])
            chosen=set()
            for e in cov:
                u,v=sorted(e,key=lambda p:a*p[0]+b*p[1]);t=a*u[0]+b*u[1]
                if (v[0]-u[0],v[1]-u[1])==c(t):chosen.add(e)
            assert all(sum(e in chosen for e in inc[v])==2 for v in deg)
            assert all(sum(e in chosen for e in own[x,y,k])==1 for x,y in sq for k in range(4))
            extendible.add(tuple(tuple(sorted((c(a*x+b*y),tuple(-v for v in c(a*x+b*y-1))))) for x,y in PTS))
    assert extendible==stack
    solver=cp_model.CpSolver();solver.parameters.num_workers=1;solver.parameters.max_time_in_seconds=20
    extras=[];t=time.monotonic()
    while True:
        status=solver.solve(m)
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
        key=tuple(tuple(sorted((v[0]-p[0],v[1]-p[1]) for e in inc[p] if solver.value(X[e]) for v in e if v!=p)) for p in PTS)
        assert key not in stack and key not in extras;extras.append(key);forbid(key)
    rec=dict(R=R,status=solver.status_name(status),seconds=time.monotonic()-t,
             stack_maps=156,extra_maps=len(extras),total_maps=156+len(extras),complete=status==cp_model.INFEASIBLE,
             variables=len(cov),extras=extras)
    results.append(rec);print({k:v for k,v in rec.items() if k!='extras'},flush=True)
(ROOT/'gap/verifier/claim34_w1_check.json').write_text(json.dumps(results,indent=2))
