#!/usr/bin/env python
"""Periodic free ring: four Z x Z corners + side bands that are free but periodic (ties), on the TT16
skeleton (interior lines x + 2y = c fixed).  Finds the best periodic side gadgets jointly with the corners
(KT Edge Searcher, 2026-10-04).  Objective: residual, so T - 8n is the objective value.
Usage: pring.py --n 56 --Z 8 --Db 4 --Dl 4 --P 8 --Q 4 --sides BTLR --mode 2f
  --sides: which bands are free (B bottom, T top, L left, R right); the other bands keep the TT16 gadget.
  --m: margin (cells) between a corner zone and the first tied cell."""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csolve import solve, region, ls, ncycles, to_grid, validate, num_turns
from mixed import skeleton

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=56); ap.add_argument('--Z', type=int, default=8)
    ap.add_argument('--Db', type=int, default=4); ap.add_argument('--Dl', type=int, default=4)
    ap.add_argument('--P', type=int, default=8); ap.add_argument('--Q', type=int, default=4)
    ap.add_argument('--m', type=int, default=0); ap.add_argument('--sides', default='BTLR')
    ap.add_argument('--mode', default='2f'); ap.add_argument('--time', type=float, default=600)
    ap.add_argument('--workers', type=int, default=2); ap.add_argument('--log', action='store_true')
    ap.add_argument('--out')
    ap.add_argument('--iters', type=int, default=0, help='2f + subtour cut loop: max iterations (0 = off)')
    ap.add_argument('--defect', type=int, default=0, help='length of a non-periodic window in the middle of each side')
    ap.add_argument('--defectW', type=int, default=6, help='depth of that window (free cells)')
    ap.add_argument('--final', type=float, default=0, help='after the cut loop: tour-mode solve with all cuts, '
                    'hinted by the TT16-skeleton tour, for this many seconds')
    ap.add_argument('--budget', type=float, default=2700, help='cut loop: wall-clock seconds')
    ap.add_argument('--stop', type=int, default=-14, help='cut loop: stop once the proven bound is >= this value')
    a = ap.parse_args()
    nb, free, ties, lo = setup(a)
    n, Z, P, Q = a.n, a.Z, a.P, a.Q
    if a.iters:
        full, info = cutloop(a, nb, free, ties)
    else:
        full, info = solve(n, nb, free, a.mode, a.time, a.workers, res=True, log=a.log, ties=ties)
    report(a, full, info, lo)

def components(full):
    seen, out = set(), []
    for c in full:
        if c in seen: continue
        comp, st = set(), [c]
        while st:
            v = st.pop()
            if v in comp: continue
            comp.add(v); st.extend(full[v])
        seen |= comp; out.append(comp)
    return out

def cutloop(a, nb, free, ties):
    import time
    cuts, hint, t0, LB = [], None, time.time(), -10**9
    for it in range(a.iters):
        full, info = solve(a.n, nb, free, '2f', a.time, a.workers, res=True, ties=ties, cuts=cuts, hint=hint)
        if full is None: return None, info
        comps = components(full)
        print(f'iter {it}: obj {info["turns"]} bound {info["bound"]} {info["status"]} cycles {len(comps)} '
              f'cuts {len(cuts)} t={time.time() - t0:.0f}s', flush=True)
        LB = max(LB, info['bound'])
        info['LB'] = LB
        if len(comps) == 1: return full, info
        if LB >= a.stop:
            print(f'STOP: tour lower bound {LB} >= {a.stop} for this family', flush=True); return None, info
        if time.time() - t0 > a.budget:
            print(f'budget; tour lower bound {LB}', flush=True)
            cuts += [S for S in comps]
            return final(a, nb, free, ties, cuts, LB, info)
        cuts += [S for S in comps]
        hint = full
    print(f'iteration limit; tour lower bound {LB}', flush=True)
    return final(a, nb, free, ties, cuts, LB, info)

def final(a, nb, free, ties, cuts, LB, info):
    if not a.final: return None, info
    base, binfo = solve(a.n, nb, set().union(*region(a.n, 6, 6).values()), 'tour', 120, 1, res=True)
    print(f'hint tour (TT16 skeleton, 6x6 corners): {binfo}', flush=True)
    full, inf2 = solve(a.n, nb, free, 'tour', a.final, a.workers, res=True, ties=ties, cuts=cuts, hint=base)
    if full is None: return None, inf2
    inf2['LB'] = max(LB, inf2['bound'])
    print(f'final tour solve: {inf2}', flush=True)
    return full, inf2

def setup(a):
    n, Z, P, Q = a.n, a.Z, a.P, a.Q
    nb = skeleton(n, n, n, 0, 1)                 # TT16: left '23 27', right '02 24', T16 top/bottom
    free = set().union(*region(n, Z, Z).values())
    ties = []
    lo, hi = Z + a.m, n - Z - a.m
    if 'B' in a.sides:
        free |= {(x, y) for x in range(n) for y in range(a.Db)}
        ties += [((x, y), (x + P, y)) for y in range(a.Db) for x in range(lo, hi - P)]
    if 'T' in a.sides:
        free |= {(x, n - 1 - y) for x in range(n) for y in range(a.Db)}
        ties += [((x, n - 1 - y), (x + P, n - 1 - y)) for y in range(a.Db) for x in range(lo, hi - P)]
    if 'L' in a.sides:
        free |= {(x, y) for x in range(a.Dl) for y in range(n)}
        ties += [((x, y), (x, y + Q)) for x in range(a.Dl) for y in range(lo, hi - Q)]
    if 'R' in a.sides:
        free |= {(n - 1 - x, y) for x in range(a.Dl) for y in range(n)}
        ties += [((n - 1 - x, y), (n - 1 - x, y + Q)) for x in range(a.Dl) for y in range(lo, hi - Q)]
    if a.defect:
        h0, h1 = n // 2 - a.defect // 2, n // 2 - a.defect // 2 + a.defect
        W = a.defectW
        win = {'B': {(x, y) for x in range(h0, h1) for y in range(W)},
               'T': {(x, n - 1 - y) for x in range(h0, h1) for y in range(W)},
               'L': {(x, y) for x in range(W) for y in range(h0, h1)},
               'R': {(n - 1 - x, y) for x in range(W) for y in range(h0, h1)}}
        D = set().union(*(win[k] for k in a.sides))
        free |= D
        # break every tie chain at the window: a tie may not jump over or touch it
        def crosses(c1, c2):
            if c1 in D or c2 in D: return True
            if c1[1] == c2[1] and c1[1] < W or c1[1] == c2[1] and c1[1] >= n - W:   # horizontal tie
                return c1[0] < h1 and c2[0] >= h0
            if c1[0] == c2[0]:                                                      # vertical tie
                return c1[1] < h1 and c2[1] >= h0
            return False
        ties = [t for t in ties if not crosses(*t)]
    return nb, free, ties, lo

def report(a, full, info, lo):
    n, Z, P, Q = a.n, a.Z, a.P, a.Q
    if full is None: print('FAIL', info, flush=True); return
    g = to_grid(n, full); T = num_turns(g)
    LS = sum(ls(n, c, *sorted(v)) for c, v in full.items())
    print(f'n={n} Z={Z} Db={a.Db} Dl={a.Dl} P={P} Q={Q} m={a.m} sides={a.sides} mode={a.mode} T={T} T-8n={T - 8 * n} '
          f'charge={LS} cycles={ncycles(full)} tour={validate(g)} info={info}', flush=True)
    # print the band patterns (one period) in board.js codes
    if 'B' in a.sides:
        print('bottom period (rows top-first):', [' '.join(g[n - 1 - y][x] for x in range(lo, lo + P)) for y in range(a.Db - 1, -1, -1)])
    if 'L' in a.sides:
        print('left period (rows top-first):', [' '.join(g[n - 1 - y][x] for x in range(a.Dl)) for y in range(lo + Q - 1, lo - 1, -1)])
    if a.out: json.dump(dict(n=n, T=T, args=vars(a), info=info, tour=g), open(a.out, 'w'))

if __name__ == '__main__':
    main()
