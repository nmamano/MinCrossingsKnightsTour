"""Measure the crossing cost of merging chevron loops: fix the fold 2-factor outside a window at the
left-edge midpoint, re-optimise inside with lazy cuts that forbid closed cycles inside the window region."""
import sys, ast, itertools
from collections import defaultdict, Counter
from ortools.sat.python import cp_model
import networkx as nx
from strip_dp import cross
from fold_complete2 import base, MOVES
n=int(sys.argv[1]); r=int(sys.argv[2]); D=int(sys.argv[3])
E,deg=base(n,ts=(-1,-1,-1,-1),ms=(0,1,0,1))
h=n//2+1   # left midline at h + ms[3]
on=lambda p:0<=p[0]<n and 0<=p[1]<n
X0=int(sys.argv[4]); Y0=int(sys.argv[5])
free={(x,y) for x in range(X0,X0+D) for y in range(Y0,Y0+r)}
assert all(deg[p]==2 for p in free), 'defect cells inside window'
fixed=[e for e in E if e[0] not in free and e[1] not in free]
cand=set()
for p in free:
    for dx,dy in MOVES:
        q=(p[0]+dx,p[1]+dy)
        if on(q):
            e=tuple(sorted([p,q]))
            if q in free or e in E: cand.add(e)
cand=sorted(cand)
m=cp_model.CpModel(); xv={e:m.NewBoolVar('') for e in cand}
inc=defaultdict(list)
for e in cand: inc[e[0]].append(e); inc[e[1]].append(e)
for p in free: m.Add(sum(xv[e] for e in inc[p])==2)
for e in cand:
    if not(e[0] in free and e[1] in free): m.Add(xv[e]==1)
seg=lambda e:(*e[0],*e[1])
terms=[]
near_fixed=[f for f in fixed if X0-3<=min(f[0][0],f[1][0])<X0+D+3 and Y0-3<=min(f[0][1],f[1][1])<Y0+r+3]
for i,e in enumerate(cand):
    for f in cand[i+1:]:
        if cross(seg(e),seg(f)):
            z=m.NewBoolVar(''); m.AddBoolOr([xv[e].Not(),xv[f].Not(),z]); terms.append(z)
    for f in near_fixed:
        if cross(seg(e),seg(f)): terms.append(xv[e])
m.Minimize(sum(terms))
def comps_of(chosen):
    G=nx.Graph(); G.add_edges_from(set(chosen)|set(fixed)); return list(nx.connected_components(G))
base_val=None
# baseline objective with current edges
cur=[e for e in cand if e in E]
basecost=sum(1 for i,e in enumerate(cand) for f in cand[i+1:] if e in E and f in E and cross(seg(e),seg(f)))+sum(1 for e in cur for f in near_fixed if cross(seg(e),seg(f)))
C0=comps_of(cur)
touch=lambda c: any(p in free for p in c)
print('baseline window cost',basecost,'components touching window',sum(1 for c in C0 if touch(c)),'total comps',len(C0),flush=True)
rounds=0
target=int(sys.argv[6]) if len(sys.argv)>6 else 1
while True:
    s=cp_model.CpSolver(); s.parameters.num_workers=2; s.parameters.max_time_in_seconds=180
    st=s.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print('round',rounds,s.StatusName(st)); break
    ch=[e for e in cand if s.Value(xv[e])]
    C=comps_of(ch); tw=[c for c in C if touch(c)]
    print('round',rounds,s.StatusName(st),'cost',s.ObjectiveValue(),'comps touching window',len(tw),'total',len(C),flush=True)
    if rounds>0 and not any(tuple(map(int,sys.argv[7].split(','))) in cc and len(cc)<4000 for cc in tw): break
    big=max(tw,key=len)
    cellc=tuple(map(int,sys.argv[7].split(',')))
    for c in [cc for cc in tw if cellc in cc]:
        cut=[e for e in cand if (e[0] in c)!=(e[1] in c)]
        if cut: m.Add(sum(xv[e] for e in cut)>=2)
    rounds+=1
