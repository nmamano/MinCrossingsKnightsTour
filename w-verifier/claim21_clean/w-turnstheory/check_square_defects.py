#!/usr/bin/env python3
"""Exact local checks for FINDINGS section 9; standard library, no solver."""
from collections import Counter, defaultdict
from itertools import product
from check_knight_tiles import MOV, microtiles

def dual_vertices(t):
    x,y,k=t;c=(2*x+1,2*y+1);d=((0,-2),(2,0),(0,2),(-2,0))[k]
    return {c,(c[0]+d[0],c[1]+d[1])}

def seam_check():
    # Out-directions depend only on h=y-x. Both decrease h by three.
    C=Counter();g=defaultdict(set);tiles={}
    for x,y in product(range(-12,13),repeat=2):
        dx,dy=(1,-2) if y>=x else (2,-1)
        p=(x,y);q=(x+dx,y+dy);e=tuple(sorted((p,q)))
        g[p].add(q);g[q].add(p);tiles[e]=microtiles(e);C.update(tiles[e])
    for x,y in product(range(-6,7),repeat=2):
        assert len(g[x,y])==2
        expected=[0,2,2,0] if y==x-2 else [1,1,1,1]
        assert [C[x,y,k] for k in range(4)]==expected
    # All possible crossings at one seam square are enumerated exactly.
    owners=defaultdict(list)
    for e,T in tiles.items():
        for t in T:owners[t].append(e)
    e=tuple(sorted(((0,-1),(2,-2))));f=tuple(sorted(((0,0),(1,-2))))
    for k in (1,2):assert set(owners[0,-2,k])=={e,f}
    assert len(tiles[e]&tiles[f])==2
    values=[]
    for y in range(-6,7):
        chi=1 if y%2==0 else -1
        values.append(chi*(C[0,y-1,2]+C[0,y,0]-2))
    assert sum(values)==-2 and sum(values)%3==1
    print('PASS: degree-two gentle seam; J=Q=0; height jump 1 mod 3; one half-area crossing per (1,1) period.')

def main():
    checked=0
    for a in product(range(2),repeat=2):
        for dx,dy in MOV:
            e=(a,(a[0]+dx,a[1]+dy));squares=defaultdict(list)
            for x,y,k in microtiles(e):squares[x,y].append(k)
            assert len(squares)==2
            for ks in squares.values():
                assert len(ks)==2 and (ks[0]-ks[1])%4 in (1,3)
                assert sum((-1)**k for k in ks)==0
            checked+=1
    print('PASS:',checked,'translated edge types; two adjacent quarters per visited square.')
    pairs=0
    for dx,dy in MOV:
        e=((0,0),(dx,dy))
        for x,y in product(range(-4,5),repeat=2):
            for u,v in MOV:
                f=((x,y),(x+u,y+v))
                if e==f:continue
                shared=microtiles(e)&microtiles(f)
                if shared:
                    assert set.intersection(*(dual_vertices(t) for t in shared))
                    pairs+=1
    print('PASS:',pairs,'overlapping tile pairs; their dual edges have a common vertex.')
    for n in (32,34,48,96):
        vertices=set();count=0
        for r in range(4):
            for R in range(12,n//2-3):
                P={(2*R+1,y) for y in range(3,2*R+2,2)}|{(x,2*R+1) for x in range(3,2*R+2,2)}
                for _ in range(r):P={(2*(n-1)-y,x) for x,y in P}
                assert not vertices&P
                assert all(3<=x<=2*n-5 and 3<=y<=2*n-5 for x,y in P)
                vertices|=P;count+=1
        assert count==2*n-60
    print('PASS: corner paths are vertex-disjoint; all incident squares avoid boundary tile overlaps.')
    seam_check()
    print('The arbitrary-size disjointness and alternating-sum implications are proved in section 9.')

if __name__=='__main__':main()
