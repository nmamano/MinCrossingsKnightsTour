import sys
from collections import Counter, defaultdict
from ortools.sat.python import cp_model
import networkx as nx
from fold_complete2 import base, MOVES
n=int(sys.argv[1]); M=int(sys.argv[2])
E,deg=base(n)
on=lambda p:0<=p[0]<n and 0<=p[1]<n
bad=[(x,y) for x in range(n) for y in range(n) if deg[(x,y)]!=2]
G=nx.Graph(); G.add_nodes_from(bad)
for a in bad:
    for b in bad:
        if a<b and max(abs(a[0]-b[0]),abs(a[1]-b[1]))<=6: G.add_edge(a,b)
for cl in nx.connected_components(G):
    xs=[p[0] for p in cl]; ys=[p[1] for p in cl]
    free={(x,y) for x in range(min(xs)-M,max(xs)+M+1) for y in range(min(ys)-M,max(ys)+M+1) if on((x,y))}
    cand=set()
    for p in free:
        for dx,dy in MOVES:
            q=(p[0]+dx,p[1]+dy)
            e=tuple(sorted([p,q]))
            if on(q) and (q in free or e in E): cand.add(e)
    m=cp_model.CpModel(); xv={e:m.NewBoolVar('') for e in cand}
    inc=defaultdict(list)
    for e in cand: inc[e[0]].append(e); inc[e[1]].append(e)
    for p in free: m.Add(sum(xv[e] for e in inc[p])==2)
    for e in cand:
        if not(e[0] in free and e[1] in free): m.Add(xv[e]==1)
    s=cp_model.CpSolver(); s.parameters.num_workers=2; s.parameters.max_time_in_seconds=60
    print(sorted(cl)[:3], len(cl), 'halfedge deficit', sum(2-deg[p] for p in cl), s.StatusName(s.Solve(m)), flush=True)
