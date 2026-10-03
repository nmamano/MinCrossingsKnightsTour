# continuous check: can nested spiral curves (4 free folds, lines from the left edge back to it) exist?
import itertools, random
from strip_dp import cross as _c
def segx(p,q,r,s):
    def o(a,b,c):
        v=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]); return (v>1e-12)-(v<-1e-12)
    return o(p,q,r)*o(p,q,s)<0 and o(r,s,p)*o(r,s,q)<0
def curve(s,a,b,c,d):
    P=[(0.0,s)]
    x,y=0.0,s
    if y>=a: return None
    t=(a-y); x,y=x+2*t,y+t; P.append((x,y))        # (2,1) to y=a
    if x+y<=b: return None
    t=(x+y-b); x,y=x-2*t,y+t; P.append((x,y))       # (-2,1): x+y decreases by 1/step
    if x<=0 or x>=c: return None
    t=(c-x); x,y=x+t,y-2*t; P.append((x,y))         # (1,-2) to x=c
    if y-x>=d: return None
    t=(d-(y-x)); x,y=x+t,y+2*t; P.append((x,y))     # (1,2): y-x increases by 1/step
    t=x/2; x,y=0.0,y-t; P.append((x,y))            # (-2,-1) to the edge
    return P
def simple(P):
    S=list(zip(P,P[1:]))
    for i,j in itertools.combinations(range(len(S)),2):
        if j>i+1 and segx(*S[i],*S[j]): return False
    return True
def nested(P,Q):
    for s1 in zip(P,P[1:]):
        for s2 in zip(Q,Q[1:]):
            if segx(*s1,*s2): return False
    return True
random.seed(1); found=0
for trial in range(200000):
    a,b,c,d=[random.uniform(-20,20) for _ in range(4)]
    ss=[random.uniform(-20,20) for _ in range(2)]
    Ps=[curve(s,a,b,c,d) for s in ss]
    if any(P is None for P in Ps): continue
    if not all(simple(P) for P in Ps): continue
    if not nested(*Ps): continue
    found+=1
    if found<=3: print('a b c d',round(a,2),round(b,2),round(c,2),round(d,2),'s',[round(s,2) for s in ss],'curve',[(round(x,1),round(y,1)) for x,y in Ps[0]])
print('found',found)
cnt=Counter() if False else {}
from collections import Counter
fail=Counter(); ok=0
for trial in range(300000):
    a,b,c,d,s=[random.uniform(-20,20) for _ in range(5)]
    P=curve(s,a,b,c,d)
    if P is None: fail['geom']+=1; continue
    if not simple(P): fail['selfcross']+=1; continue
    ok+=1
    if ok<=2: print('simple curve',[(round(x,1),round(y,1)) for x,y in P])
print('single simple curves',ok,dict(fail))
