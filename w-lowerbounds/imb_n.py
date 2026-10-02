import itertools, sys
from imb import clusters
for n in map(int, sys.argv[1:]):
    best=None
    for ts in itertools.product(range(-1,2),repeat=4):
        E,deg,cl=clusters(n,ts,(0,0,0,0))
        tot=sum(abs(i) for c,i in cl)
        if best is None or tot<best[0]: best=(tot,ts,[i for c,i in cl])
    print(n,best,flush=True)
