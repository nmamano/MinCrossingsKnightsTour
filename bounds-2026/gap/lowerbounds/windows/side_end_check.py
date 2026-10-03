#!/usr/bin/env python3
"""Independent check of a side_end.py witness (JSON): degrees, no finite cycle, crossing classes, quarter
multiplicities by exact area overlap (shapely-free: point test at 4 interior points per quarter), formula (2)
omega = chi(a)(m+ + m- + 1) mod 3 on every vertical-edge dual step, and the end-zone flux per row.
usage: side_end_check.py FILE.json"""
import sys, json
from fractions import Fraction as Fr

def chi(p): return 1 if (p[0] + p[1]) % 2 == 0 else -1
def cr(a, b, c): return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
def proper(e, f):
    a, b = e; c, d = f
    return cr(a, b, c) * cr(a, b, d) < 0 and cr(c, d, a) * cr(c, d, b) < 0

def main():
    D = json.load(open(sys.argv[1])); P, W = D['P'], D['W']
    E = [tuple(map(tuple, e)) for e in D['edges']]
    L = [((a[0], a[1] + k * P), (b[0], b[1] + k * P)) for a, b in E for k in range(-3, 4)]
    deg = {}
    for a, b in E:
        for p in (a, b): q = (p[0], p[1] % P); deg[q] = deg.get(q, 0) + 1
    for x in range(W + 2):
        for y in range(P):
            d = deg.get((x, y), 0)
            assert (d == 2) if x < W else (d <= 2), (x, y, d)
    # crossings: pairs (base edge, any lift) counted once per unordered quotient pair
    X = 0; nonS = 0
    for i, e in enumerate(E):
        for j, f in enumerate(E):
            if j <= i: continue
            if any(proper(e, ((f[0][0], f[0][1] + k * P), (f[1][0], f[1][1] + k * P))) for k in range(-2, 3)):
                if min(e[0][0], e[1][0]) <= 1 and min(f[0][0], f[1][0]) <= 1: X += 1
                else: nonS += 1
    # tiles: parallelogram with long diagonal e and short diagonal the unit grid edge at its midpoint
    def tile(e):
        (x0, y0), (x1, y1) = e; mx, my = Fr(x0 + x1, 2), Fr(y0 + y1, 2)
        s = ((mx, my - Fr(1, 2)), (mx, my + Fr(1, 2))) if abs(x1 - x0) == 2 else ((mx - Fr(1, 2), my), (mx + Fr(1, 2), my))
        return [(x0, y0), s[0], (x1, y1), s[1]]
    def ins(poly, p):
        sg = [cr(poly[i], poly[(i + 1) % 4], p) for i in range(4)]
        return all(s > 0 for s in sg) or all(s < 0 for s in sg)
    T = [tile(e) for e in L]
    def m(x, y, q):
        c = (Fr(2 * x + 1, 2), Fr(2 * y + 1, 2)); o = {'b': (0, -1), 'r': (1, 0), 't': (0, 1), 'l': (-1, 0)}[q]
        pts = [(c[0] + Fr(o[0], 3) + Fr(u, 13), c[1] + Fr(o[1], 3) + Fr(w, 17)) for u, w in ((1, 1), (-1, 1), (1, -1), (-1, -1))]
        cnt = [sum(ins(t, p) for t in T) for p in pts]
        assert len(set(cnt)) == 1; return cnt[0]
    def omega(x, r):   # dual step (x-1/2, r+1/2) -> (x+1/2, r+1/2); left cell of the crossed grid edge is (x, r+1)
        a, b = (Fr(2 * x - 1, 2), Fr(2 * r + 1, 2)), (Fr(2 * x + 1, 2), Fr(2 * r + 1, 2))
        s = chi((x, r + 1))
        for e in L:
            p, q = e
            if cr(a, b, p) * cr(a, b, q) < 0 and cr(p, q, a) * cr(p, q, b) < 0:
                s += chi(p) * (1 if cr(a, b, p) > 0 else -1)
        return s
    ok = True; ends = []
    for r in range(P):
        tot = 0
        for x in range(1, W):
            om = omega(x, r); tot += om if x >= 2 else 0
            pred = chi((x, r + 1)) * (m(x - 1, r, 'r') + m(x, r, 'l') + 1)
            if (om - pred) % 3: ok = False
        ends.append(tot % 3)
    TAB = {((0, -1), (1, 1)): -1, ((0, 0), (1, -2)): -1, ((0, 0), (2, -1)): -1, ((0, 1), (1, -1)): 1,
           ((0, 1), (2, 0)): 1, ((0, 2), (1, 0)): -1, ((1, 0), (2, 2)): -1, ((1, 1), (2, -1)): -1}
    Eset = {(a, b) for a, b in L} | {(b, a) for a, b in L}
    Fv = []; exc = []
    for r in range(P):
        Fv.append(sum(c for (a, b), c in TAB.items() if ((a[0], a[1] + r), (b[0], b[1] + r)) in Eset) % 3)
        exc.append(int(((0, r), (2, r + 1)) in Eset and ((0, r + 1), (2, r)) in Eset))
    inv = [(ends[r] + (-1) ** r * (Fv[r] - 2)) % 3 for r in range(P)]
    invm = [(ends[r] - (-1) ** r * (Fv[r] - 2)) % 3 for r in range(P)]
    print(f'  F mod 3 per row {Fv}; exception rows {exc}; E+(-1)^r(F-2) {inv}; E-(-1)^r(F-2) {invm}')
    holes = [(x, y, q) for x in range(W) for y in range(P) for q in 'brtl' if m(x, y, q) == 0]
    deep_bad = [(x, y, q) for x in range(4, W) for y in range(P) for q in 'brtl' if m(x, y, q) != 1]
    print(f'{sys.argv[1]}: degrees ok; S* crossings {X} (excess {X - P}), non-S* {nonS}; formula (2) {"ok" if ok else "FAILS"}; '
          f'end-zone flux mod 3 per row {ends}; holes {len(holes)}; bad quarters at depth >= 4: {len(deep_bad)}')

if __name__ == '__main__':
    main()
