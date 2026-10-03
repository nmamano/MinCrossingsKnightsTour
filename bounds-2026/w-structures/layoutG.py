#!/usr/bin/env python
"""Layout G (KT Structures, 2026-10-02): left/right edges A' (2,1), bottom/top edges B' (1,2),
main diagonal = free fold (A'|B'), anti-diagonal = gentle seam (A'|B' on slope -1, 1.0 per unit x).
No midpoint chevrons. Corner nests at BL and TR (diagonal fold offset t, odd untraps them).
TL and BR corners sit on the gentle seam, which carries currents -1 and 0 at the same cost.
Expected crossings: 4n (edges) + n (seam) + 2n/3 (BL, TR flux along the diagonal) + O(1) = 17n/3.

Field = fold_board BL frame (r=0) below the anti-diagonal, TR frame (r=2) above it.
Free cells: gentle-seam band |x + y - (n-1)| <= sw, diagonal flux corridors |y - x - t| <= band
(both halves of the main diagonal), and boxes of radius rad around defect clusters.
usage: layoutG.py n [n ...] [--sw 3] [--band 1] [--time 120] [--lns 0]
"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, 'w-lowerbounds'))
import fold3
from fold3 import comps
from repair import clusters, window_cells
from kt.board import complete, to_grid, lns
from kt.core import validate, num_crossings, num_turns, crossing_list


def field_G(n, ts=(1, 1, 1, 1), ms=None):
    t = ts[0]
    rotd = lambda d: (-d[1], d[0])
    v = {}
    for x in range(n):
        for y in range(n):
            r = 0 if x + y < n - 1 else 2
            p = (x, y)
            for _ in range(r):
                p = (p[1], n - 1 - p[0])
            d = (2, 1) if p[1] > p[0] + t else (-1, -2)
            for _ in range(r):
                d = rotd(d)
            v[(x, y)] = d
    return v


def build_G(n, t=1):
    old = fold3.field
    fold3.field = lambda n_, ts=(t,) * 4, ms=(0, 0, 0, 0): field_G(n_, ts)
    try:
        E, deg = fold3.build(n, ts=(t,) * 4)
    finally:
        fold3.field = old
    return E, deg


def setup(n, t=1, sw=3, band=1, rad=4, link=4):
    E, deg = build_G(n, t)
    cs, cyc, bad = comps(n, E, deg)
    free = {(x, y) for x in range(n) for y in range(n) if abs(x + y - (n - 1)) <= sw}
    if band is not None:
        free |= {(x, y) for x in range(n) for y in range(n) if abs(y - x - t) <= band}
    cls = clusters(bad, link=link)
    for c in cls:
        free |= window_cells(n, c, rad)
    info = dict(comps=len(cs), closed=len(cyc), bad=len(bad), clusters=len(cls), free=len(free),
                X_pre=len(crossing_list(E)))
    return E, free, info


def edges_to_nb(n, E):
    nb = {(x, y): set() for x in range(n) for y in range(n)}
    for a, b in E:
        nb[a].add(b); nb[b].add(a)
    return nb


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('ns', type=int, nargs='+'); ap.add_argument('--sw', type=int, default=3)
    ap.add_argument('--band', type=int, default=1); ap.add_argument('--t', type=int, default=1)
    ap.add_argument('--time', type=float, default=120); ap.add_argument('--lns', type=int, default=0)
    ap.add_argument('--rad', type=int, default=4); ap.add_argument('--feas', action='store_true')
    a = ap.parse_args()
    for n in a.ns:
        t0 = time.time()
        E, free, info = setup(n, a.t, a.sw, a.band, a.rad)
        print(f'n={n} pre: {info}', flush=True)
        nb = edges_to_nb(n, E)
        full, cinfo = complete(n, nb, free, time_limit=a.time, workers=2, feasibility=a.feas)
        if full is None:
            print(f'n={n} FAIL {cinfo}', flush=True); continue
        if a.lns:
            X0 = num_crossings(to_grid(n, full))
            full = lns(n, full, free, win=8, step=4, time_limit=20, workers=2, rounds=a.lns)
            print(f'  LNS: X {X0} -> {num_crossings(to_grid(n, full))}', flush=True)
        g = to_grid(n, full)
        ok = validate(g)
        X, T = num_crossings(g), num_turns(g)
        print(f'n={n} valid={ok} X={X} X/n={X / n:.3f} (17n/3={17 * n / 3:.0f}, 19n/3={19 * n / 3:.0f}) T={T} '
              f'{cinfo} {time.time() - t0:.0f}s', flush=True)
        if ok:
            os.makedirs(os.path.join(HERE, 'tours'), exist_ok=True)
            json.dump(dict(n=n, crossings=X, turns=T, info=info, tour=g),
                      open(os.path.join(HERE, 'tours', f'layoutG_n{n}.json'), 'w'))
