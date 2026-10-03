#!/usr/bin/env python
"""Can (1,2) defect walls replace the 4 diagonal flux corridors of the fold design? (KT Integrator, 2026-10-03)
Fold field + 13 windows (fold_assemble.setup, no diagonal corridors), plus free bands along chosen wall paths.
CP-SAT feasibility for one Hamiltonian cycle (kt.board.complete), then crossings.
Usage: chevron.py n MODE [--w 3] [--time 300]
MODE: none (windows only), diag (fold corridors, band 1, reference), lr (chevrons BL->TL and BR->TR,
      vertex on the horizontal midline at x = n/4 and 3n/4), bt (chevrons BL->BR and TL->TR)."""
import argparse, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from fold_assemble import setup, edges_to_nb, ROOT
from kt.board import complete, to_grid, lns
from kt.core import validate, num_crossings, num_turns
from assemble import walk_check

def chevron_cells(n, w, pairs):
    """Cells within horizontal (or vertical) distance w of the polyline corner -> midline vertex -> corner."""
    h = n // 2
    S = set()
    for y in range(n):
        xc = (y if y <= h else n - 1 - y) / 2.0          # (1,2) from (0,0) up to (n/4, n/2), back to (0, n-1)
        for x in range(n):
            if 'L' in pairs and abs(x - xc) <= w: S.add((x, y))
            if 'R' in pairs and abs((n - 1 - x) - xc) <= w: S.add((x, y))
    for x in range(n):
        yc = (x if x <= h else n - 1 - x) / 2.0
        for y in range(n):
            if 'B' in pairs and abs(y - yc) <= w: S.add((x, y))
            if 'T' in pairs and abs((n - 1 - y) - yc) <= w: S.add((x, y))
    return S

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int); ap.add_argument('mode')
    ap.add_argument('--w', type=float, default=3); ap.add_argument('--time', type=float, default=300)
    ap.add_argument('--obj', action='store_true', help='minimise crossings (default: feasibility)')
    ap.add_argument('--lns', type=int, default=0)
    a = ap.parse_args()
    n = a.n; t0 = time.time()
    E, free, info = setup(n, 4, {}, 4, band=1 if a.mode == 'diag' else None)
    if a.mode in ('lr', 'bt'):
        free |= chevron_cells(n, a.w, 'LR' if a.mode == 'lr' else 'BT')
    info['free'] = len(free)
    print(f'n={n} mode={a.mode} w={a.w} {info}', flush=True)
    nb = edges_to_nb(n, E)
    full, ci = complete(n, nb, free, time_limit=a.time, workers=2, feasibility=not a.obj)
    if full is None:
        print(f'RESULT n={n} mode={a.mode} w={a.w}: no tour ({ci}) {time.time() - t0:.0f}s', flush=True); sys.exit()
    for rnd in range(a.lns):
        full = lns(n, full, free, win=8, step=4, time_limit=20, workers=2, rounds=1)
        print(f'  lns round {rnd}: X={num_crossings(to_grid(n, full))} {time.time() - t0:.0f}s', flush=True)
    g = to_grid(n, full)
    ok = validate(g) and walk_check(g)
    print(f'RESULT n={n} mode={a.mode} w={a.w}: valid={ok} X={num_crossings(g)} T={num_turns(g)} {ci} {time.time() - t0:.0f}s', flush=True)
    import json
    json.dump(dict(n=n, mode=a.mode, w=a.w, tour=g), open(os.path.join(HERE, f'chev_{a.mode}_n{n}_w{a.w}.json'), 'w'))
