#!/usr/bin/env python3
"""The 11.3 blocking field extends to a strip of every width k with no extra crossing.

Width-k strip model S_k (w-lowerbounds/FINDINGS.md F1): strip columns 0..k-1 have degree exactly 2,
ghost columns k, k+1 degree <= 2, edges inside columns 0..k+1 with an end in the strip, no cycle.
Extension: add (x,y)-(x+2,y-1) for 2 <= x <= k-1 (all long edges are then on lines x+2y = const).
The endpoint test uses only edges between columns 0..2 that straddle the row, so F, h, a are unchanged.
Checks for k = 2..8: degrees, no cycle, 8 proper crossings per 4 rows, and the same per-row test data.
"""
from itertools import combinations
import check_frac_obstruction as B


def main():
    base = B.field()
    for k in range(2, 9):
        E = set(base)
        for y in range(B.LO, B.HI):
            for x in range(2, k):
                E.add(B.E2((x, y), (x + 2, y - 1)))
        E = {e for e in E if min(p[0] for p in e) <= k - 1 and max(p[0] for p in e) <= k + 1}
        deg = {}
        for e in E:
            for c in e: deg[c] = deg.get(c, 0) + 1
        for y in range(B.LO + 6, B.HI - 6):
            for x in range(k + 2):
                d = deg.get((x, y), 0)
                assert (d == 2) if x < k else (d <= 2), (k, x, y, d)
        par = {}
        def find(c):
            while par.get(c, c) != c: c = par[c]
            return c
        for e in E:
            a, b = map(find, tuple(e)); assert a != b; par[a] = b
        cr = sum(1 for e, f in combinations(E, 2) if B.crosses(e, f)
                 and 20 <= max(min(p[1] for p in e), min(p[1] for p in f)) < 24)
        assert cr == 8, (k, cr)
        near = {e for e in E if max(p[0] for p in e) <= 2}
        assert near == {e for e in base if max(p[0] for p in e) <= 2}
        print(f'PASS k={k}: valid S_k field, 8 crossings per 4 rows, same test edges as width two')


if __name__ == '__main__':
    main()
