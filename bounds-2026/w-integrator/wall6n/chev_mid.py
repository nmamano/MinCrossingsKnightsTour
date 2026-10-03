#!/usr/bin/env python
"""Re-solve only the tied wall middles (2-factor, crossing objective) on top of a saved tf_lr solution.
Usage: chev_mid.py n [--w 3] [--P 4] [--lo 12] [--time 600]  (reads tf_lr_n{n}.json; KT Integrator 2026-10-03)"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from fold_assemble import edges_to_nb
from tf import twofactor
from chev_period import setup_walls, segments, crossing_pairs, full_to_edges
from chev_tf import measure
ap = argparse.ArgumentParser()
ap.add_argument('n', type=int); ap.add_argument('--w', type=float, default=3); ap.add_argument('--P', type=int, default=4)
ap.add_argument('--lo', type=int, default=12); ap.add_argument('--time', type=float, default=600)
ap.add_argument('--src', default=None)
a = ap.parse_args(); n = a.n; h = n // 2; t0 = time.time()
E, free0, mids, ties, info = setup_walls(n, a.w, a.P, a.lo)
src = json.load(open(a.src or os.path.join(HERE, f'tf_lr_n{n}.json')))['full']
full = edges_to_nb(n, E)
for k, v in src.items():
    x, y = map(int, k.split(','))
    full[(x, y)] = {tuple(p) for p in v}
# cells that were free in the source but are field cells for this w keep the source moves (consistent 2-factor)
mid = set().union(*mids.values())
print(f'n={n} w={a.w} mid={len(mid)} ties={len(ties)}', flush=True)
new, ci = twofactor(n, full, mid, time_limit=a.time, workers=2, feasibility=False, ties=ties, hint=full)
if new is None: print('none', ci); sys.exit()
cp = crossing_pairs(full_to_edges(new))
per = 2 * a.P; lo_m, hi_m = a.lo + per, h - a.lo - per; span = hi_m - lo_m
out = {nm: measure(cp, s, lev, lo_m, hi_m, a.w + 3) for nm, s, lev, d in segments(n)}
print(f'RESULT n={n} w={a.w} P={a.P}: X={len(cp)} {ci} span {span}: ' + ', '.join(f'{k} {c}/{span}={c / span:.4f}' for k, c in out.items()) + f' {time.time() - t0:.0f}s', flush=True)
json.dump(dict(n=n, full={f'{c[0]},{c[1]}': sorted(v) for c, v in new.items()}), open(os.path.join(HERE, f'tf_lr_n{n}_mid_w{a.w}.json'), 'w'))
