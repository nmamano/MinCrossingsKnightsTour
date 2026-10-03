"""Square-column-0 area data of the known strip fields (KT Structures, 2026-10-03).
Square column 0 = unit squares [0,1] x [j,j+1]. No candidate path of the 14n/3 and 52n/11 proofs uses these
squares, so every bad quarter there is wasted for the bound bad(U) <= 2E + 2(X-|B|).
Per 4 rows: holes (multiplicity 0), sum (m-1)_+, non-B overlap quarters in column 0, B overlap quarters."""
import sys
from collections import Counter
from itertools import combinations
sys.path[:0] = ['../../w-turnstheory', '../lowerbounds']
from check_knight_tiles import microtiles, cross
from check_frac_obstruction import field

def periodic(t):
    return {tuple(sorted(((a[0], a[1]+y), (b[0], b[1]+y)))) for a, b in t for y in range(-20, 40)}
fields = {
    'period4': {tuple(sorted(e)) for e in field()},
    'saturated': periodic([((1,0),(0,2)), ((2,0),(0,1)), ((2,0),(1,2))]),
    'cheap': periodic([((0,0),(2,1)), ((0,0),(1,2)), ((1,0),(3,1))]),
}
ROWS = range(8, 12)
for name, E in fields.items():
    E = [e for e in E if min(p[0] for p in e) <= 1]          # edges touching columns 0,1 cover all col-0 squares
    tiles = {e: microtiles(e) for e in E}
    mult = Counter(q for ts in tiles.values() for q in ts)
    col0 = [(0, j, k) for j in ROWS for k in range(4)]
    holes = sum(1 for q in col0 if mult[q] == 0)
    exc = sum(max(0, mult[q] - 1) for q in col0)
    nonB = Counter(); Bq = Counter()
    for e, f in combinations(E, 2):
        if not cross(e, f): continue
        isB = min(p[0] for p in e) == 0 and min(p[0] for p in f) == 0
        for q in tiles[e] & tiles[f]:
            if q[0] == 0 and q[1] in ROWS:
                (Bq if isB else nonB)[q] += 1
    print(f'{name:10s} per 4 rows, square column 0: holes {holes}, sum(m-1)+ {exc}, '
          f'B-overlap quarters {sum(Bq.values())}, non-B overlap quarters {sum(nonB.values())}')

print('--- endpoint squares (square column 1, row r): q = holes + quarters covered by a non-B crossing pair')
for name, E in fields.items():
    E = [e for e in E if min(p[0] for p in e) <= 1]
    tiles = {e: microtiles(e) for e in E}
    mult = Counter(q for ts in tiles.values() for q in ts)
    nonBq = set(); Bonly = set()
    for e, f in combinations(E, 2):
        if not cross(e, f): continue
        isB = min(p[0] for p in e) == 0 and min(p[0] for p in f) == 0
        for q in tiles[e] & tiles[f]:
            if not isB: nonBq.add(q)
    out = []
    for r in range(8, 16):
        qs = [(1, r, k) for k in range(4)]
        out.append(sum(1 for q in qs if mult[q] == 0 or q in nonBq))
    print(f'{name:10s} q(r), r = 8..15:', out)
