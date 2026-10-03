# general: walks on the free-fold 8-cycle from (2,1) to a direction (-2,+-1); random fold constants;
# is there a simple arc from the left edge back to the left edge?  (continuous geometry)
import random, itertools
from collections import Counter
from spiral_geo import segx, simple
CYC=[(2,1),(-2,1),(1,-2),(1,2),(-2,-1),(2,-1),(-1,2),(-1,-2)]
def normal(d1,d2):
    # integer n with n.d1 = n.d2 = 1
    for a in range(-3,4):
        for b in range(-3,4):
            if a*d1[0]+b*d1[1]==1 and a*d2[0]+b*d2[1]==1: return (a,b)
def arc(steps, consts, s):
    i=0; d=CYC[0]; x,y=0.0,s; P=[(x,y)]; pos=0
    for st,t in zip(steps,consts):
        npos=(pos+st)%8; nd=CYC[npos]; n_=normal(d,nd)
        f=n_[0]*x+n_[1]*y
        if f>=t: return None
        k=t-f; x,y=x+k*d[0],y+k*d[1]
        if x<0: return None
        P.append((x,y)); d=nd; pos=npos
    if d[0]>=0: return None
    k=x/(-d[0]); x,y=0.0,y+k*d[1]; P.append((x,y))
    return P
random.seed(2); res=Counter(); ex={}
for L in range(1,7):
    for steps in itertools.product((1,-1),repeat=L):
        net=sum(steps)
        if CYC[net%8][0]!=-2: continue
        for trial in range(20000):
            consts=[random.uniform(-30,30) for _ in steps]; s=random.uniform(-30,30)
            P=arc(steps,consts,s)
            if P is None: continue
            key=(net,L)
            res[(key,'valid')]+=1
            if simple(P):
                res[(key,'simple')]+=1; ex.setdefault(key,(steps,[(round(a,1),round(b,1)) for a,b in P]))
for k in sorted(set(k for k,_ in res)):
    print('net steps',k[0],'folds',k[1],'valid',res[(k,'valid')],'simple',res[(k,'simple')], ex.get(k,'')) 
