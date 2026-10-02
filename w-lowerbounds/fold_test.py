# test: A lines direction dA turn into B lines direction dB at fold band  t-s < f <= t, f = normal . (x,y)
import sys
from strip_dp import cross
def test(dA, dB, nrm, R=30):
    s = nrm[0]*dA[0]+nrm[1]*dA[1]
    assert s == nrm[0]*dB[0]+nrm[1]*dB[1] and s > 0
    f = lambda x,y: nrm[0]*x+nrm[1]*y
    t = 0
    E = []
    for x in range(-R,R):
        for y in range(-R,R):
            if f(x,y) <= t - s:   # A edge P -> P+dA stays in f<=t
                E.append((x,y,x+dA[0],y+dA[1]))
            if f(x,y) > t - s:    # B edge Q -> Q+dB
                E.append((x,y,x+dB[0],y+dB[1]))
    # count crossings in a central window along fold
    cnt = 0; cells=0
    import itertools
    def inwin(e): return abs(e[0])<=R//3 and abs(e[1])<=R//3
    W = [e for e in E if inwin(e)]
    for e,g in itertools.combinations(W,2):
        if cross(e,g): cnt+=1
    # degree check
    from collections import Counter
    deg = Counter()
    for e in E:
        deg[(e[0],e[1])]+=1; deg[(e[2],e[3])]+=1
    bad = [c for c,d in deg.items() if d!=2 and abs(c[0])<R//2 and abs(c[1])<R//2]
    print(dA,dB,nrm,'crossings in window',cnt,'bad deg',len(bad))
test((2,1),(1,-2),(3,-1))
test((2,1),(1,2),(1,1))
test((2,1),(-1,2),(1,3))
