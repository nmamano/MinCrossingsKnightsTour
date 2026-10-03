#!/usr/bin/env python3
"""Beyond-5n pilot (KT Lower Bounds, 2026-10-03): joint side certificate with collar ports.

Width-three strip graph: columns 0, 1, 2 = collar (degree exactly 2), columns 3, 4 = ghost interior columns
(degree <= 2, only edges to the collar counted). Edges: knight moves with an end in columns 0..2. Cells in (y, x)
order, x = 0..4. State = pending edges (lower end processed, upper end not), each with a flag (below), plus the
up/down test accumulators F mod 3 and E (exception edges, capped at 2) of the current row, plus (down only) the
VIS bit of the previous row. No connectivity labels (option CONN is not implemented: no forest condition).

Per arc:
  w  = new proper crossings between WIDTH-TWO edges (an end in column 0 or 1)  [S* crossings, as in f1v_stab.py]
  g  = at row end: up/down test fails (F != 2, or both exception edges) or VIS  [f1v_stab.py definitions]
  Q  = (#steep ports) - (#non-steep ports) - 2 (#local P paths completed)
       ports = edges between columns 0..2 and columns 3, 4; steep = |dx| = 2; non-steep = (2,y)-(3,y+-2);
       local P path = the collar path (4,y+1)-(2,y)-(0,y-1)-(1,y+1)-(3,y+2) or its mirror y -> -y.
  Q = NLOC - 2 NS, NLOC = ports not on a local P path >= N_re (Structures' changed ports), NS = non-steep ports.
Arc weight b*(5w - 1) - 5b*g - 5a*Q certifies   X_sigma - rows >= #g + (a/b) (N_re - 2 NS) - C.
env: XW=2|3 (crossings among edges with an end in columns < XW; 2 = S*), QMODE=ns2|all (Q = NLOC - 2NS or NLOC),
     QROW=0|1 (1: count Q only in rows with g = 0)
usage: joint_stab.py up|down crit [c0]     Dinkelbach for c* (default start 1)
       joint_stab.py up|down cert a b       certify c = a/b
       joint_stab.py up|down zero           Q = 0: check the g-rate-1 inequality alone in this model
"""
import sys, time
from collections import deque
from fractions import Fraction
from itertools import combinations
import numpy as np
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE.parent / 'windows'))
import frac_stab as FS
from strip_dp import cross
from f1v_stab import tile_quarters

W = 5
import os
XW = int(os.environ.get('XW', '2'))      # crossings counted among edges with an end in columns < XW (2 = S*, 3 = width three)
QROW = int(os.environ.get('QROW', '0'))     # 1: Q counts only in rows with g = 0 (row accumulator in the state)
QMODE = os.environ.get('QMODE', 'ns2')     # ns2: Q = NLOC - 2 NS;  all: Q = NLOC (>= N_re)
UP = [(2, 1), (-2, 1), (1, 2), (-1, 2)]
TQ = {}


def tq(e):
    if e not in TQ: TQ[e] = tile_quarters(e)
    return TQ[e]


def is_w2(e): return min(e[0], e[2]) <= 1


def is_wx(e): return min(e[0], e[2]) <= XW - 1


def vis(edges):
    es = [e[:4] for e in edges if is_w2(e)]
    for e, f in combinations(es, 2):
        if not cross(e, f): continue
        if 0 in (e[0], e[2]) and 0 in (f[0], f[2]): continue
        ov = tq(e) & tq(f)
        if len(ov) == 2 and any(x in (1, 2, 3) and y == -1 for x, y, q in ov): return 1
    return 0


def build(orient):
    coef, exc = FS.test(orient)
    def tcont(es):
        F = E = 0
        for e in es:
            k = FS.key((e[0], e[1]), (e[2], e[3])); F += coef.get(k, 0); E += k in exc
        return F, E
    start = (0, (), 0, 0, 0, 0)
    index = {start: 0}; states = [start]; q = deque([0])
    S, D, Wt, G, Qv = [], [], [], [], []
    t0 = time.time()
    while q:
        sid = q.popleft()
        x, edges, F, E, vb, qa = states[sid]
        incoming = [e for e in edges if e[2] == x and e[3] == 0]
        rest = [e for e in edges if not (e[2] == x and e[3] == 0)]
        strip = x <= 2
        cands = []
        for dx, dy in UP:
            tx = x + dx
            if 0 <= tx < W and (strip or tx <= 2):
                cands.append((x, 0, tx, dy))
        if strip:
            r = 2 - len(incoming)
            if r < 0: continue
            need = [r]
        else:
            if len(incoming) > 2: continue
            need = range(0, 3 - len(incoming))
        tdeg0 = {}
        for e in rest: tdeg0[(e[2], e[3])] = tdeg0.get((e[2], e[3]), 0) + 1
        inv = sorted((e[0] - x, e[1]) for e in incoming)          # incoming lower ends, relative
        for r in need:
            for chosen in combinations(cands, r):
                tdeg = dict(tdeg0); ok = True
                for e in chosen:
                    k = (e[2], e[3]); tdeg[k] = tdeg.get(k, 0) + 1
                    if tdeg[k] > 2: ok = False
                if not ok: continue
                w = 0
                for i, f in enumerate(chosen):
                    if not is_wx(f): continue
                    for e in rest:
                        if is_wx(e) and cross(e[:4], f): w += 1
                    for g2 in chosen[:i]:
                        if is_wx(g2) and cross(g2, f): w += 1
                # ports
                Q = 0
                for f in chosen:
                    a, b = f[0], f[2]
                    if (a <= 2) != (b <= 2):
                        Q += 1 if (abs(b - a) == 2 or QMODE == 'all') else -1
                outv = sorted((f[2] - x, f[3]) for f in chosen)
                flags = {}
                new_rest = list(rest)
                # '/' pattern
                if x == 0 and not incoming and outv == [(1, 2), (2, 1)]:
                    flags[(0, 0, 1, 2)] = 1
                if x == 2 and inv == [(-2, -1)] and outv == [(2, 1)]:
                    for j, e in enumerate(new_rest):
                        if e[:4] == (0, -1, 1, 1) and e[4] == 1: new_rest[j] = e[:4] + (2,)
                if x == 1 and len(incoming) == 1 and incoming[0] == (0, -2, 1, 0, 2) and outv == [(2, 1)]:
                    Q -= 2
                # '\' pattern
                if x == 1 and inv == [(2, -1)] and outv == [(-1, 2)]:
                    flags[(1, 0, 0, 2)] = 3
                if x == 2 and inv == [(2, -1)] and outv == [(-2, 1)]:
                    flags[(2, 0, 0, 1)] = 4
                if x == 0 and r == 0 and sorted(e[4] for e in incoming) == [3, 4] \
                        and sorted(e[:4] for e in incoming) == [(1, -2, 0, 0), (2, -1, 0, 0)]:
                    Q -= 2
                new_edges = new_rest + [f + (flags.get(f, 0),) for f in chosen]
                dF, dE = tcont(chosen)
                F2 = (F + dF) % 3; E2 = min(E + dE, 2)
                nx = x + 1; g = 0
                if nx == W:
                    nx = 0
                    ne = tuple(sorted((a, b - 1, c, d - 1, fl) for a, b, c, d, fl in new_edges))
                    v = vis(ne)
                    vv = v if orient == 'up' else vb
                    g = 1 if (F2 != 2 or E2 >= 2 or vv) else 0
                    F3, E3 = tcont(ne); ns = (0, ne, F3 % 3, min(E3, 2), v if orient == 'down' else 0, 0)
                    if QROW: Q = (qa + Q) * (1 - g)
                else:
                    ns = (nx, tuple(sorted(new_edges)), F2, E2, vb, qa + Q if QROW else 0)
                    if QROW: Q = 0
                if ns not in index:
                    index[ns] = len(states); states.append(ns); q.append(index[ns])
                    if len(states) % 200000 == 0:
                        print(f'  states {len(states)}, queue {len(q)}, {time.time() - t0:.0f}s', flush=True)
                S.append(sid); D.append(index[ns]); Wt.append(w); G.append(g); Qv.append(Q)
    print(f'{orient}: states {len(states)}, arcs {len(S)}, build {time.time() - t0:.0f}s', flush=True)
    return states, np.array(S), np.array(D), np.array(Wt), np.array(G), np.array(Qv)


def weights(Wt, G, Qv, c):
    a, b = c.numerator, c.denominator
    return b * (W * Wt - 1) - W * b * G - W * a * Qv


def main():
    orient = sys.argv[1]; mode = sys.argv[2]
    states, S, D, Wt, G, Qv = build(orient)
    M = len(states)
    used = np.zeros(M, dtype=bool); used[S] = True; used[D] = True
    if mode == 'zero':
        res, data, it = FS.neg_cycle(S, D, W * Wt - 1 - W * G, M)
        print('g rate 1 (Q ignored):', res, it, (f'range {data[used].min()}..{data[used].max()} (units 1/5)' if res == 'ok'
              else f'cycle {len(data)} arcs, sum(5w-1-5g) = {int((W * Wt - 1 - W * G)[data].sum())}'))
        if res != 'ok': np.save(f'joint_cycle_{orient}_zero.npy', np.array(data))
        return
    if mode == 'cert':
        c = Fraction(int(sys.argv[3]), int(sys.argv[4]))
        res, data, it = FS.neg_cycle(S, D, weights(Wt, G, Qv, c), M)
        print(f'c = {c}: {res} after {it} passes' + (f'; potential range {data[used].min()}..{data[used].max()} (units 1/(5b))' if res == 'ok' else ''))
        return
    c = Fraction(sys.argv[3]) if len(sys.argv) > 3 else Fraction(1)
    while True:
        res, data, it = FS.neg_cycle(S, D, weights(Wt, G, Qv, c), M)
        if res == 'ok':
            print(f'{orient}: CRITICAL c* = {c} = {float(c):.6f}; potential range {data[used].min()}..{data[used].max()} '
                  f'(units 1/(5b)), {it} passes', flush=True)
            np.save(f'joint_pot_{orient}_XW{XW}_{QMODE}_R{QROW}_{c.numerator}_{c.denominator}.npy', data)
            return
        num = int((W * Wt[data] - 1 - W * G[data]).sum()); den = int(Qv[data].sum())
        print(f'  negative cycle: {len(data)} arcs ({len(data) / W:.0f} rows), sum(5w-1-5g) = {num}, sum Q = {den}', flush=True)
        np.save(f'joint_cycle_{orient}_XW{XW}_{QMODE}_R{QROW}.npy', np.array(data))
        if den <= 0:
            print('  cycle with Q <= 0: the g-rate-1 inequality fails in this model (no forest condition?)'); return
        c = Fraction(num, W * den)
        print(f'  -> c <= {c} = {float(c):.6f}', flush=True)


if __name__ == '__main__':
    main()
