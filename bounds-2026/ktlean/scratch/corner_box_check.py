# New formulation: B = [0,R]^2, Q = left/bottom outside sides + top steps x in {0,1} + right steps y in {0,1}.
from itertools import product
import random, sys
sys.path.insert(0,'/home/nil/nil/knight-formation-research/w-turnstheory')
from check_corner_endpoint_charge import corner_options
K8=[(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
def sign(x): return (x>0)-(x<0)
def chi(p): return 1 if (p[0]+p[1])%2==0 else -1
def path(p,d):
    m1=(sign(d[0]),0) if abs(d[0])==2 else (0,sign(d[1]))
    m2=(sign(d[0]),sign(d[1]))
    return [p,(p[0]+m1[0],p[1]+m1[1]),(p[0]+m2[0],p[1]+m2[1]),(p[0]+d[0],p[1]+d[1])]
def setup(R):
    inB=lambda v: 0<=v[0]<=R and 0<=v[1]<=R
    # Q as set of unordered unit pairs {b,a} b in B, a outside
    Q=set()
    for y in range(0,R+1): Q.add(frozenset({(0,y),(-1,y)}))
    for x in range(0,R+1): Q.add(frozenset({(x,0),(x,-1)}))
    for x in (0,1): Q.add(frozenset({(x,R),(x,R+1)}))
    for y in (0,1): Q.add(frozenset({(R,y),(R+1,y)}))
    Qp=0
    for q in Q:
        b=[v for v in q if inB(v)][0]; Qp+=chi(b)
    def c_edge(p,d):
        P=path(p,d); s=0
        for u,w in zip(P,P[1:]):
            if frozenset({u,w}) in Q:
                s+=(1 if inB(u) else 0)-(1 if inB(w) else 0)
        return chi(p)*s
    return Qp,c_edge
for R in range(12,20):
    Qp,c_edge=setup(R)
    F=set((x,y) for x in (0,1) for y in range(R-1,R+3))|set((y,x) for x in (0,1) for y in range(R-1,R+3))
    for u in product(range(0,R+8),repeat=2):
        for d in K8:
            v=(u[0]+d[0],u[1]+d[1])
            if min(v)<0: continue
            if c_edge(u,d)!=0: assert u in F or v in F,(R,u,v)
    vals=set()
    for sL,sB in product((1,-1),repeat=2):
        E=set()
        for tr,s in ((False,sL),(True,sB)):
            f=(lambda u:(u[1],u[0])) if tr else (lambda u:u)
            for y in range(R-1,R+3):
                for x,nb in ((0,((2,y+s),(1,y+2*s))),(1,((3,y+s),(0,y-2*s)))):
                    u=f((x,y))
                    for v in nb: E.add(tuple(sorted((u,f(v)))))
        tot=Qp+sum(c_edge(u,(v[0]-u[0],v[1]-u[1])) for (u,v) in E)
        vals.add((sL,sB,Qp%3,tot%3))
    print(R,sorted(vals))
