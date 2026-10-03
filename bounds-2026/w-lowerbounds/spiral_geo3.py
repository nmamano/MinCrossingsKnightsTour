import random
from spiral_geo import segx, simple
from spiral_geo2 import arc
def nested(P,Q):
    return not any(segx(*a,*b) for a in zip(P,P[1:]) for b in zip(Q,Q[1:]))
random.seed(3)
for steps in [(1,1,-1),(-1,-1,1),(1,-1,1),(1,1,-1,1,-1)]:
    best=None; cnt=0
    for trial in range(100000):
        consts=[random.uniform(-30,30) for _ in steps]
        ss=sorted(random.uniform(-30,30) for _ in range(6))
        Ps=[arc(steps,consts,s) for s in ss]
        if any(P is None for P in Ps) or not all(simple(P) for P in Ps): continue
        if all(nested(Ps[i],Ps[j]) for i in range(6) for j in range(i+1,6)):
            cnt+=1
            if best is None: best=(consts,ss,[[(round(a,1),round(b,1)) for a,b in P] for P in Ps[:2]])
    print(steps,'nested families of 6 curves found:',cnt, best)
