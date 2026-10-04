#!/usr/bin/env python
"""Mixed side gadgets: left side A ('23 27') below row y0 and B ('02 24') from y0 up; right side B below
y1 and A from y1 up (KT Edge Searcher, 2026-10-04).  Top and bottom are T16.
Free cells: four Z x Z corners + a transition window (W columns x H rows) on each side at y0 / y1.
Objective: residual (t - side charge), so T - 8n = sum of residuals over the free cells (+ 0 on sides).
Modes: 2f (each free component alone) or tour (AddCircuit over everything).
Usage: mixed.py --n 56 --Z 8 --y0 28 --y1 28 --W 6 --H 8 --mode 2f
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csolve import solve, region, build_general, ls, ncycles, to_grid, validate, num_turns
from kt.board import tpl_moves

T16 = ['26 26 26 26 26 26 26 26', '36 26 26 46 26 46 36 26', '25 26 25 26 26 25 26 25', '16 67 06 16 06 16 16 67']
A, B = ['23 27'], ['02 24']

def skeleton(n, y0, y1, xb=0, xt=1, lo=A, hi=B, rlo=B, rhi=A):
    nb, _ = build_general(n, T16, lo, T16, rlo, phases=(xb, xt, 0, 0), Z=6)
    hm, DL, _ = tpl_moves(hi); rm, DR, _ = tpl_moves(rhi)
    for y in range(y0, n):           # left side, upper part
        for x in range(DL):
            nb[(x, y)] = {(x + d[0], y + d[1]) for d in hm[(x, 0)]}
    for y in range(y1, n):           # right side, upper part (rotated 180)
        for x in range(DR):
            c = (n - 1 - x, y); nb[c] = {(c[0] - d[0], c[1] - d[1]) for d in rm[(x, 0)]}
    return nb

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=56); ap.add_argument('--Z', type=int, default=8)
    ap.add_argument('--y0', type=int); ap.add_argument('--y1', type=int)
    ap.add_argument('--W', type=int, default=6); ap.add_argument('--H', type=int, default=8)
    ap.add_argument('--xb', type=int, default=0); ap.add_argument('--xt', type=int, default=1)
    ap.add_argument('--mode', default='2f', choices=['2f', 'tour']); ap.add_argument('--time', type=float, default=120)
    ap.add_argument('--out'); ap.add_argument('--log', action='store_true')
    a = ap.parse_args()
    n = a.n; y0 = a.y0 if a.y0 is not None else n // 2; y1 = a.y1 if a.y1 is not None else n // 2
    nb = skeleton(n, y0, y1, a.xb, a.xt)
    comps = dict(region(n, a.Z, a.Z))
    comps['Ltr'] = {(x, y) for x in range(a.W) for y in range(y0 - a.H // 2, y0 + a.H - a.H // 2)}
    comps['Rtr'] = {(n - 1 - x, y) for x in range(a.W) for y in range(y1 - a.H // 2, y1 + a.H - a.H // 2)}
    if a.mode == '2f':
        full = {c: set(v) for c, v in nb.items()}; info = {}
        for k, cells in comps.items():
            f, inf = solve(n, nb, cells, '2f', a.time, 2, res=True, log=a.log)
            if f is None: print(k, inf); info[k] = inf; continue
            for c in cells: full[c] = f[c]
            info[k] = (inf['turns'], inf['status'])
    else:
        free = set().union(*comps.values())
        full, info = solve(n, nb, free, 'tour', a.time, 2, res=True, log=a.log)
        if full is None: print('FAIL', info); return
    g = to_grid(n, full)
    ok = all(len(v) == 2 for v in full.values()) and all(c in full[v] for c in full for v in full[c])
    if not ok: print('not a 2-factor', info); return
    T = num_turns(g); LS = sum(ls(n, c, *sorted(v)) for c, v in full.items())
    print(f'n={n} Z={a.Z} y0={y0} y1={y1} W={a.W} H={a.H} mode={a.mode} T={T} T-8n={T - 8 * n} '
          f'charge={LS} cycles={ncycles(full)} tour={validate(g)} info={info}', flush=True)
    if a.out: json.dump(dict(n=n, T=T, args=vars(a), info=str(info), tour=g), open(a.out, 'w'))

if __name__ == '__main__':
    main()
