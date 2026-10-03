#!/usr/bin/env python3
"""Explicit check of the period-8 field that blocks the combined certificate (N1) at beta = 16/11.

No transfer-graph code. Field for every row y (all rows y mod 8 unless stated):
    (1,y)-(0,y+2), (2,y)-(0,y+1)                    for every y
    (2,y)-(1,y+2)                                   if y mod 8 != 2
    (3,y+1)-(1,y+2)                                 if y mod 8 == 2
(the saturated field of FINDINGS 11.4 with one edge moved every 8 rows). Checks: strip-model validity,
per 8 rows: 16 crossings, 8 crossing pairs whose two edges touch column 0, blocked rows by Turns Theory (1),
run lengths (all < 5, so K = 0), and the endpoint penalties a in both orientations and parity phases.
Ratio (X - L + K) / (sum a - (B - L)) = 8 / 5.5 = 16/11.
"""
from itertools import combinations
from fractions import Fraction
import check_frac_obstruction as B

LO, HI = -48, 96


def field():
    E = set()
    for y in range(LO, HI):
        E.add(B.E2((1, y), (0, y + 2))); E.add(B.E2((2, y), (0, y + 1)))
        if y % 8 != 2: E.add(B.E2((2, y), (1, y + 2)))
        else: E.add(B.E2((3, y + 1), (1, y + 2)))
    return E


def main():
    E = field()
    deg = {}
    for e in E:
        a, b = tuple(e)
        assert sorted((abs(a[0] - b[0]), abs(a[1] - b[1]))) == [1, 2] and min(a[0], b[0]) <= 1
        for c in e: deg[c] = deg.get(c, 0) + 1
    for y in range(LO + 8, HI - 8):
        assert deg.get((0, y), 0) == 2 and deg.get((1, y), 0) == 2
        assert deg.get((2, y), 0) <= 2 and deg.get((3, y), 0) <= 2
    par = {}
    def find(c):
        while par.get(c, c) != c: c = par[c]
        return c
    for e in E:
        a, b = map(find, tuple(e)); assert a != b; par[a] = b
    lo = 16
    pairs = [(e, f) for e, f in combinations(E, 2) if B.crosses(e, f)
             and lo <= max(min(p[1] for p in e), min(p[1] for p in f)) < lo + 8]
    X = len(pairs)
    Bc = sum(1 for e, f in pairs if any(p[0] == 0 for p in e) and any(p[0] == 0 for p in f))
    d = lambda x, y: deg.get((x, y), 0)
    blocked = [y for y in range(lo - 16, lo + 24) if d(3, y) == 0 and d(2, y - 2) == 2 and d(2, y + 2) == 2]
    runs = []; y = lo - 16
    while y < lo + 24:
        if y in blocked:
            z = y
            while z + 1 in blocked: z += 1
            runs.append(z - y + 1); y = z + 1
        else: y += 1
    print('per 8 rows: crossings', X, 'boundary pairs', Bc, '; blocked rows mod 8',
          sorted({y % 8 for y in blocked}), '; run lengths', runs)
    assert X == 16 and Bc == 8 and max(runs) <= 4
    print('PASS: valid strip field, X = 16, B = 8 per 8 rows, all blocked runs shorter than 5 (K = 0)')
    for s, name in ((1, 'up'), (-1, 'down')):
        coef = {B.E2((a[0], s * a[1]), (b[0], s * b[1])): c for (a, b), c in B.LIST}
        exc = {B.E2((a[0], s * a[1]), (b[0], s * b[1])) for a, b in B.EXC}
        best = Fraction(0)
        for phase in (0, 1):
            tot = Fraction(0)
            for y in range(lo, lo + 8):
                sel = {B.E2((a[0], a[1] - y), (b[0], b[1] - y)) for a, b in map(tuple, E)
                       if min(a[1], b[1]) <= y <= max(a[1], b[1])}
                F = sum(c for e, c in coef.items() if e in sel) % 3
                c = 1 if (y + phase) % 2 == 0 else -1
                h = ((1 + c) // 2 + c * (F + 2)) % 3
                tot += 1 if exc <= sel else {0: Fraction(1, 2), 1: 1, 2: 0}[h]
            print(f'  {name}, phase {phase}: sum a over 8 rows = {tot}')
            best = max(best, tot)
        ratio = Fraction(X - 8 + 0, 1) / (best - (Bc - 8))
        print(f'PASS: {name}: max sum a = {best}; ratio (X-L+K)/(A-(B-L)) = {ratio}')
        assert ratio == Fraction(16, 11)


if __name__ == '__main__':
    main()
