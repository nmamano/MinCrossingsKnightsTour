#!/usr/bin/env python3
"""Explicit check of the period-6 field that limits the combined certificate at beta = 8/5 even with run
constant 0 (every blocked row pays 1). No transfer-graph code. Field, every row y:
    (1,y)-(0,y+2), (2,y)-(0,y+1)          every y
    (2,y)-(1,y+2)                         if y mod 6 in {0, 4, 5}
    (3,y)-(1,y+1)                         if y mod 6 in {2, 3, 4}
Per 6 rows: 10 crossings (excess 4), 6 boundary pairs (R = 0), no blocked row (K = 0 for every run constant),
max sum a = 5/2. Ratio 4 / (5/2) = 8/5.
"""
from itertools import combinations
from fractions import Fraction
import check_frac_obstruction as B

LO, HI = -48, 96


def field():
    E = set()
    for y in range(LO, HI):
        E.add(B.E2((1, y), (0, y + 2))); E.add(B.E2((2, y), (0, y + 1)))
        if y % 6 in (0, 4, 5): E.add(B.E2((2, y), (1, y + 2)))
        if y % 6 in (2, 3, 4): E.add(B.E2((3, y), (1, y + 1)))
    return E


def main():
    E = field(); P = 6; lo = 18
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
    pairs = [(e, f) for e, f in combinations(E, 2) if B.crosses(e, f)
             and lo <= max(min(p[1] for p in e), min(p[1] for p in f)) < lo + P]
    X = len(pairs)
    Bc = sum(1 for e, f in pairs if any(p[0] == 0 for p in e) and any(p[0] == 0 for p in f))
    d = lambda x, y: deg.get((x, y), 0)
    blocked = [y for y in range(lo, lo + P) if d(3, y) == 0 and d(2, y - 2) == 2 and d(2, y + 2) == 2]
    assert X == 10 and Bc == 6 and not blocked, (X, Bc, blocked)
    print(f'PASS: valid strip field; per {P} rows X = {X}, B = {Bc}, no blocked row')
    for s, name in ((1, 'up'), (-1, 'down')):
        coef = {B.E2((a[0], s * a[1]), (b[0], s * b[1])): c for (a, b), c in B.LIST}
        exc = {B.E2((a[0], s * a[1]), (b[0], s * b[1])) for a, b in B.EXC}
        best = Fraction(0)
        for phase in (0, 1):
            tot = Fraction(0)
            for y in range(lo, lo + P):
                sel = {B.E2((a[0], a[1] - y), (b[0], b[1] - y)) for a, b in map(tuple, E)
                       if min(a[1], b[1]) <= y <= max(a[1], b[1])}
                F = sum(c for e, c in coef.items() if e in sel) % 3
                c = 1 if (y + phase) % 2 == 0 else -1
                h = ((1 + c) // 2 + c * (F + 2)) % 3
                tot += 1 if exc <= sel else {0: Fraction(1, 2), 1: 1, 2: 0}[h]
            best = max(best, tot)
        ratio = Fraction(X - P, 1) / (best - (Bc - P))
        print(f'  {name}: max sum a = {best}; ratio = {ratio}')
    print('(up must be 8/5; down is reported for information)')


if __name__ == '__main__':
    main()
