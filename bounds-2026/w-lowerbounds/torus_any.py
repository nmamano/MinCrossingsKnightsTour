# flux mod 3 for 2-factors of the 6x6 torus WITH crossings allowed (random sample via CP-SAT with random objective)
import random
from collections import Counter
from ortools.sat.python import cp_model
from strip_dp import cross
p=q=6
MOV=[(1,2),(2,1),(2,-1),(1,-2)]
E=[(x,y,d[0],d[1]) for x in range(p) for y in range(q) for d in MOV]
chi=lambda x,y: 1 if (x+y)%2==0 else -1
def ncross(ch):
    c=0
    for i,e in enumerate(ch):
        for f in ch[i:]:
            for sx in (-p,0,p):
                for sy in (-q,0,q):
                    if f==e and sx==0 and sy==0: continue
                    x,y,dx,dy=e; a,b,cc,d=f
                    if cross((x,y,x+dx,y+dy),(a+sx,b+sy,a+sx+cc,b+sy+d)): c+=1
    return c
res=Counter()
random.seed(5)
for t in range(60):
    m=cp_model.CpModel(); xv={e:m.NewBoolVar('') for e in E}
    inc={(x,y):[] for x in range(p) for y in range(q)}
    for e in E:
        x,y,dx,dy=e; inc[(x,y)].append(e); inc[((x+dx)%p,(y+dy)%q)].append(e)
    for c in inc: m.Add(sum(xv[e] for e in inc[c])==2)
    m.Maximize(sum(random.randint(0,100)*xv[e] for e in E))
    s=cp_model.CpSolver(); s.parameters.num_workers=2; s.parameters.max_time_in_seconds=10
    s.Solve(m); ch=[e for e in E if s.Value(xv[e])]
    h=0
    for (x,y,dx,dy) in ch:
        if dy>0 and y+dy>=q: h+=chi(x,y)
        if dy<0 and y+dy<0: h+=chi((x+dx)%p,(y+dy)%q)
    res[(h%3, ncross(ch)>0)]+=1
print(dict(res))
