#!/usr/bin/env python
"""Free a whole side band (plus its two corners) on a T16-top/bottom skeleton; 2-factor or tour floor
with the residual objective (KT Edge Searcher, 2026-10-04).
Usage: band.py --n 56 --side L --W 6 --Z 8 [--mode 2f|tour] [--ring]"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csolve import solve, region, ls, ncycles, to_grid, validate, num_turns
from mixed import skeleton

ap = argparse.ArgumentParser()
ap.add_argument('--n', type=int, default=56); ap.add_argument('--side', default='L'); ap.add_argument('--W', type=int, default=6)
ap.add_argument('--Z', type=int, default=8); ap.add_argument('--xb', type=int, default=0); ap.add_argument('--xt', type=int, default=1)
ap.add_argument('--mode', default='2f'); ap.add_argument('--time', type=float, default=300); ap.add_argument('--log', action='store_true')
ap.add_argument('--ring', action='store_true', help='free a width-W ring on all four sides')
ap.add_argument('--out')
a = ap.parse_args(); n = a.n
nb = skeleton(n, n, n, a.xb, a.xt)            # left A, right B everywhere (TT16 sides)
R = region(n, a.Z, a.Z)
if a.ring:
    free = {(x, y) for x in range(n) for y in range(n) if min(x, y, n - 1 - x, n - 1 - y) < a.W}
elif a.side == 'L':
    free = set().union(*R.values()) | {(x, y) for x in range(a.W) for y in range(n)}
else:
    free = set().union(*R.values()) | {(n - 1 - x, y) for x in range(a.W) for y in range(n)}
full, info = solve(n, nb, free, a.mode, a.time, 2, res=True, log=a.log)
if full is None: print('FAIL', info); sys.exit()
g = to_grid(n, full); T = num_turns(g)
print(f'n={n} side={"ring" if a.ring else a.side} W={a.W} Z={a.Z} mode={a.mode} T-8n={T - 8 * n} '
      f'charge={sum(ls(n, c, *sorted(v)) for c, v in full.items())} cycles={ncycles(full)} tour={validate(g)} info={info}', flush=True)
if a.out: json.dump(dict(n=n, T=T, args=vars(a), info=info, tour=g), open(a.out, 'w'))
