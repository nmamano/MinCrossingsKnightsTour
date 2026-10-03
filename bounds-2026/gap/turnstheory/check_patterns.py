#!/usr/bin/env python3
"""Exact local checks for the two boundary fields used in the report."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'w-turnstheory'))
sys.path.insert(0,str(ROOT/'w-lowerbounds'))
from check_knight_tiles import microtiles,cross
from endpoint_independent import make_tests,norm

patterns={
    'cheap':[((0,0),(2,1)),((0,0),(1,2)),((1,0),(3,1))],
    'sharp':[((1,0),(0,2)),((2,0),(0,1)),((2,0),(1,2))],
}
for name,template in patterns.items():
    edges={norm((a[0],a[1]+y),(b[0],b[1]+y))
           for a,b in template for y in range(-8,9)}
    tiles={e:microtiles(e) for e in edges}
    counts=Counter(t for ts in tiles.values() for t in ts)
    degree=Counter(p for e in edges for p in e)
    pairs=[(e,f) for e,f in combinations(edges,2) if cross(e,f)
           and max(min(p[1] for p in e),min(p[1] for p in f))==0]
    assert all(len(tiles[e]&tiles[f])==2 for e,f in pairs)
    assert all(counts[x,0,k] in (1,2) for x in (0,1) for k in range(4))
    blocked=degree[3,0]==0 and degree[2,-2]==degree[2,2]==2
    assert blocked==(name=='sharp')
    assert len(pairs)==(2 if blocked else 1)
    residues=[]
    for coef,exc in make_tests('both'):
        F=sum(c for e,c in coef.items() if e in edges)
        assert not exc<=edges
        hs=[((1+c)//2+c*(F+2))%3 for c in (1,-1)]
        assert hs==([1,0] if blocked else [2,2])
        residues.append(hs)
    print(name, 'crossings/row',len(pairs), 'blocked',blocked,
          'endpoint residues',residues,
          'quarter counts',[[counts[x,0,k] for k in range(4)] for x in (0,1)])
print('PASS: sharp field has blocked density 1 and endpoint penalty density 3/4.')
