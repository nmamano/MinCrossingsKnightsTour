import sys
from collections import Counter, defaultdict
from ortools.sat.python import cp_model
from fold_complete2 import base, MOVES
n=int(sys.argv[1])
E,deg=base(n)
on=lambda p:0<=p[0]<n and 0<=p[1]<n
h=n//2
for r in range(2,9):
    free={(x,y) for x in range(h-r,h+r) for y in range(h-r,h+r)}
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
    print(r, s.StatusName(s.Solve(m)), flush=True)
