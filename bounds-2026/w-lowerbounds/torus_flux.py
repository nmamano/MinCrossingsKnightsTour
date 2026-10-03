# crossing-free 2-factors on a p x q torus (knight moves, crossings in the universal cover);
# maximise colour flux through the horizontal cut between rows q-1 and 0.
import sys, itertools
from ortools.sat.python import cp_model
from strip_dp import cross
p=int(sys.argv[1]); q=int(sys.argv[2])
MOV=[(1,2),(2,1),(2,-1),(1,-2)]
E=[]  # (x,y,dx,dy) base cell + move
for x in range(p):
    for y in range(q):
        for d in MOV: E.append((x,y,d[0],d[1]))
m=cp_model.CpModel(); xv={e:m.NewBoolVar('') for e in E}
inc={(x,y):[] for x in range(p) for y in range(q)}
for e in E:
    x,y,dx,dy=e
    inc[(x,y)].append(e); inc[((x+dx)%p,(y+dy)%q)].append(e)
for c in inc: m.Add(sum(xv[e] for e in inc[c])==2)
# zero crossings: for each pair of edge instances in the cover that cross, not both
def inst(e,sx,sy):
    x,y,dx,dy=e; return (x+sx,y+sy,x+dx+sx,y+dy+sy)
for e in E:
    for f in E:
        for sx in (-p,0,p):
            for sy in (-q,0,q):
                if (f,sx,sy) <= (e,0,0) and not (sx==0 and sy==0 and f<e): pass
                if cross(inst(e,0,0),inst(f,sx,sy)):
                    m.AddBoolOr([xv[e].Not(),xv[f].Not()])
# no 2-cycles (same pair of cells twice) handled by distinct moves; forbid short contractible cycles lazily: skip
# flux through cut between rows q-1 and 0 (edges whose lower endpoint row y and y+dy>=q, or dy<0 wrapping)
fl=[]
for e in E:
    x,y,dx,dy=e
    lo=(x,y) if dy>0 else ((x+dx)%p,(y+dy)%q)
    ylo=y if dy>0 else y+dy
    yhi=y+dy if dy>0 else y
    # crosses cut at multiples of q: ylo < kq <= yhi
    if any(ylo < k*q <= yhi for k in (-1,0,1,2)):
        s=1 if (lo[0]+lo[1])%2==0 else -1
        fl.append(s*xv[e])
m.Maximize(sum(fl))
s=cp_model.CpSolver(); s.parameters.num_workers=2; s.parameters.max_time_in_seconds=120
st=s.Solve(m)
print(p,q,s.StatusName(st),'max flux',s.ObjectiveValue())
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    ch=[e for e in E if s.Value(xv[e])]
    from collections import Counter
    print(Counter((e[2],e[3]) for e in ch))
