from strip_dp import cross
import itertools
def test(dA, dB, nrm, R=40):
    s = nrm[0]*dA[0]+nrm[1]*dA[1]
    f = lambda x,y: nrm[0]*x+nrm[1]*y
    E = []
    for x in range(-R,R):
        for y in range(-R,R):
            if f(x,y) <= -s: E.append((x,y,x+dA[0],y+dA[1]))
            else: E.append((x,y,x+dB[0],y+dB[1]))
    # count crossings attributed to fold cells with |x|,|y| <= R/3 : assign crossing to min lower-endpoint
    band = [(x,y) for x in range(-R//3,R//3) for y in range(-R//3,R//3) if -s < f(x,y) <= 0]
    bs=set(band)
    # crossings where the lexicographically smaller edge start is a band cell? simpler: count crossings among edges near band in window, divide by band cells in window
    W=[e for e in E if abs(e[0])<R//3 and abs(e[1])<R//3]
    cnt=sum(1 for e,g in itertools.combinations(W,2) if cross(e,g))
    print(dA,dB,nrm,'crossings',cnt,'band cells',len(band),'ratio %.3f'%(cnt/len(band)))
test((2,1),(1,-2),(3,-1))
test((2,1),(1,2),(1,1))
test((2,1),(-1,2),(1,3))
test((2,1),(2,-1),(0,1)) if False else None
