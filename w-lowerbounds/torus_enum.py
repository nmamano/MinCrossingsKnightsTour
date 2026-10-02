# enumerate crossing-free 2-factors on a p x q torus (knight moves; crossings checked in the cover)
import sys
from collections import Counter
from ortools.sat.python import cp_model
from strip_dp import cross
p=int(sys.argv[1]); q=int(sys.argv[2])
MOV=[(1,2),(2,1),(2,-1),(1,-2)]
E=[(x,y,d[0],d[1]) for x in range(p) for y in range(q) for d in MOV]
m=cp_model.CpModel(); xv={e:m.NewBoolVar('') for e in E}
inc={(x,y):[] for x in range(p) for y in range(q)}
for e in E:
    x,y,dx,dy=e; inc[(x,y)].append(e); inc[((x+dx)%p,(y+dy)%q)].append(e)
for c in inc: m.Add(sum(xv[e] for e in inc[c])==2)
for e in E:
    for f in E:
        if f<=e: continue
        for sx in (-p,0,p):
            for sy in (-q,0,q):
                x,y,dx,dy=e; a,b,c,d=f
                if cross((x,y,x+dx,y+dy),(a+sx,b+sy,a+sx+c,b+sy+d)):
                    m.AddBoolOr([xv[e].Not(),xv[f].Not()])
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s): super().__init__(); s.types=Counter(); s.n=0
    def on_solution_callback(s):
        s.n+=1
        ch=[e for e in E if s.Value(xv[e])]
        # per-cell type: sorted pair of move vectors
        cell={}
        for (x,y,dx,dy) in ch:
            cell.setdefault((x,y),[]).append((dx,dy)); cell.setdefault(((x+dx)%p,(y+dy)%q),[]).append((-dx,-dy))
        straight=sum(1 for v in cell.values() if v[0][0]==-v[1][0] and v[0][1]==-v[1][1])
        s.types[(tuple(sorted(Counter((abs(dx),abs(dy),(dx*dy>0)) for (_,_,dx,dy) in ch).items())), straight)]+=1
s=cp_model.CpSolver(); s.parameters.enumerate_all_solutions=True; s.parameters.num_workers=1; s.parameters.max_time_in_seconds=300
cb=CB(); st=s.Solve(m,cb)
print(p,q,s.StatusName(st),'solutions',cb.n)
for k,v in cb.types.most_common(30): print(v,k)
