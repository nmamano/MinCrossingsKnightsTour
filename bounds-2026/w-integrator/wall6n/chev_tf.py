#!/usr/bin/env python
"""Wall cost per level in the fold field, 2-factor relaxation (KT Integrator, 2026-10-03).
mode lr: 4 free (1,2) wall bands (chevrons BL->(n/4,n/2)->TL, BR->(3n/4,n/2)->TR), middles tied by P*(1,+-2).
mode diag: the fold design's 4 diagonal corridors (|y-x-1| <= 1, BL frame), middles tied by (p, p) (calibration:
           the fold corridor is known to cost 2/3 per level).
Model: degree 2 at every free cell (no single-cycle constraint), minimise crossings (tf.twofactor).
Measure: crossing points inside each tied middle strip, per level.
Usage: chev_tf.py n mode [--w 3] [--P 4] [--p 6] [--lo 12] [--time 900]"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from fold_assemble import setup, edges_to_nb, band_ties
from tf import twofactor
from chev_period import setup_walls, segments, crossing_pairs, full_to_edges

def measure(cp, s, lev, lo_m, hi_m, wm):
    cnt = 0
    for (a, b), (c, d) in cp:
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = a, b, c, d
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        px, py = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
        if abs(s(px, py)) <= wm and lo_m <= lev(px, py) < hi_m: cnt += 1
    return cnt

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int); ap.add_argument('mode')
    ap.add_argument('--w', type=float, default=3); ap.add_argument('--P', type=int, default=4); ap.add_argument('--p', type=int, default=6)
    ap.add_argument('--lo', type=int, default=12); ap.add_argument('--time', type=float, default=900)
    a = ap.parse_args(); n = a.n; h = n // 2; t0 = time.time()
    if a.mode == 'lr':
        E, free, mids, ties, info = setup_walls(n, a.w, a.P, a.lo)
        per = 2 * a.P
        strips = [(nm, s, lev) for nm, s, lev, d in segments(n)]
        wm = a.w + 3
    else:
        E, free, info = setup(n, 4, {}, 4, band=1)
        ties = band_ties(n, 1, a.p, a.lo, h - a.lo)
        per = a.p
        # BL corridor only (the 4 are rotations): s = transversal offset, level = x
        strips = [('D0', lambda x, y: (y - x - 1) / 1.0, lambda x, y: x)]
        wm = 1 + 3
    print(f'n={n} mode={a.mode} free={len(free)} ties={len(ties)} X_pre={info["X_pre"]}', flush=True)
    nb = edges_to_nb(n, E)
    full, ci = twofactor(n, nb, free, time_limit=a.time, workers=2, feasibility=False, ties=ties)
    if full is None:
        print(f'RESULT n={n} mode={a.mode}: none ({ci}) {time.time() - t0:.0f}s', flush=True); sys.exit()
    cp = crossing_pairs(full_to_edges(full))
    lo_m, hi_m = a.lo + per, h - a.lo - per
    out = {nm: measure(cp, s, lev, lo_m, hi_m, wm) for nm, s, lev in strips}
    span = hi_m - lo_m
    print(f'RESULT n={n} mode={a.mode} w={a.w}: X={len(cp)} {ci} levels [{lo_m},{hi_m}) span {span}: '
          + ', '.join(f'{k} {c}/{span}={c / span:.4f}' for k, c in out.items()) + f' {time.time() - t0:.0f}s', flush=True)
    json.dump(dict(n=n, mode=a.mode, full={f'{c[0]},{c[1]}': sorted(v) for c, v in full.items()}),
              open(os.path.join(HERE, f'tf_{a.mode}_n{n}.json'), 'w'))
