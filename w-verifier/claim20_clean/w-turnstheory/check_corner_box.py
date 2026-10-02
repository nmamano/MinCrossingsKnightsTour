#!/usr/bin/env python3
"""Exact one-row corner charge check. Standard library; no corner enumeration."""
from itertools import product

MOVES = [(a,b) for a,b in product(range(-2,3), repeat=2)
         if sorted((abs(a),abs(b))) == [1,2]]
def chi(p): return 1 if sum(p)%2 == 0 else -1
def orient(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def sign(x): return (x>0)-(x<0)
def flux(e, step):
    a,b = step
    p,q = [tuple(2*t for t in v) for v in e]
    if orient(a,b,p)*orient(a,b,q)>=0 or orient(p,q,a)*orient(p,q,b)>=0:
        return 0
    return chi(e[0])*sign(orient(a,b,p))

def main():
    # Top two dual steps, directed left: outward is upward. Coordinates doubled.
    top = [((3,1),(1,1)), ((1,1),(-1,1))]
    edges = set()
    for p in product(range(4),range(-2,3)):
        for dx,dy in MOVES:
            q = (p[0]+dx,p[1]+dy)
            if 0<=q[0]<=3 and -2<=q[1]<=2:
                edges.add(tuple(sorted((p,q))))
    coeff = {e:sum(flux(e,s) for s in top) for e in edges}
    coeff = {e:c for e,c in coeff.items() if c}
    # A crossing lies at 0<=x<1.5, y=.5. Its endpoint box gives
    # 0<=endpoint x<=3 and -1<=endpoint y<=2, so the list is exhaustive.
    for p,q in coeff:
        assert min(p[0],q[0])<2
        assert min(p[1],q[1])<=0<max(p[1],q[1])
    # Equivalence with the earlier eight-edge endpoint test F=-1 mod 3.
    old_raw = [((0,-1),(1,1),-1), ((0,0),(1,-2),-1),
               ((0,0),(2,-1),-1), ((0,1),(1,-1),1),
               ((0,1),(2,0),1), ((0,2),(1,0),-1),
               ((1,0),(2,2),-1), ((1,1),(2,-1),-1)]
    old = {tuple(sorted((p,q))):c for p,q,c in old_raw}
    for e in edges | set(old):
        assert coeff.get(e,0)-old.get(e,0)==int((0,0) in e)
    # Thus new end flux = F + degree(0,0) = F + 2.
    for s in (-1,1):
        selected = set()
        for y in range(-4,5):
            for p,ns in (((0,y),((2,y+s),(1,y+2*s))),
                         ((1,y),((3,y+s),(0,y-2*s)))):
                for q in ns: selected.add(tuple(sorted((p,q))))
        assert sum(c for e,c in coeff.items() if e in selected)==1
        # Transpose and reverse the dual steps: right end, outward right.
        tr=lambda p:(p[1],p[0])
        right=[(tr(b),tr(a)) for a,b in top]
        assert sum(sum(flux((tr(p),tr(q)),t) for t in right)
                   for p,q in selected)==1
    for R in range(12,20):
        outer=2*sum(chi((0,y)) for y in range(R+1))
        assert outer==1+chi((0,R))
        end_grid=2*(chi((0,R))+chi((1,R)))
        assert end_grid==0
        assert (outer+end_grid+2*chi((0,R)))%3==1
    print('PASS: all',len(coeff),'top-end edges straddle the one critical row.')
    print('PASS: top and right end flux = chi(R) for either pattern sign.')
    print('PASS: new endpoint test equals the earlier test plus degree two.')
    print('PASS: outside flux + end flux = 1 + 3 chi(R) = 1 mod 3.')
if __name__=='__main__': main()
