# For all crossing-free 2-factors of a p x q torus: colour flux through the horizontal and vertical cuts, mod 3
import sys
from collections import Counter
from ortools.sat.python import cp_model
from strip_dp import cross
p=int(sys.argv[1]); q=int(sys.argv[2]); tl=int(sys.argv[3]) if len(sys.argv)>3 else 600
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
chi=lambda x,y: 1 if (x+y)%2==0 else -1
def flux(ch):
    # horizontal cut between rows q-1 and 0 (and vertical between columns p-1 and 0)
    h=v=0
    for (x,y,dx,dy) in ch:
        # lower end in y: start (x,y) if dy>0 else end
        if dy>0:
            if y+dy>=q: h+=chi(x,y)
        else:
            if y+dy<0: h+=chi((x+dx)%p,(y+dy)%q)
        if dx>0 and x+dx>=p: v+=chi(x,y)
    return h,v
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s): super().__init__(); s.c=Counter(); s.n=0
    def on_solution_callback(s):
        s.n+=1; ch=[e for e in E if s.Value(xv[e])]; h,v=flux(ch); s.c[(h%3,v%3)]+=1
s=cp_model.CpSolver(); s.parameters.enumerate_all_solutions=True; s.parameters.num_workers=1; s.parameters.max_time_in_seconds=tl
cb=CB(); st=s.Solve(m,cb)
print(p,q,s.StatusName(st),'solutions',cb.n,'(h mod 3, v mod 3) counts',dict(cb.c))
