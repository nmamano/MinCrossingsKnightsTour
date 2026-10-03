#!/usr/bin/env python
"""Per-corner 2-factor floor sweep over side gadgets and phases (KT Edge Searcher, 2026-10-04).

T(tour or 2-factor) = 8n + sum of residuals (t - side charge); the side gadgets here have residual 0,
so T - 8n = sum of the four corner-region residuals.  Each corner region residual depends only on the
two gadgets and phases that meet at that corner, so each corner is solved alone (2-factor, degree 2).
Output: JSON lines {corner, n, B/T gadget, L/R gadget, phases, res, status}.
Usage: sweep.py --n 56 --Z 8 --out sweep_Z8_n56.jsonl
"""
import argparse, json, os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csolve import solve, region, build_general

T16 = ['26 26 26 26 26 26 26 26', '36 26 26 46 26 46 36 26', '25 26 25 26 26 25 26 25', '16 67 06 16 06 16 16 67']
LEFT = {'A23_27': ['23 27'], 'B02_24': ['02 24'], 'C_lanes4o0': ['23 24', '23 24', '02 27', '02 27']}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, required=True); ap.add_argument('--Z', type=int, default=8)
    ap.add_argument('--time', type=float, default=60); ap.add_argument('--out', required=True)
    ap.add_argument('--corners', default='BL,BR,TL,TR')
    a = ap.parse_args()
    n, Z = a.n, a.Z
    f = open(a.out, 'a')
    for k in a.corners.split(','):
        for ln, Lt in LEFT.items():
            Q = len(Lt)
            for xp in range(8):
                for yp in range(Q):
                    # phases (xb, xt, yl, yr): the corner's own two phases are xp (bottom or top) and yp
                    ph = {'BL': (xp, 0, yp, 0), 'BR': (xp, 0, 0, yp), 'TL': (0, xp, yp, 0), 'TR': (0, xp, 0, yp)}[k]
                    nb, _ = build_general(n, T16, Lt, T16, Lt, phases=ph, Z=6)
                    cells = region(n, Z, Z)[k]
                    full, info = solve(n, nb, cells, '2f', a.time, 2, res=True)
                    row = dict(corner=k, n=n, Z=Z, side=ln, xp=xp, yp=yp,
                               res=None if full is None else info['turns'],
                               bound=None if full is None else info['bound'],
                               status=info if full is None else info['status'])
                    f.write(json.dumps(row) + '\n'); f.flush()
                    print(row, flush=True)

if __name__ == '__main__':
    main()
