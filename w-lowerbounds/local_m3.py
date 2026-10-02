"""Local lemma test: in a crossing-free W x W window (all cells degree 2, frame degree <= 2, no
crossings among edges touching the window), which values can the colour flux through the central
unit dual segment take?"""
import sys, itertools
from ortools.sat.python import cp_model
from strip_dp import cross
W=int(sys.argv[1]); orient=sys.argv[2]   # 'h' horizontal segment or 'v' vertical
MOVES=[(1,2),(2,1),(2,-1),(1,-2)]
cells=[(x,y) for x in range(-2,W+2) for y in range(-2,W+2)]; cs=set(cells)
win={(x,y) for x in range(W) for y in range(W)}
E=[]
for (x,y) in cells:
    for d in MOVES:
        q=(x+d[0],y+d[1])
        if q in cs and ((x,y) in win or q in win): E.append(((x,y),q))
c=W//2
import os
OX=int(os.environ.get("OX","0")); OY=int(os.environ.get("OY","0"))
if orient=="h": A,B=(c-0.5+OX,c-0.5+OY),(c+0.5+OX,c-0.5+OY)
else: A,B=(c-0.5+OX,c-0.5+OY),(c-0.5+OX,c+0.5+OY)
chi=lambda p: 1 if (p[0]+p[1])%2==0 else -1
def side(P): return (B[0]-A[0])*(P[1]-A[1])-(B[1]-A[1])*(P[0]-A[0])
fl=[]
for e in E:
    if cross((*A,*B),(*e[0],*e[1])):
        left=e[0] if side(e[0])>0 else e[1]
        fl.append((chi(left),e))
res={}
for val in range(-6,7):
    m=cp_model.CpModel(); xv={e:m.NewBoolVar('') for e in E}
    inc={p:[] for p in cells}
    for e in E: inc[e[0]].append(e); inc[e[1]].append(e)
    for p in cells:
        if p in win: m.Add(sum(xv[e] for e in inc[p])==2)
        else: m.Add(sum(xv[e] for e in inc[p])<=2)
    for e,f in itertools.combinations(E,2):
        if cross((*e[0],*e[1]),(*f[0],*f[1])): m.AddBoolOr([xv[e].Not(),xv[f].Not()])
    m.Add(sum(s*xv[e] for s,e in fl)==val)
    s=cp_model.CpSolver(); s.parameters.num_workers=2; s.parameters.max_time_in_seconds=300
    res[val]=s.StatusName(s.Solve(m))
print('W',W,orient,'segment',A,B,'edges crossing it',len(fl),{k:v for k,v in res.items() if v!='INFEASIBLE'})
