#!/usr/bin/env python3
"""Exact local facts for FINDINGS section 11; no new stability claim."""
from itertools import product, combinations
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'w-lowerbounds'))
from endpoint_independent import make_tests, norm
from check_knight_tiles import cross

def score(F, exceptional, parity):
    c=1 if parity==0 else -1
    h=((1+c)//2+c*(F+2))%3
    return h, 2 if exceptional else {0:1,1:2,2:0}[h]

def main():
    for h,k,e,f in product(range(3),range(3),range(2),range(2)):
        loss=int(e or f or (h+k)%3==0)
        t=2 if e else {0:1,1:2,2:0}[h]
        u=2 if f else {0:1,1:2,2:0}[k]
        assert 2*loss<=t+u
    assert [(h,k) for h,k in product(range(3),repeat=2) if (h+k)%3==0]==[(0,0),(1,2),(2,1)]
    print('PASS: 36 residue/exception pairs; lost path <= sum of endpoint penalties.')
    E=set()
    for y in range(-8,9):
        E.update((norm((1,y),(0,y+2)),norm((2,y),(0,y+1)),norm((2,y),(1,y+2))))
    for coef,exc in make_tests('both'):
        F=sum(c for e,c in coef.items() if e in E)
        assert F%3==1 and not exc<=E
        assert [score(F,False,p) for p in (0,1)]==[(1,2),(0,1)]
    crossings=[(e,f) for e,f in combinations(E,2) if cross(e,f)
               and max(min(p[1] for p in e),min(p[1] for p in f))==0]
    assert len(crossings)==2, crossings
    for x in range(3):
        for y in range(-4,5):assert sum((x,y) in e for e in E)==2
    for orient in ('up','down'):
        coef,exc=make_tests(orient)[0]
        for s in (-1,1):
            P=set()
            for y in range(-8,9):
                P.update((norm((0,y),(2,y+s)),norm((0,y),(1,y+2*s)),norm((1,y),(3,y+s))))
            F=sum(c for e,c in coef.items() if e in P)
            assert F%3==2 and not exc<=P
            assert [score(F,False,p) for p in (0,1)]==[(2,0),(2,0)]
    print('PASS: P/P-prime have penalty zero in both orientations and parities.')
    print('PASS: critical period-one field has 2 crossings/row and penalty 3/4 per row.')
    print('PASS: critical field saturates all three columns 0,1,2.')
    print('No weighted strip stability certificate is claimed by this check.')
if __name__=='__main__':main()
