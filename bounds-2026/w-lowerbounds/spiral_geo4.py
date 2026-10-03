import random, itertools
from collections import Counter
from spiral_geo import segx, simple
from spiral_geo2 import arc, CYC
def nested(P,Q):
    return not any(segx(*a,*b) for a in zip(P,P[1:]) for b in zip(Q,Q[1:]))
random.seed(4); out=Counter(); ex={}
for L in range(1,6):
    for steps in itertools.product((1,-1),repeat=L):
        net=sum(steps)
        if CYC[net%8][0]!=-2: continue
        for trial in range(30000):
            consts=[random.uniform(-30,30) for _ in steps]
            s1,s2=sorted(random.uniform(-30,30) for _ in range(2))
            P,Q=arc(steps,consts,s1),arc(steps,consts,s2)
            if P is None or Q is None or not simple(P) or not simple(Q): continue
            out[(steps,'pairs')]+=1
            if nested(P,Q): out[(steps,'nested')]+=1; ex.setdefault(steps,(consts,s1,s2))
for st in sorted(set(k for k,_ in out)):
    print(st,'net',sum(st),'simple pairs',out[(st,'pairs')],'nested pairs',out[(st,'nested')])
