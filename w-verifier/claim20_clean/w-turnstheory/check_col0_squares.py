#!/usr/bin/env python3
"""Full-square exclusion and boundary-strip checks for FINDINGS 9.6."""
from itertools import product, combinations
from pathlib import Path
import sys
from check_knight_tiles import microtiles, cross

def main():
    moves=((1,-2),(2,-1),(2,1),(1,2));exceptions=[];count=0
    for dx,dy in moves:
        e=((0,0),(dx,dy))
        for j,(u,v) in product(range(-4,5),moves):
            f=((0,j),(u,j+v))
            if not cross(e,f):continue
            count+=1;shared=microtiles(e)&microtiles(f)
            assert shared
            for x,y,k in shared:
                assert x<=1
                if x==1:
                    assert k==3
                    expected={((0,y),(2,y+1)),((0,y+1),(2,y))}
                    assert {e,f}==expected
                    exceptions.append((e,f))
                    for sign in (-1,1):
                        allowed={((0,z),(2,z+sign)) for z in (y,y+1)}
                        assert not {e,f}<=allowed
    assert len(exceptions)==2
    print('PASS:',count,'normalised crossing pairs; only two orientations of the inward overlap exception.')
    print('PASS: each exception is excluded by two adjacent good rows of the same P/P-prime pattern.')
    # Edges incident to both axes: two at the origin, two across the corner.
    E=(((0,0),(1,2)),((0,0),(2,1)),((0,1),(2,0)),((0,2),(1,0)))
    pairs=[(e,f) for e,f in combinations(E,2) if cross(e,f)]
    assert len(pairs)==5
    assert cross(E[0],E[2]) and cross(E[1],E[2])
    print('PASS: at most five duplicate crossing pairs per corner; the asserted bound one is false.')
    import json
    root=Path(__file__).resolve().parents[1]
    tour=json.loads((root/'w-integrator/tours/FOLD24_n96.json').read_text())['tour']
    moves=((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
    def present(e):
        (x,y),(u,v)=e
        return (u-x,v-y) in [moves[int(c)] for c in tour[95-y][x]]
    def rotate(p,r):
        x,y=p
        for _ in range(r):x,y=95-y,x
        return x,y
    for r in range(4):
        selected=[tuple(rotate(p,r) for p in e) for e in E]
        selected=[e for e in selected if present(e)]
        assert sum(cross(e,f) for e,f in combinations(selected,2))==2
    print('PASS: saved FOLD24 n=96 has two duplicated pairs at each corner.')
    # Rebuild the small width-one strip graph; integer shortest-path certificate.
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'w-lowerbounds'))
    from strip_dp import build
    states,adj,W=build(1);assert W==3 and len(states)==330
    INF=10**9;pot=[INF]*len(states);pot[0]=0
    for _ in range(len(states)):
        changed=False
        for u,arcs in enumerate(adj):
            for v,w in arcs:
                if pot[v]>pot[u]+3*w-1:
                    pot[v]=pot[u]+3*w-1;changed=True
        if not changed:break
    else:raise AssertionError('negative cycle')
    assert pot[0]==0 and min(pot)==-3 and max(pot)<INF
    assert all(3*w-1+pot[u]-pot[v]>=0 for u,arcs in enumerate(adj) for v,w in arcs)
    print('PASS: width-one potential minimum -3 in units 1/3; each side has at least n-1 crossings.')
    print('Therefore the union B has at least 4n-24 crossing pairs, and avoids the retained paths\' whole squares.')

if __name__=='__main__':main()
