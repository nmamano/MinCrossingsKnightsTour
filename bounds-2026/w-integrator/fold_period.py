#!/usr/bin/env python
"""Exact slope for the fold design: periodic corridor template + reused windows.

1. Base n0: field (KT Structures, pure, t=1, arch flips) + free cluster windows (rad) + free diagonal
   corridors |y-x-1| <= band; the corridor middles (BL frame lo <= x < h-lo) are tied to period p;
   feasibility solve, then alternating (periodic middle re-solve, LNS on the rest).
2. The middle template (one period per corridor) and the content of every other free component are
   saved.  For n = n0 + 2p*k the field is rebuilt, the template is pasted along the whole corridor
   middle, and each free component is copied by translation (components matched by shape and order).
3. Every tour is validated (kt.core.validate + independent walk) and counted.
Usage: fold_period.py n0 [--K 3] [--p 6] [--lo 8] [--rad 4] [--band 1]
"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fold_assemble import setup, edges_to_nb, band_ties, ROOT
from kt.board import complete, to_grid, lns
from kt.core import validate, num_crossings, num_turns
from assemble import walk_check
import networkx as nx
sys.path.insert(0, os.path.join(ROOT, 'w-structures'))
from paste import Rot

def rotv(d, r):
    for _ in range(r):
        d = (-d[1], d[0])
    return d

def mid_cells(n, lo, band, r=None, inner=0):
    hi = n // 2 - lo - inner; lo = lo + inner
    rs = range(4) if r is None else [r]
    return {Rot((x, y), n, rr) for rr in rs for x in range(lo, hi) for y in range(x + 1 - band, x + 1 + band + 1)}

def components(cells):
    G = nx.Graph(); G.add_nodes_from(cells)
    for (x, y) in cells:
        for d in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            q = (x + d[0], y + d[1])
            if q in cells: G.add_edge((x, y), q)
    out = []
    for c in nx.connected_components(G):
        mx, my = min(p[0] for p in c), min(p[1] for p in c)
        shape = frozenset((p[0] - mx, p[1] - my) for p in c)
        out.append(((mx, my), shape, c))
    return out

def base_solve(n0, a, log=print):
    E, free, info = setup(n0, a.rad, {}, 4, band=a.band, jogD=a.jogD)
    nb = edges_to_nb(n0, E)
    ties = band_ties(n0, a.band, a.p, a.lo, n0 // 2 - a.lo)
    mid = mid_cells(n0, a.lo, a.band)
    if a.jogD:                                 # jog corridors: periodic middles as well
        h = n0 // 2
        for D in a.jogD:
            e = h - D
            if D - 3 - 3 > a.p:
                ties += band_ties(n0, 1, a.p, 3, D - 3, t=e)
                mid |= {Rot((x, y), n0, r) for r in range(4) for x in range(3, D - 3) for y in range(x + e - 1, x + e + 2)}
    full, ci = complete(n0, nb, free, time_limit=a.ftime, workers=3, feasibility=True, ties=ties)
    if full is None: raise SystemExit(f'base infeasible: {ci}')
    for rnd in range(a.rounds):
        new, ci = complete(n0, full, mid, time_limit=120, workers=3, hint=full, ties=ties)
        if new is not None: full = new
        full = lns(n0, full, free - mid, win=8, step=4, time_limit=20, rounds=1)
        log(f'  base round {rnd}: X={num_crossings(to_grid(n0, full))}')
    return full, free

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('n0', type=int); ap.add_argument('--K', type=int, default=3); ap.add_argument('--p', type=int, default=6)
    ap.add_argument('--lo', type=int, default=8); ap.add_argument('--rad', type=int, default=4)
    ap.add_argument("--band", type=int, default=1); ap.add_argument("--ftime", type=float, default=400); ap.add_argument('--rounds', type=int, default=4)
    ap.add_argument('--jogD', default=None, type=lambda v: [int(x) for x in v.split(',')]); ap.add_argument('--tag', default='FOLDX'); ap.add_argument('--step', type=int, default=0)
    a = ap.parse_args()
    n0 = a.n0
    full0, free0 = base_solve(n0, a, log=lambda s: print(s, flush=True))
    # template: moves of middle cells for one period, per corridor, in the BL frame
    tpl = {}
    for r in range(4):
        for x in range(a.lo + 3, a.lo + 3 + a.p):
            for y in range(x + 1 - a.band, x + 1 + a.band + 1):
                c = Rot((x, y), n0, r)
                tpl[(r, (x - a.lo) % a.p, y - x)] = [rotv((v[0] - c[0], v[1] - c[1]), (4 - r) % 4) for v in full0[c]]
    mid0 = mid_cells(n0, a.lo, a.band, inner=3)
    comps0 = sorted(components(free0 - mid0), key=lambda t: (len(t[2]), t[0]))
    content0 = [(off, shape, {(p[0] - off[0], p[1] - off[1]): [(v[0] - p[0], v[1] - p[1]) for v in full0[p]] for p in cells})
                for off, shape, cells in comps0]
    json.dump(dict(n0=n0, p=a.p, lo=a.lo, band=a.band, rad=a.rad,
                   template={f'{k[0]}:{k[1]},{k[2]}': v for k, v in tpl.items()},
                   components=[dict(offset=off, cells={f'{q[0]},{q[1]}': v for q, v in cont.items()}) for off, sh, cont in content0]),
              open(os.path.join(HERE, 'corners', f'{a.tag}_base_n{n0}.json'), 'w'))
    step = a.step or 2 * a.p
    print(f'{a.tag}: n0={n0} p={a.p}; transplant to n0 + {step}k', flush=True)
    for k in range(a.K + 1):
        n = n0 + step * k
        E, free, info = setup(n, a.rad, {}, 4, band=a.band, jogD=a.jogD)
        full = {c: set(v) for c, v in edges_to_nb(n, E).items()}
        mid = mid_cells(n, a.lo, a.band, inner=3)
        hi = n // 2 - a.lo - 3
        for r in range(4):
            for x in range(a.lo + 3, hi):
                for y in range(x + 1 - a.band, x + 1 + a.band + 1):
                    c = Rot((x, y), n, r)
                    ds = tpl[(r, (x - a.lo) % a.p, y - x)]
                    full[c] = {(c[0] + d[0], c[1] + d[1]) for d in (rotv(d, r) for d in ds)}
        comps = components(free - mid)
        pairs, used = [], set()
        for off, shape, cells in comps:
            best = min((j for j, b in enumerate(content0) if b[1] == shape and j not in used),
                       key=lambda j: abs(off[0] / n - content0[j][0][0] / n0) + abs(off[1] / n - content0[j][0][1] / n0), default=None)
            if best is None: break
            used.add(best); pairs.append(((off, shape, cells), content0[best]))
        if len(pairs) != len(content0) or len(comps) != len(content0):
            print(f'  n={n}: free components do not match the base ({len(comps)} vs {len(content0)})'); continue
        for (off, shape, cells), (_, _, cont) in pairs:
            for q, ds in cont.items():
                c = (off[0] + q[0], off[1] + q[1])
                full[c] = {(c[0] + d[0], c[1] + d[1]) for d in ds}
        try:
            g = to_grid(n, full)
            ok = validate(g) and walk_check(g)
        except Exception as e:
            print(f'  n={n}: BAD ({e})', flush=True); continue
        X, T = num_crossings(g), num_turns(g)
        print(f'  n={n}: valid={ok} X={X} T={T}', flush=True)
        if ok:
            json.dump(dict(n=n, crossings=X, turns=T, tour=g), open(os.path.join(HERE, 'tours', f'{a.tag}_n{n}.json'), 'w'))

if __name__ == '__main__':
    main()
