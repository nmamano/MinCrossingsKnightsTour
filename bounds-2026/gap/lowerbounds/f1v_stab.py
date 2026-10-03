#!/usr/bin/env python3
"""F1-V (R4 simplification, gap/lowerbounds FINDINGS section F): width-two strip stability with a STRONG row test.

Same width-two strip graph and up-test accumulator as frac_stab.py (audited Section 5 model: edges incident to
columns 0,1; degree 2 in columns 0,1, <= 2 in columns 2,3; no cycle among strip edges). At each row end (row r)
the indicator is
    g(r) = 1  if the up test fails at r (F != 2 mod 3, or both exception edges present), or
              VIS(r): some crossing pair of strip edges NOT both incident to column 0 (a pair in S* minus B)
              has a two-quarter tile overlap with a quarter in the squares (1..3, r).
VIS(r) is a function of the pending edges at the end of row r (every edge whose tile meets square row r is
pending then). Arc weight q*(4w - 1) - 4*p*g (rate p/q). A converged potential proves
    X_sigma - (rows) >= (p/q) * #(rows with g = 1) - (potential range)/(4q).
usage: f1v_stab.py crit [b0] [up|down]      Dinkelbach for the critical rate (start b0, default 2)
       f1v_stab.py cert p q       certify rate p/q
"""
import sys
from fractions import Fraction
from itertools import combinations
import numpy as np
import frac_stab as FS
from strip_dp import cross
sys.path.insert(0, 'windows')
from w3_quarters import tile, inside, quarters


def tile_quarters(e):
    (x0, y0, x1, y1) = e
    t = tile(((x0, y0), (x1, y1)))
    out = set()
    for x in range(min(x0, x1) - 1, max(x0, x1) + 1):
        for y in range(min(y0, y1) - 1, max(y0, y1) + 1):
            for q, pt in quarters(x, y).items():
                if inside(t, pt): out.add((x, y, q))
    return out


def vis_of_state(edges):
    es = [e[:4] for e in edges]
    tq = {e: tile_quarters(e) for e in es}
    for e, f in combinations(es, 2):
        if not cross(e, f): continue
        if 0 in (e[0], e[2]) and 0 in (f[0], f[2]): continue      # pair in B
        ov = tq[e] & tq[f]
        if len(ov) == 2 and any(x in (1, 2, 3) and y == -1 for x, y, q in ov): return 1
    return 0


def setup(orient='up'):
    states, W, src, dst, wt = FS.graph()
    coef, exc = FS.test(orient)
    N = len(states)
    vis = np.zeros(N, dtype=np.int64)
    for u, s in enumerate(states):
        if s[0] == 0: vis[u] = vis_of_state(s[1])
    # FS.augment charges T = charge(F,E,par) at row ends; rebuild the strong indicator from the target code:
    # target nodes of row-end arcs are phase-0 nodes v*A + (1-par)*9; we need F2, E2 of the finished row, so redo
    phase = np.array([s[0] for s in states])
    c0 = np.zeros(N, dtype=np.int64); e0 = np.zeros(N, dtype=np.int64)
    for u, s in enumerate(states):
        if s[0] != 0: continue
        for e in s[1]:
            k = FS.key((e[0], e[1]), (e[2], e[3])); c0[u] += coef.get(k, 0); e0[u] += k in exc
    ca = np.zeros(len(src), dtype=np.int64); ea = np.zeros(len(src), dtype=np.int64)
    for i, (u, v) in enumerate(zip(src, dst)):
        x = states[u][0]; shift = 1 if x == W - 1 else 0
        for e in states[v][1]:
            if (e[0], e[1]) == (x, -shift):
                k = FS.key((e[0], e[1] + shift), (e[2], e[3] + shift)); ca[i] += coef.get(k, 0); ea[i] += k in exc
    # node code = bit * 18 + par * 9 + F * 3 + E; bit = VIS of the previous finished row (down orientation only)
    A = 36
    bits = (0, 1) if orient == 'down' else (0,)
    S2, D2, W2, G2 = [], [], [], []
    for i, (u, v) in enumerate(zip(src, dst)):
        for bt in bits:
            for par in (0, 1):
                codes = [(0, 0)] if phase[u] == 0 else [(F, E) for F in range(3) for E in range(3)]
                for F, E in codes:
                    cin = bt * 18 + par * 9 + F * 3 + E
                    if phase[u] == 0: F, E = c0[u], e0[u]
                    F2 = (F + ca[i]) % 3; E2 = min(E + ea[i], 2)
                    if phase[v] == 0:
                        vv = vis[v] if orient == 'up' else bt            # up: square row r; down: square row r - 1
                        g = 1 if (F2 != 2 or E2 >= 2 or vv) else 0
                        nb = vis[v] if orient == 'down' else 0
                        S2.append(u * A + cin); D2.append(v * A + nb * 18 + (1 - par) * 9); W2.append(wt[i]); G2.append(g)
                    else:
                        S2.append(u * A + cin); D2.append(v * A + bt * 18 + par * 9 + F2 * 3 + E2); W2.append(wt[i]); G2.append(0)
    S2, D2, W2, G2 = map(np.array, (S2, D2, W2, G2))
    used = np.zeros(N * A, dtype=bool); used[S2] = True; used[D2] = True
    print(f'base states {N} (phase-0 with VIS: {int(vis.sum())}), aug arcs {len(S2)}, used nodes {used.sum()}', flush=True)
    return S2, D2, W2, G2, N * A, used


def run(beta, S, D, Wt, G, M, used):
    p, q = beta.numerator, beta.denominator
    ww = q * (4 * Wt - 1) - 4 * p * G
    return FS.neg_cycle(S, D, ww, M)


def main():
    orient = 'down' if 'down' in sys.argv else 'up'
    sys.argv = [a for a in sys.argv if a not in ('up', 'down')]
    S, D, Wt, G, M, used = setup(orient)
    print('orientation', orient, flush=True)
    if sys.argv[1] == 'cert':
        beta = Fraction(int(sys.argv[2]), int(sys.argv[3]))
        res, data, it = run(beta, S, D, Wt, G, M, used)
        print(f'rate {beta}: {res} after {it} passes' + (f'; potential range {data[used].min()}..{data[used].max()}' if res == 'ok' else ''))
        return
    beta = Fraction(sys.argv[2]) if len(sys.argv) > 2 else Fraction(2)
    while True:
        res, data, it = run(beta, S, D, Wt, G, M, used)
        if res == 'ok':
            print(f'CRITICAL RATE = {beta} = {float(beta):.6f}; potential range {data[used].min()}..{data[used].max()} '
                  f'(units 1/(4q)), {it} passes', flush=True)
            np.save(f'f1v_pot_{orient}_{beta.numerator}_{beta.denominator}.npy', data)
            return
        num = int((4 * Wt[data] - 1).sum()); den = int(G[data].sum())
        beta = Fraction(num, 4 * den)
        print(f'  negative cycle: {len(data)} arcs, sum(4w-1) = {num}, sum g = {den} -> rate <= {beta}', flush=True)
        np.save('f1v_cycle.npy', np.array(data))


if __name__ == '__main__':
    main()
