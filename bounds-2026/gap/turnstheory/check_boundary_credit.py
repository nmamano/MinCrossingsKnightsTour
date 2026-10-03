#!/usr/bin/env python3
"""Check actual outer-boundary crossing counts in the known fields."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'gap/lowerbounds'),str(ROOT/'w-turnstheory')]
from check_frac_obstruction import field
from check_knight_tiles import cross,microtiles

def periodic(template):
    return {tuple(sorted(((a[0],a[1]+y),(b[0],b[1]+y))))
            for a,b in template for y in range(-20,40)}

fields={
    'period4':{tuple(sorted(e)) for e in field()},
    'saturated':periodic([((1,0),(0,2)),((2,0),(0,1)),((2,0),(1,2))]),
    'cheap':periodic([((0,0),(2,1)),((0,0),(1,2)),((1,0),(3,1))]),
}
for name,edges in fields.items():
    pairs=[(e,f) for e,f in combinations(edges,2) if cross(e,f)
           and 8<=max(min(p[1] for p in e),min(p[1] for p in f))<12]
    boundary=[(e,f) for e,f in pairs if min(p[0] for p in e)==min(p[0] for p in f)==0]
    expected={'period4':(8,8),'saturated':(8,4),'cheap':(4,4)}[name]
    assert (len(pairs),len(boundary))==expected
    degrees=Counter(p for e in edges for p in e)
    blocked=[degrees[3,y]==0 and degrees[2,y-2]==degrees[2,y+2]==2 for y in range(8,12)]
    assert sum(blocked)==(4 if name=='saturated' else 0)
    print(name,'per four rows: X_strip =',len(pairs),'B_strip =',len(boundary),
          'blocked rows =',sum(blocked))
    if name=='period4':
        tiles={e:microtiles(e) for e in edges}
        overlaps=Counter(len(tiles[e]&tiles[f]) for e,f in pairs)
        assert overlaps=={1:4,2:4}
        multiplicity=Counter(t for ts in tiles.values() for t in ts)
        values=[multiplicity[0,y,k] for y in range(8,12) for k in range(4)]
        assert values.count(0)==2 and values.count(3)==2 and max(values)==3
        print('period4 area slack: four one-quarter pairs; two empty and two triple quarters at depth zero.')
print('PASS: boundary surplus removes period4 obstruction from requested inequality R1.')
