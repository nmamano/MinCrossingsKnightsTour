import sys
from collections import Counter
from fold_complete2 import base
n=int(sys.argv[1])
E,deg=base(n,ts=(-1,-1,-1,-1),ms=(0,1,0,1))
def imb(free):
    dem=Counter({p:2 for p in free})
    for a,b in E:
        if (a in free)!=(b in free): dem[a if a in free else b]-=1
    return sum(d if (p[0]+p[1])%2==0 else -d for p,d in dem.items()), sum(dem.values())
for X in range(n//4-1, n//4+4):
    for y0 in range(n//4-4, n//4+1):
        for y1 in range(3*n//4, 3*n//4+5):
            free={(x,y) for x in range(X) for y in range(y0,y1)}
            i,d=imb(free)
            if i==0 and d%2==0: print(X,y0,y1,'cells',len(free),'demand',d)
