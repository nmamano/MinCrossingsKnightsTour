# Width-one boundary bound without acyclicity: windows of column-0 choices.
# Each cell (0,y) picks 2 of 4 neighbours. c(y) = crossings between edges at y and at y+1..y+4.
import itertools
from fractions import Fraction
def sgn(v): return (v>0)-(v<0)
def turn(a,b,c): return sgn((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
def proper(e,f):
    a,b=e; c,d=f
    return turn(a,b,c)*turn(a,b,d)==-1 and turn(c,d,a)*turn(c,d,b)==-1
NB=[(1,2),(2,1),(2,-1),(1,-2)]
CH=list(itertools.combinations(range(4),2))  # 6 choices
def edges(y,ch): return [((0,y),(NB[k][0],y+NB[k][1])) for k in CH[ch]]
def ghostok(win):
    # ghost degree from column-0 edges <= 2 automatically; also distinct edges automatically
    return True
c={}
for w in itertools.product(range(6),repeat=5):
    e0=edges(0,w[0]); s=0
    for j in range(1,5):
        for f in edges(j,w[j]):
            for e in e0:
                if proper(e,f): s+=1
    c[w]=s
states=list(itertools.product(range(6),repeat=4))
idx={s:i for i,s in enumerate(states)}
N=len(states)
arcs=[(idx[w[:4]],idx[w[1:]],c[w]) for w in c]
# Bellman-Ford potential: phi(v) = min over paths ending at v of sum (c-1), from all-zero start
phi=[0]*N
for it in range(10000):
    ch=False
    for u,v,wt in arcs:
        if phi[u]+wt-1<phi[v]: phi[v]=phi[u]+wt-1; ch=True
    if not ch: break
print("iterations",it,"range",min(phi),max(phi))
from collections import Counter
print(Counter(phi))
import json
json.dump(phi,open('ktlean/scratch/col0_phi.json','w'))

# Search for a potential depending only on a subset of the 4 state positions.
for keep in itertools.chain.from_iterable(itertools.combinations(range(4),r) for r in range(1,4)):
    proj=lambda s:tuple(s[k] for k in keep)
    P=sorted(set(proj(s) for s in states)); pid={p:i for i,p in enumerate(P)}
    pa=[(pid[proj(w[:4])],pid[proj(w[1:])],c[w]) for w in c]
    ph=[0]*len(P); ok=True
    for it in range(200):
        chg=False
        for u,v,wt in pa:
            if ph[u]+wt-1<ph[v]: ph[v]=ph[u]+wt-1; chg=True
        if not chg: break
    else: ok=False
    print(keep, "ok" if ok else "no", min(ph) if ok else None)
