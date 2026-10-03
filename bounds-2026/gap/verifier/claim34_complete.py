"""Try to complete the half-version counterexample into a closed knight tour."""
from pathlib import Path
from itertools import product
from collections import defaultdict
import json,sys,time
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'w-verifier'))
from claim9_tiles import quarters
source=json.loads((ROOT/'gap/verifier/claim34_gap_N4_L6_half.json').read_text())
N=int(sys.argv[1]) if len(sys.argv)>1 else 16; SHIFT=N//2-2
V=set(product(range(N),repeat=2)); moves=[(x,y) for x,y in product(range(-2,3),repeat=2) if sorted((abs(x),abs(y)))==[1,2]]
edges=sorted({tuple(sorted((v,(v[0]+dx,v[1]+dy)))) for v in V for dx,dy in moves if (v[0]+dx,v[1]+dy) in V})
model=cp_model.CpModel();X={e:model.new_bool_var('edge') for e in edges};arcs=[]
ids={v:i for i,v in enumerate(sorted(V))}
for a,b in edges:
    ab=model.new_bool_var('ab');ba=model.new_bool_var('ba');model.add(ab+ba==X[a,b])
    arcs.extend([(ids[a],ids[b],ab),(ids[b],ids[a],ba)])
model.add_circuit(arcs)
own=defaultdict(list)
for e in edges:
    a,b=e
    for x,y,k in quarters(((0,0),(b[0]-a[0],b[1]-a[1]))):own[x+a[0],y+a[1],k].append(e)
path=source['cuts'][0]
for x,y,h in path:
    values=source['quarter_multiplicities'][str((x,y))]
    for k,m in enumerate(values):model.add(sum(X[e] for e in own[x+SHIFT,y+SHIFT,k])==m)
# Preserve the endpoint's actual tile choices, hence its H/V bit.
original={tuple(map(tuple,e)) for e in source['edges']}
for x,y,h in (path[0],path[-1]):
    for e in original:
        a,b=e
        qs={(xx+a[0],yy+a[1],k) for xx,yy,k in quarters(((0,0),(b[0]-a[0],b[1]-a[1])))}
        target={'BR':0,'TL':2,'RT':1,'LB':3}[h]
        if (x,y,target) in qs:
            shifted=tuple((u+SHIFT,v+SHIFT) for u,v in e)
            model.add(X[shifted]==1)
solver=cp_model.CpSolver();solver.parameters.num_workers=1;solver.parameters.max_time_in_seconds=40
t=time.monotonic();status=solver.solve(model)
out=dict(date='2026-10-03',n=N,status=solver.status_name(status),seconds=time.monotonic()-t,shift=SHIFT)
if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    selected=[e for e in edges if solver.value(X[e])]; adj=defaultdict(list)
    for a,b in selected:adj[a].append(b);adj[b].append(a)
    assert len(selected)==N*N and all(len(adj[v])==2 for v in V)
    visited=set();walk=[];prev=None;cur=(0,0)
    while cur not in visited:
        visited.add(cur);walk.append(cur)
        nxt=next(v for v in adj[cur] if v!=prev);prev,cur=cur,nxt
    assert cur==walk[0] and visited==V
    out.update(edges=selected,tour_order=walk,cut=[(x+SHIFT,y+SHIFT,h) for x,y,h in path])
print(json.dumps(out,indent=2));(ROOT/'gap/verifier/claim34_closed_tour.json').write_text(json.dumps(out,indent=2))
