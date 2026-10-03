#!/usr/bin/env python
"""Layout G with pasted periodic templates (KT Structures, 2026-10-02).
- Gentle seam on the anti-diagonal: optimal periodic seam (seam.py kind 'gentle', period (6,6), w=3,
  1.0 crossing per unit x) for a chosen current, mirrored x -> -x for the TL half, and rotated by
  180 degrees for the BR half.
- Diagonal flux templates (diag_tpl_p6_w3.json, paste.paste_field) on the BL (r=0) and TR (r=2) diagonals.
- Free: windows at the 4 corners, the centre, and around remaining defect clusters.
Tries every (seam current, parity) combination per half and keeps those whose free windows balance.
usage: layoutG_paste.py n [--time 120] [--lns 0] [--tg 1]
"""
import argparse, itertools, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, ROOT)
os.chdir(HERE)
import fold3, paste
from fold3 import comps
from layoutG import field_G, edges_to_nb
from repair import clusters, window_cells
from imbal import imbalance
from seam import Seam, build_model
from seam_flux import cur_terms
from ortools.sat.python import cp_model
from kt.board import complete, to_grid, lns
from kt.core import validate, num_crossings, num_turns, crossing_list
from collections import Counter
import networkx as nx

P, W = 6, 3


def seam_template(target):
    st = Seam(T=(P, P), hv=(-1, 1), w1=W, w2=W, f1=(2, -1), form1=(1, 2), f2=(1, -2), form2=(2, 1), s=1)
    m, x = build_model(st, lanes=False)
    terms, const = cur_terms(st, x)
    m.Add(sum(terms) + const == target)
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 120
    r = s.Solve(m)
    assert r in (cp_model.OPTIMAL, cp_model.FEASIBLE), r
    ch = {i for i in range(len(x)) if s.Value(x[i])}
    cells = {}
    for u in st.base:
        ds = [d for (e, d) in st.inc[u] if e in ch] + [d for d, _ in st.fixed_inc[u]]
        assert len(ds) == 2
        cells[u] = ds
    print(f'  seam template current {target}: {s.StatusName(r)} X/period {s.ObjectiveValue()}', flush=True)
    return cells


def canon(c):
    k = c[0] // P
    return (c[0] - P * k, c[1] - P * k)


def place_seam(n, cells, par, lo, hi, delta=0):
    """TL half: board C = (a - x, b + y), a + b = n - 1 (+ parity shift). Returns {board cell: [board moves]}."""
    a = par; b = n - 1 + delta - par
    out = {}
    for X in range(lo, hi):
        for Y in range(n):
            hval = X + Y - (n - 1 + delta)
            if abs(hval) > W: continue
            x, y = a - X, Y - b
            u = canon((x, y))
            if u not in cells: return None
            out[(X, Y)] = [(-d[0], d[1]) for d in cells[u]]
    return out


def build(n, tg, seamTL, seamBR, lo, t=1):
    old = fold3.field
    fold3.field = lambda n_, ts=(t,) * 4, ms=(0, 0, 0, 0): field_G(n_, ts)
    try:
        E, deg = paste.paste_field(n, t, {0: tg, 2: tg}, None, lo=lo, hi=n // 2 - lo)
    finally:
        fold3.field = old
    E = set(E)
    rot = lambda c: (n - 1 - c[0], n - 1 - c[1])
    put = dict(seamTL)
    for c, ds in seamBR.items():
        put[rot(c)] = [(-d[0], -d[1]) for d in ds]
    E = {e for e in E if e[0] not in put and e[1] not in put}
    for c, ds in put.items():
        for d in ds:
            q = (c[0] + d[0], c[1] + d[1])
            E.add(tuple(sorted([c, q])))
    deg = Counter()
    for e in E:
        deg[e[0]] += 1; deg[e[1]] += 1
    return E, deg, set(put)


def free_set(n, E, deg, pasted, lo, rad=4, link=4):
    cs, cyc, bad = comps(n, E, deg)
    bad = list(bad)
    free = set()
    for c in clusters(bad, link=link):
        free |= window_cells(n, c, rad)
    h = n // 2; t = 1
    for x in range(n):                         # end caps of the 4 template bands (corner side and centre side)
        if lo <= x < h - lo: continue
        for y in range(n):
            if abs(y - x - t) <= W + 1 and x < h:                  # BL diagonal
                free.add((x, y)); free.add((n - 1 - x, n - 1 - y))  # and TR diagonal
            if abs(x + y - (n - 1)) <= W + 1 and x < h:            # TL seam half
                free.add((x, y)); free.add((n - 1 - x, n - 1 - y))  # and BR seam half
    return free, len(cs), len(cyc), len(bad)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int); ap.add_argument('--time', type=float, default=120)
    ap.add_argument('--lns', type=int, default=0); ap.add_argument('--tg', type=int, default=1)
    ap.add_argument('--lo', type=int, default=8)
    a = ap.parse_args(); n = a.n; h = n // 2
    tpl = {c: seam_template(c) for c in (-1, 0)}
    cands = []
    for (cTL, pTL, cBR, pBR) in itertools.product((-1, 0), (0, 1), (-1, 0), (0, 1)):
        sTL = place_seam(n, tpl[cTL], pTL, a.lo, h - a.lo)
        sBR = place_seam(n, tpl[cBR], pBR, a.lo, h - a.lo)
        if sTL is None or sBR is None: continue
        E, deg, pasted = build(n, a.tg, sTL, sBR, a.lo)
        free, nc, ncyc, nbad = free_set(n, E, deg, pasted, a.lo)
        G = nx.Graph(); G.add_nodes_from(free)
        MOV = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        for c in free:
            for d in MOV:
                q = (c[0] + d[0], c[1] + d[1])
                if q in free: G.add_edge(c, q)
        imbs = sorted(imbalance(n, E, comp) for comp in nx.connected_components(G))
        print(f'combo TL({cTL},{pTL}) BR({cBR},{pBR}): comps {nc} closed {ncyc} bad {nbad} free {len(free)} '
              f'window imbalances {imbs} X_pre {len(crossing_list(E))}', flush=True)
        if all(v == 0 for v in imbs):
            cands.append((len(free), cTL, pTL, cBR, pBR, E, free))
    cands.sort(key=lambda z: z[0])
    for (_, cTL, pTL, cBR, pBR, E, free) in cands[:2]:
        t0 = time.time()
        full, ci = complete(n, edges_to_nb(n, E), free, time_limit=a.time, workers=2)
        if full is None:
            print('  FAIL', ci, flush=True); continue
        if a.lns:
            full = lns(n, full, free, win=8, step=4, time_limit=20, workers=2, rounds=a.lns)
        g = to_grid(n, full)
        X = num_crossings(g)
        print(f'  n={n} TL({cTL},{pTL}) BR({cBR},{pBR}) valid={validate(g)} X={X} X/n={X / n:.3f} '
              f'17n/3={17 * n / 3:.1f} {ci.get("status")} {time.time() - t0:.0f}s', flush=True)
