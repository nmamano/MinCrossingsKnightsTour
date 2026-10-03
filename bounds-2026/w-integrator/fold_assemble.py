#!/usr/bin/env python
"""Fold design (KT Structures) -> validated tours with the Integrator solver.

Field and templates come from w-structures (paste_field: fold field t, arch flips, diagonal flux
templates); free windows = boxes of radius rad around defect clusters (w-structures/repair.py).
Completion: kt.board.complete (fixed paths contracted, CP-SAT AddCircuit -> one cycle per solve).
Usage: fold_assemble.py n [n ...] [--rad 4] [--time 120] [--tgs "{0:1,1:1,2:1,3:1}"] [--link 4]
"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, 'w-structures'))
_cwd = os.getcwd()
os.chdir(os.path.join(ROOT, 'w-structures'))       # paste.load reads its json relative to cwd
from paste import paste_field
from fold3 import comps
from repair import clusters, window_cells
from imbal import imbalance
os.chdir(_cwd)
from kt.board import complete, to_grid, lns
from kt.core import validate, num_crossings, num_turns, crossing_list
from assemble import walk_check, brute_crossings

def setup(n, rad, tgs, link, t=1, band=None, jogD=None):
    h = n // 2
    fl = lambda r, y: h - n // 4 <= y < h
    cwd = os.getcwd(); os.chdir(os.path.join(ROOT, 'w-structures'))
    try:
        if jogD is not None:                     # jog bands instead of arch flips
            import fold3, fold_jog
            old = fold3.field
            fold3.field = fold_jog.make_field(lambda m: [m // 2 - D for D in jogD], d=1, ts=(t,) * 4)
            try:
                E, deg = fold3.build(n, ts=(t,) * 4)
            finally:
                fold3.field = old
        else:
            E, deg = paste_field(n, t, tgs, fl, hi=h - 4)
    finally:
        os.chdir(cwd)
    cs, cyc, bad = comps(n, E, deg)
    cls = clusters(bad, link=link)
    free = set()
    for c in cls:
        free |= window_cells(n, c, rad)
    if jogD is not None:                       # free corridors along every jog band (carry its +-3 end charges)
        from paste import Rot
        for r in range(4):
            for D in jogD:
                e = h - D
                for x in range(0, h):
                    for y in range(x + e - 1, x + e + 2):
                        if 0 <= y < h + 1: free.add(Rot((x, y), n, r))
    if band is not None:                       # free diagonal flux corridors, corner -> centre
        from paste import Rot
        w = band
        for r in range(4):
            for x in range(0, h):
                for y in range(x + t - w, x + t + w + 1):
                    if 0 <= y < n: free.add(Rot((x, y), n, r))
    info = dict(comps=len(cs), closed=len(cyc), bad=len(bad), clusters=len(cls), free=len(free),
                imb=[imbalance(n, E, window_cells(n, c, rad)) for c in cls], X_pre=len(crossing_list(E)))
    return E, free, info

def band_ties(n, band, p, lo, hi, t=1):
    """Tie every free-free edge of the 4 diagonal corridors (BL frame: |y-x-t| <= band, lo <= x < hi)
    to its translate by (p, p): the corridor middle becomes periodic with period p."""
    from paste import Rot
    MOV = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
    ties = []
    inb = lambda c: lo <= c[0] < hi and abs(c[1] - c[0] - t) <= band
    for r in range(4):
        for x in range(lo, hi - p):
            for y in range(x + t - band, x + t + band + 1):
                c = (x, y)
                for d in MOV:
                    q = (x + d[0], y + d[1])
                    c2, q2 = (x + p, y + p), (q[0] + p, q[1] + p)
                    if inb(q) and inb(c2) and inb(q2):
                        ties.append(((Rot(c, n, r), Rot(q, n, r)), (Rot(c2, n, r), Rot(q2, n, r))))
    return ties

def edges_to_nb(n, E):
    nb = {(x, y): set() for x in range(n) for y in range(n)}
    for a, b in E:
        nb[a].add(b); nb[b].add(a)
    return nb

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ns', type=int, nargs='+'); ap.add_argument('--rad', type=int, default=4)
    ap.add_argument('--time', type=float, default=120); ap.add_argument('--link', type=int, default=4)
    ap.add_argument('--tgs', default='{0: 1, 1: 1, 2: 1, 3: 1}'); ap.add_argument('--tag', default='FOLD')
    ap.add_argument('--brute', action='store_true')
    ap.add_argument('--lns', type=int, default=0, help='LNS rounds after the first solve')
    ap.add_argument('--win', type=int, default=8)
    ap.add_argument('--period', type=int, default=0)
    ap.add_argument('--jogD', default=None, help='comma list of band distances D (bands at h - D); "auto" = jog_rule2')
    ap.add_argument('--lo', type=int, default=8)
    ap.add_argument('--feas', action='store_true', help='first solve without objective (LNS optimises)')
    ap.add_argument('--band', type=int, default=None, help='free diagonal corridors of half-width band')
    a = ap.parse_args()
    tgs = eval(a.tgs)
    for n in a.ns:
        t0 = time.time()
        jd = None
        if a.jogD == 'auto':
            from jog_rule2 import find_bands
            jd = find_bands(n)[1]; print(f'  jog bands D = {jd}', flush=True)
        elif a.jogD:
            jd = [int(v) for v in a.jogD.split(',')]
        E, free, info = setup(n, a.rad, tgs, a.link, band=a.band, jogD=jd)
        print(f'n={n} pre: {info}', flush=True)
        nb = edges_to_nb(n, E)
        ties = band_ties(n, a.band, a.period, a.lo, n // 2 - a.lo) if a.period else ()
        full, cinfo = complete(n, nb, free, time_limit=a.time, workers=3, feasibility=a.feas, ties=ties)
        if full is None:
            print(f'n={n} FAIL {cinfo}', flush=True); continue
        if a.lns and a.period:
            from paste import Rot
            X0 = num_crossings(to_grid(n, full))
            hi = n // 2 - a.lo
            mid = {Rot((x, y), n, r) for r in range(4) for x in range(a.lo, hi)
                   for y in range(x + 1 - a.band, x + 1 + a.band + 1)}
            for rnd in range(a.lns):
                new, ci = complete(n, full, mid, time_limit=a.time, workers=3, hint=full, ties=ties)
                if new is not None: full = new
                print(f'   round {rnd}: periodic middle {ci["status"] if new else ci}, X={num_crossings(to_grid(n, full))}', flush=True)
                full = lns(n, full, free - mid, win=a.win, step=a.win // 2, time_limit=20, rounds=1,
                           log=lambda s: print('  ', s, flush=True))
                print(f'   round {rnd}: X={num_crossings(to_grid(n, full))}', flush=True)
        elif a.lns:
            X0 = num_crossings(to_grid(n, full))
            full = lns(n, full, free, win=a.win, step=a.win // 2, time_limit=20, rounds=a.lns,
                       log=lambda s: print('  ', s, flush=True))
            print(f'  LNS: X {X0} -> {num_crossings(to_grid(n, full))}', flush=True) if a.lns else None
        g = to_grid(n, full)
        ok = validate(g) and walk_check(g)
        X, T = num_crossings(g), num_turns(g)
        line = f'n={n} valid={ok} X={X} X/n={X / n:.3f} T={T} {cinfo} {time.time() - t0:.0f}s'
        if a.brute: line += f' Xbrute={brute_crossings(g)}'
        print(line, flush=True)
        if ok:
            os.makedirs(os.path.join(HERE, 'tours'), exist_ok=True)
            json.dump(dict(n=n, crossings=X, turns=T, rad=a.rad, tgs=a.tgs, info=info, cinfo=cinfo, tour=g),
                      open(os.path.join(HERE, 'tours', f'{a.tag}_n{n}.json'), 'w'))

if __name__ == '__main__':
    main()
