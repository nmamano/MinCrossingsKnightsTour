# Can a crossing-free W x W window (all cells degree 2) have 3 move types among edges at its centre cells?
import sys, itertools
from ortools.sat.python import cp_model
from strip_dp import cross
W=int(sys.argv[1]); r=int(sys.argv[2])  # centre box half-size r
MOVES=[(1,2),(2,1),(2,-1),(1,-2)]
cells=[(x,y) for x in range(-2,W+2) for y in range(-2,W+2)]
win={(x,y) for x in range(W) for y in range(W)}
cs=set(cells)
E=[]
for (x,y) in cells:
    for d in MOVES:
        q=(x+d[0],y+d[1])
        if q in cs and ((x,y) in win or q in win): E.append(((x,y),q,d))
m=cp_model.CpModel(); xv={e:m.NewBoolVar('') for e in E}
inc={c:[] for c in cells}
for e in E: inc[e[0]].append(e); inc[e[1]].append(e)
for c in cells:
    m.Add(sum(xv[e] for e in inc[c])==2) if c in win else m.Add(sum(xv[e] for e in inc[c])<=2)
for e,f in itertools.combinations(E,2):
    if cross((*e[0],*e[1]),(*f[0],*f[1])): m.AddBoolOr([xv[e].Not(),xv[f].Not()])
c0=W//2
centre={(x,y) for x in range(c0-r,c0+r) for y in range(c0-r,c0+r)}
used={d:m.NewBoolVar('') for d in MOVES}
for d in MOVES:
    m.AddBoolOr([xv[e] for e in E if e[2]==d and (e[0] in centre or e[1] in centre)]).OnlyEnforceIf(used[d])
import os
if os.environ.get("PERP"): m.Add(used[(2,1)]+used[(1,-2)]==2)
else: m.Add(sum(used.values())>=3)
s=cp_model.CpSolver(); s.parameters.num_workers=2; s.parameters.max_time_in_seconds=600
st=s.Solve(m); print('W',W,'centre',2*r,'x',2*r,s.StatusName(st))
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    ch=[e for e in E if s.Value(xv[e])]
    sym={(2,1):'h',(1,2):'v',(2,-1):'H',(1,-2):'V'}
    for y in reversed(range(W)):
        print(' '.join(''.join(sorted(sym[e[2]] for e in inc[(x,y)] if s.Value(xv[e]))) for x in range(W)))
