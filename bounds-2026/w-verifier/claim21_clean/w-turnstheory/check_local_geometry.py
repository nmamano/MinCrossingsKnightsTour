"""Independent exhaustive check of the two-layer lemma, without a SAT package."""
from itertools import combinations
from collections import defaultdict
M=[(a,b) for a in (-2,-1,1,2) for b in (-2,-1,1,2) if abs(a)+abs(b)==3]
E=[]
for u in (0,1):
    for v in range(-6,7):
        p=(u+v,v)
        for dx,dy in M:
            if dx>dy:E.append((p,(p[0]+dx,p[1]+dy)))
I=defaultdict(list)
for k,e in enumerate(E):
    for p in e:I[p].append(k)
constraints=[]
for (x,y),ls in I.items():
    u=x-y;hi=1 if u==0 else 2
    lo=hi if u in (0,1) and -2<=y<=2 else 0
    constraints.append((tuple(ls),lo,hi))
central=tuple(k for k,(a,b) in enumerate(E) if a==(0,0) and b[0]-b[1]==3)
assert len(central)==2
constraints.append((central,1,1))
def area(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
for i,j in combinations(range(len(E)),2):
    a,b=E[i];c,d=E[j]
    if area(a,b,c)*area(a,b,d)<0 and area(c,d,a)*area(c,d,b)<0:
        constraints.append(((i,j),0,1))
# Fixed incoming A edges occupy -1<=u<=0, while candidate edges occupy u>=0.
# They cannot cross properly. Their degree use is already included in hi=1 at u=0.
nodes=0

def solve(values):
    global nodes
    nodes+=1
    while True:
        change=False
        for ls,lo,hi in constraints:
            yes=sum(values[k]==1 for k in ls)
            unset=[k for k in ls if values[k]<0]
            if yes>hi or yes+len(unset)<lo:return False
            if unset and (yes==hi or yes+len(unset)==lo):
                val=0 if yes==hi else 1
                for k in unset:values[k]=val
                change=True
        if not change:break
    if all(x>=0 for x in values):return True
    # Branch first in the shortest still undecided positive lower-bound constraint.
    cand=[]
    for ls,lo,hi in constraints:
        if sum(values[k]==1 for k in ls)<lo:
            us=[k for k in ls if values[k]<0]
            if us:cand.append(us)
    k=min(cand,key=len)[0] if cand else values.index(-1)
    for bit in (1,0):
        nxt=values.copy();nxt[k]=bit
        if solve(nxt):return True
    return False

assert not solve([-1]*len(E))
print('PASS: the local geometric model is UNSAT;',len(E),'edges,',len(constraints),'constraints,',nodes,'search nodes.')
