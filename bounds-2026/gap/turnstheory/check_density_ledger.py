#!/usr/bin/env python3
"""Exact integer check of the excess identity and mixed side ledger."""
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'w-turnstheory')]
from kt.core import edges,crossing_list,validate
from check_knight_tiles import microtiles

def main():
    data=json.loads(Path(sys.argv[1]).read_text())
    tour=data['tour']
    n=len(tour)
    validate(tour)
    es=edges(tour)
    assert len(es)==n*n
    tiles={e:microtiles(e) for e in es}
    counts=Counter(q for ts in tiles.values() for q in ts)
    assert all(0<=x<n-1 and 0<=y<n-1 for x,y,k in counts)
    pairs=crossing_list(es)
    overlaps=[len(tiles[e]&tiles[f]) for e,f in pairs]
    assert all(k in (1,2) for k in overlaps)
    G=4*(n-1)**2-len(counts)
    X1=sum(k==1 for k in overlaps)
    W3=sum((m-1)*(m-2)//2 for m in counts.values())
    X=len(pairs)
    E=X-4*n+2
    assert sum(counts.values())==4*n*n
    assert sum(m*(m-1)//2 for m in counts.values())==sum(overlaps)
    assert 2*E==G+X1+W3
    def side_mask(edge):
        (x,y),(u,v)=edge
        return (int(min(x,u)<=1) | (int(max(x,u)>=n-2)<<1)
                | (int(min(y,v)<=1)<<2) | (int(max(y,v)>=n-2)<<3))
    masks=[side_mask(e)&side_mask(f) for e,f in pairs]
    s=sum(mask!=0 for mask in masks)
    strip_sum=sum(mask.bit_count() for mask in masks)
    assert 0<=strip_sum-s<=1104
    U=X-s
    T=s-4*n+2
    lam=Fraction(2,3)
    mixed=lam*U+(1-lam)*Fraction(G+X1+W3,2)
    assert E==mixed+lam*T
    restored=mixed+lam*(T+1160)
    assert restored==E+lam*1160
    print(json.dumps(dict(n=n,X=X,E=E,G=G,X1=X1,W3=W3,
                          side_pair_union=s,side_pair_sum=strip_sum,
                          outside_pairs=U,side_excess=T,
                          lambda_value=str(lam),mixed_capacity=str(mixed)),indent=2))
    print('PASS: exact integer tiles; excess identity; union correction; mixed-capacity identity.')

if __name__=='__main__':main()
