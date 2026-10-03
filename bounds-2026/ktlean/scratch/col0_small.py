import itertools
def sgn(v): return (v>0)-(v<0)
def turn(a,b,c): return sgn((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
def proper(e,f):
    a,b=e; c,d=f
    return turn(a,b,c)*turn(a,b,d)==-1 and turn(c,d,a)*turn(c,d,b)==-1
NB=[(1,2),(2,1),(2,-1),(1,-2)]
CH=list(itertools.combinations(range(4),2))
def edges(y,ch): return [((0,y),(NB[k][0],y+NB[k][1])) for k in CH[ch]]
for L in (2,3,4,5):
    c={}
    for w in itertools.product(range(6),repeat=L):
        c[w]=sum(proper(e,f) for j in range(1,L) for f in edges(j,w[j]) for e in edges(0,w[0]))
    for K in range(1,L):
        # potential on first K entries of state; arc w: state w[:K] -> w[1:K+1]
        S=sorted(set(w[:K] for w in c)); 
        ph={s:0 for s in S}; ok=False
        for it in range(500):
            chg=False
            for w,wt in c.items():
                u,v=w[:K],w[1:K+1]
                if ph[u]+wt-1<ph[v]: ph[v]=ph[u]+wt-1; chg=True
            if not chg: ok=True; break
        print("L",L,"K",K,"ok" if ok else "no", min(ph.values()) if ok else "", [ph[(i,)] for i in range(6)] if ok and K==1 else "")
print("choices",[[NB[k] for k in ch] for ch in CH])

C0=[(1,2),(2,1),(2,-1),(1,-2)]
def c2(A,B):
    return sum(proper(((0,0),w),((0,1),(v[0],v[1]+1))) for w in A for v in B)
subs=list(itertools.combinations(C0,2))
for f in itertools.product(range(-3,4),repeat=4):
    F=dict(zip(C0,f))
    psi=lambda A: sum(F[w] for w in A)
    if all(c2(A,B)>=1+psi(B)-psi(A) for A in subs for B in subs):
        print("linear potential f =",F, "range", min(psi(A) for A in subs), max(psi(A) for A in subs), "psi(up,up)=",psi(subs[0]),"psi(down,down)=",psi(subs[5]))
for A in subs:
    print(A,[c2(A,B) for B in subs])
