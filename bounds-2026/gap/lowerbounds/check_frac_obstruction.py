#!/usr/bin/env python3
"""Explicit check of the period-4 field that blocks beta > 1 in FINDINGS (w-turnstheory) 11.3.

Uses no transfer-graph code. The field, for every row y:
    (2,y)-(0,y+1), (3,y)-(1,y+1)                          [the P-type long edges]
    (1,y)-(0,y+2)  if y % 4 != 3                          [P-type column 0-1 edges]
    (0,y)-(1,y+2)  if y % 4 == 1                          [one reversed column 0-1 edge per period]
Checks: knight moves; columns 0,1 have degree 2 and columns 2,3 degree <= 2; no cycle; proper crossings per
4 rows (a pair is assigned to the row max(min_y(e), min_y(f))); and, for both orientations and both phases of
the row parity, the endpoint penalty a of FINDINGS 11.2 at each row. Result: 8 crossings per 4 rows, so
sum(w-1/4) = 1 per row, and in each orientation one parity phase gives a = 1 at every row. Hence
sum(w-1/4) / sum(a) = 1, and no certificate (11.5) with beta > 1 exists in the width-two strip model.
"""
from itertools import combinations

LIST = [(((0, -1), (1, 1)), -1), (((0, 0), (1, -2)), -1), (((0, 0), (2, -1)), -1), (((0, 2), (1, 0)), -1),
        (((1, 0), (2, 2)), -1), (((1, 1), (2, -1)), -1), (((0, 1), (1, -1)), 1), (((0, 1), (2, 0)), 1)]
EXC = [((0, 0), (2, 1)), ((0, 1), (2, 0))]
LO, HI = -40, 80


def E2(a, b):
    return frozenset((a, b))


def field():
    E = set()
    for y in range(LO, HI):
        E.add(E2((2, y), (0, y + 1))); E.add(E2((3, y), (1, y + 1)))
        if y % 4 != 3: E.add(E2((1, y), (0, y + 2)))
        if y % 4 == 1: E.add(E2((0, y), (1, y + 2)))
    return E


def ccw(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def crosses(e, f):
    a, b = tuple(e); c, d = tuple(f)
    d1, d2, d3, d4 = ccw(a, b, c), ccw(a, b, d), ccw(c, d, a), ccw(c, d, b)
    return d1 * d2 < 0 and d3 * d4 < 0


def main():
    E = field()
    for e in E:
        a, b = tuple(e)
        assert sorted((abs(a[0] - b[0]), abs(a[1] - b[1]))) == [1, 2]
        assert min(a[0], b[0]) <= 1 and max(a[0], b[0]) <= 3
    deg = {}
    for e in E:
        for c in e: deg[c] = deg.get(c, 0) + 1
    for y in range(LO + 4, HI - 4):
        for x in range(4):
            assert (deg.get((x, y), 0) == 2) if x < 2 else (deg.get((x, y), 0) <= 2), (x, y)
    par = {}
    def find(c):
        while par.get(c, c) != c: c = par[c]
        return c
    for e in E:
        a, b = map(find, tuple(e))
        assert a != b, 'cycle'
        par[a] = b
    print('PASS: valid width-two strip field (degrees, knight moves, no cycle)')
    lo4 = 20
    cr = sum(1 for e, f in combinations(E, 2) if crosses(e, f)
             and lo4 <= max(min(p[1] for p in e), min(p[1] for p in f)) < lo4 + 4)
    assert cr == 8, cr
    print('PASS: 8 proper crossings per 4 rows, so sum(w-1/4) = 4 per 4 rows')
    for s, name in ((1, 'up'), (-1, 'down')):
        coef = {E2((a[0], s * a[1]), (b[0], s * b[1])): c for (a, b), c in LIST}
        exc = {E2((a[0], s * a[1]), (b[0], s * b[1])) for a, b in EXC}
        best = 0
        for phase in (0, 1):
            tot = 0; rows = []
            for y in range(lo4, lo4 + 4):
                sel = {E2((a[0], a[1] - y), (b[0], b[1] - y)) for a, b in map(tuple, E)
                       if min(a[1], b[1]) <= y <= max(a[1], b[1])}
                F = sum(c for e, c in coef.items() if e in sel) % 3
                c = 1 if (y + phase) % 2 == 0 else -1
                h = ((1 + c) // 2 + c * (F + 2)) % 3
                a_ = 1 if exc <= sel else {0: 0.5, 1: 1, 2: 0}[h]
                tot += a_; rows.append((F, h, a_))
            print(f'  {name}, phase {phase}: (F, h, a) per row = {rows}, sum a = {tot}')
            best = max(best, tot)
        assert best == 4
        print(f'PASS: {name}: some parity phase gives a = 1 on every row; ratio sum(w-1/4)/sum(a) = 1')


if __name__ == '__main__':
    main()
