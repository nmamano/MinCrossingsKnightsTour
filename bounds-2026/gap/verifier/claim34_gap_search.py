"""Search for a Hall-deficient set of absorbing gaps in a local degree-two patch."""
from collections import defaultdict
from itertools import product
from pathlib import Path
import json,sys,time
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'w-verifier'))
from claim9_tiles import quarters

N=int(sys.argv[1]); MAXG=int(sys.argv[2]); SECONDS=int(sys.argv[3])
MODE=sys.argv[4] if len(sys.argv)>4 else 'square'
HQ={'BR':(0,1),'TL':(2,3),'RT':(1,2),'LB':(3,0)}
MOV=[(x,y) for x,y in product(range(-2,3),repeat=2) if sorted((abs(x),abs(y)))==[1,2]]
core=set(product(range(N+1),repeat=2)); squares=set(product(range(N),repeat=2))
es=sorted({tuple(sorted((v,(v[0]+dx,v[1]+dy)))) for v in core for dx,dy in MOV})
idx={e:i for i,e in enumerate(es)}
model=cp_model.CpModel(); X=[model.new_bool_var('e') for e in es]
inc=defaultdict(list); own=defaultdict(list)
for i,e in enumerate(es):
    for v in e:inc[v].append(X[i])
    a,b=e
    for x,y,k in quarters(((0,0),(b[0]-a[0],b[1]-a[1]))):own[x+a[0],y+a[1],k].append(i)
for v,vs in inc.items():
    if v in core:model.add(sum(vs)==2)
    else:model.add(sum(vs)<=2)
bad={}; qb={}
for x,y in squares:
    for k in range(4):
        b=model.new_bool_var('badquarter'); m=sum(X[i] for i in own[x,y,k])
        model.add(m!=1).only_enforce_if(b);model.add(m==1).only_enforce_if(b.Not())
        qb[x,y,k]=b
    bad[x,y]=model.new_bool_var('badsquare')
    model.add_max_equality(bad[x,y],[qb[x,y,k] for k in range(4)])

def nxt(z):
    x,y,h=z
    return {'BR':(x+1,y,'TL'),'TL':(x,y+1,'BR'),
            'RT':(x+1,y,'LB'),'LB':(x,y-1,'RT')}[h]
def halfedges(z):
    x,y,h=z
    # H and V possible tiles covering this half; independent endpoint construction.
    pairs={'BR':(((x,y),(x+2,y+1)),((x,y-1),(x+1,y+1))),
           'TL':(((x-1,y),(x+1,y+1)),((x,y),(x+1,y+2))),
           'RT':(((x,y+1),(x+2,y)),((x,y+2),(x+1,y))),
           'LB':(((x-1,y+1),(x+1,y)),((x,y+1),(x+1,y-1)))}[h]
    return [idx[tuple(sorted(e))] for e in pairs]
cuts=[]; uses=defaultdict(list)
for x,y in sorted(squares):
    for h in ('BR','TL','RT','LB'):
        start=(x,y,h); path=[start]
        for length in range(1,MAXG+2):
            end=nxt(path[-1]);path.append(end)
            if end[:2] not in squares:break
            if length<2:continue
            gap=path[1:-1];z=model.new_bool_var('cut')
            for t in (start,end):
                model.add(bad[t[:2]]==0).only_enforce_if(z)
                he,ve=halfedges(t);model.add(X[he]+X[ve]==1).only_enforce_if(z)
            model.add(X[halfedges(start)[0]]+X[halfedges(end)[0]]==1).only_enforce_if(z)
            for t in gap:model.add(bad[t[:2]]==1).only_enforce_if(z)
            targets={(t[0],t[1],k) for t in gap for k in (HQ[t[2]] if MODE=='half' else range(4))}
            for q in targets:uses[q].append(z)
            cuts.append((z,list(path)))
cost=[]
for q,zs in uses.items():
    u=model.new_bool_var('union');model.add_max_equality(u,zs)
    v=model.new_bool_var('count');model.add_min_equality(v,[u,qb[q]])
    cost.append(v)
model.add(2*sum(z for z,p in cuts)>sum(cost))
solver=cp_model.CpSolver();solver.parameters.num_workers=1;solver.parameters.max_time_in_seconds=SECONDS
t=time.monotonic();status=solver.solve(model)
result=dict(date='2026-10-03',N=N,max_gap=MAXG,mode=MODE,seconds=time.monotonic()-t,
            status=solver.status_name(status),candidate_cuts=len(cuts),edge_variables=len(es))
if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    selected={i for i in range(len(es)) if solver.value(X[i])}
    paths=[p for z,p in cuts if solver.value(z)]
    def mult(sq,k):return sum(i in selected for i in own[*sq,k])
    def good(sq):return all(mult(sq,k)==1 for k in range(4))
    for p in paths:
        assert all(not good(t[:2]) for t in p[1:-1])
        assert all(good(t[:2]) and sum(i in selected for i in halfedges(t))==1 for t in (p[0],p[-1]))
        assert (halfedges(p[0])[0] in selected)!=(halfedges(p[-1])[0] in selected)
    union={(t[0],t[1],k) for p in paths for t in p[1:-1] for k in (HQ[t[2]] if MODE=='half' else range(4))}
    bq=[q for q in sorted(union) if mult(q[:2],q[2])!=1]
    assert len(bq)<2*len(paths)
    result.update(edges=[es[i] for i in sorted(selected)],cuts=paths,bad_quarters=bq,
                  quarter_multiplicities={str(sq):[mult(sq,k) for k in range(4)] for sq in sorted(squares)})
print(json.dumps(result,indent=2))
(ROOT/f'gap/verifier/claim34_gap_N{N}_L{MAXG}_{MODE}.json').write_text(json.dumps(result,indent=2))
