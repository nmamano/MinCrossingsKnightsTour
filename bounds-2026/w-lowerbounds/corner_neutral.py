"""Corner neutrality test (2026-10-02). Quarter plane x,y >= 0, window 0..M-1 (degree 2), frame
M..M+1 (degree <= 2). Left edge rows >= d: pattern A (P or P'); bottom edge columns >= d: pattern B
(transposed P or P'). No crossings allowed except between two forced pattern edges, or when one
edge has both ends in the d x d corner box. Feasible => a corner with only O(1) defects exists."""
import sys, itertools
from ortools.sat.python import cp_model
from strip_dp import cross
M=int(sys.argv[1]); d=int(sys.argv[2]); A=sys.argv[3]; B=sys.argv[4]; tl=int(sys.argv[5]) if len(sys.argv)>5 else 600
KM=[(1,2),(2,1),(2,-1),(1,-2)]
import os
STRAIGHT=os.environ.get("STRAIGHT")
y0=-2 if STRAIGHT else 0
cells=[(x,y) for x in range(M+2) for y in range(y0,M+2)]; cs=set(cells)
win={(x,y) for x in range(M) for y in range(M)}
E=[]
for (x,y) in cells:
    for dd in KM+[(-a,-b) for a,b in KM]:
        q=(x+dd[0],y+dd[1])
        if q in cs and ((x,y) in win or q in win):
            e=tuple(sorted([(x,y),q]))
            if e not in E: E.append(e)
Eset=set(E)
def left_pattern(kind, y):
    s=1 if kind=='P' else -1
    return [((0,y),(2,y+s)), ((0,y),(1,y+2*s)), ((1,y),(3,y+s))]
forced=set()
for y in range(d, M+2):
    for (a,b) in left_pattern(A,y):
        e=tuple(sorted([a,b]))
        if e in Eset: forced.add(e)
for x in ([] if STRAIGHT else range(d, M+2)):
    for (a,b) in left_pattern(B,x):
        a=(a[1],a[0]); b=(b[1],b[0]); e=tuple(sorted([a,b]))
        if e in Eset: forced.add(e)
m=cp_model.CpModel(); xv={e:m.NewBoolVar('') for e in E}
inc={c:[] for c in cells}
for e in E: inc[e[0]].append(e); inc[e[1]].append(e)
for c in cells:
    if c in win: m.Add(sum(xv[e] for e in inc[c])==2)
    else: m.Add(sum(xv[e] for e in inc[c])<=2)
# pattern cells: columns 0,1 for rows >= d and rows 0,1 for columns >= d have exactly the pattern edges
for e in forced: m.Add(xv[e]==1)
def pcell(c, kind, t):
    # c=(depth, along); pattern cell of a left-type edge with pattern kind
    dep, al = c
    if dep == 0: return al >= d
    if dep == 1: return al >= (d + 2 if kind == 'P' else d)
    return False
pc={(x,y) for (x,y) in win if pcell((x,y),A,0) or (not STRAIGHT and pcell((y,x),B,0))}
for c in pc:
    for e in inc[c]:
        if e not in forced: m.Add(xv[e]==0)
box=lambda e: all(p[0]<d and p[1]<d for p in e)
import os
NOX=os.environ.get("NOX")
for e,f in ([] if NOX else itertools.combinations(E,2)):
    if (e in forced and f in forced) or box(e) or box(f): continue
    if cross((*e[0],*e[1]),(*f[0],*f[1])): m.AddBoolOr([xv[e].Not(),xv[f].Not()])
s=cp_model.CpSolver(); s.parameters.num_workers=2; s.parameters.max_time_in_seconds=tl
st=s.Solve(m)
print(f'M={M} d={d} left={A} bottom={B}: {s.StatusName(st)}', flush=True)
