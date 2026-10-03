#!/usr/bin/env python3
"""Turns Theory request R1 (gap/turnstheory/REQUESTS.md): fractional endpoint charge with boundary credit.

Same augmented graph as frac_stab.py (base state, F mod 3, EXC count, parity). For each arc we recompute
w (all new crossings) and w0 (new crossings whose two edges both have an endpoint in column 0) from the
pair of states, and assert that w equals the weight stored by strip_dp. Integer weight for beta = p/q:
    q*(4w-1) + p*(4w0-1) - 2p*t,      t = 2a charged at row end.

usage: r1_stab.py ORIENT p q | r1_stab.py crit ORIENT [b0]
"""
import sys
from fractions import Fraction
import numpy as np
import frac_stab as FS
from strip_dp import cross


def arc_w0(states, W, src, dst, wt):
    w0 = np.zeros(len(src), dtype=np.int64)
    for i, (u, v) in enumerate(zip(src, dst)):
        x = states[u][0]; shift = 1 if x == W - 1 else 0
        rest = [e[:4] for e in states[u][1] if not (e[2] == x and e[3] == 0)]
        chosen = [(e[0], e[1] + shift, e[2], e[3] + shift) for e in states[v][1] if (e[0], e[1]) == (x, -shift)]
        w = c0 = 0
        for j, f in enumerate(chosen):
            for e in rest + chosen[:j]:
                if cross(e, f):
                    w += 1
                    if 0 in (e[0], e[2]) and 0 in (f[0], f[2]):
                        c0 += 1
        assert w == wt[i], (i, w, wt[i])
        w0[i] = c0
    return w0


def setup(orient):
    states, W, src, dst, wt = FS.graph()
    w0 = arc_w0(states, W, src, dst, wt)
    S, D, Wt, T, M = FS.augment(states, W, src, dst, wt, orient)
    # augment() emits, for each base arc i in order, a fixed number of copies; rebuild the map arc -> base arc
    reps = []
    phase = np.array([s[0] for s in states])
    for i, u in enumerate(src):
        reps.append(2 * (1 if phase[u] == 0 else 9))
    base = np.repeat(np.arange(len(src)), reps)
    assert len(base) == len(S) and np.array_equal(Wt, wt[base])
    W0 = w0[base]
    used = np.zeros(M, dtype=bool); used[S] = True; used[D] = True
    print(f'orient={orient}: aug arcs {len(S)}, used aug nodes {used.sum()}', flush=True)
    return S, D, Wt, W0, T, M, used


def weights(Wt, W0, T, beta):
    p, q = beta.numerator, beta.denominator
    return q * (4 * Wt - 1) + p * (4 * W0 - 1) - 2 * p * T


def critical(orient, beta):
    """Dinkelbach on beta: cycle ratio = sum(4w-1) / (2 sum t - sum(4w0-1))."""
    S, D, Wt, W0, T, M, used = setup(orient)
    while True:
        res, data, it = FS.neg_cycle(S, D, weights(Wt, W0, T, beta), M)
        if res == 'ok':
            print(f'{orient}: beta* = {beta} = {float(beta):.6f}, converged after {it} passes; potential range '
                  f'{data[used].min()}..{data[used].max()} (units 1/(4q))', flush=True)
            return beta
        a = int((4 * Wt[data] - 1).sum()); b = int((4 * W0[data] - 1).sum()); t = int(T[data].sum())
        rows = len(data) // 4
        beta = Fraction(a, 2 * t - b)
        print(f'  negative cycle: {rows} rows, sum(4w-1)={a}, sum(4w0-1)={b}, sum t={t} -> beta <= {beta} '
              f'= {float(beta):.6f}', flush=True)
        np.save(f'r1_cycle_{orient}.npy', np.array(data))


if __name__ == '__main__':
    if sys.argv[1] == 'crit':
        critical(sys.argv[2], Fraction(sys.argv[3]) if len(sys.argv) > 3 else Fraction(4, 3))
    else:
        S, D, Wt, W0, T, M, used = setup(sys.argv[1])
        beta = Fraction(int(sys.argv[2]), int(sys.argv[3]))
        res, data, it = FS.neg_cycle(S, D, weights(Wt, W0, T, beta), M)
        print(sys.argv[1], beta, res, it, (data[used].min(), data[used].max()) if res == 'ok' else len(data))
