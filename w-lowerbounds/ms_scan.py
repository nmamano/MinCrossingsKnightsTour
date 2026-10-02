import itertools
from imb import clusters
n=32
for ms in itertools.product(range(-1,2),repeat=4):
    E,deg,cl=clusters(n,(-1,-1,-1,-1),ms)
    left=[(i,c) for c,i in cl if all(p[0]<4 for p in c) and all(n//4<p[1]<3*n//4 for p in c)]
    dem=sum(2-deg[p] for c,i in cl for p in c if all(q[0]<4 for q in c) and all(n//4<q[1]<3*n//4 for q in c))
    print(ms, [i for i,c in left], 'left-mid demand', dem)
