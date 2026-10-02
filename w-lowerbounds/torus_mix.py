# torus p x q: columns A pure (2,1)-family, columns B every cell has one (1,2) and one (2,1) edge; zero crossings?
import sys
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
for (x,y),L in inc.items():
    if x in range(0,4):
        m.Add(sum(xv[e] for e in L if (e[2],e[3])==(2,1))==2)
    if x in range(p//2,p//2+4):
        m.Add(sum(xv[e] for e in L if (e[2],e[3])==(2,1))==1)
        m.Add(sum(xv[e] for e in L if (e[2],e[3])==(1,2))==1)
s=cp_model.CpSolver(); s.parameters.num_workers=2; s.parameters.max_time_in_seconds=300
st=s.Solve(m); print(p,q,s.StatusName(st))
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    for y in reversed(range(q)):
        row=[]
        for x in range(p):
            ds=[(e[2],e[3]) for e in inc[(x,y)] if s.Value(xv[e])]
            row.append(''.join({(2,1):'h',(1,2):'v',(2,-1):'H',(1,-2):'V'}[d] for d in sorted(ds)))
        print(' '.join(row))
