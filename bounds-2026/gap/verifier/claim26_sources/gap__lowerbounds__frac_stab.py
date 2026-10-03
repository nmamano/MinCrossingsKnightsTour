#!/usr/bin/env python3
"""FINDINGS (w-turnstheory) 11.3: fractional endpoint penalties, one orientation at a time.

Width-two strip graph (strip_dp.build(2), crossings). Augmented node = (base state, F mod 3, number of
EXC edges seen (capped at 2), local row parity). As in w-lowerbounds/endpoint_stab.py, a phase-0 node
adds its pending test edges, and every arc adds the test edges introduced at its cell. At row end:
    c = +1 (even parity) or -1 (odd parity);  h = ((1+c)//2 + c*(F+2)) mod 3;
    t = 2 if both EXC edges are selected, else {0:1, 1:2, 2:0}[h];
then the accumulator is reset and the parity is toggled. Arc weight q*(4w-1) - 2*p*t for beta = p/q.
Both initial parities are covered: Bellman-Ford starts from 0 on every node (virtual source).

usage: frac_stab.py ORIENT p q        certify beta=p/q (converged potential) or report no convergence
       frac_stab.py crit ORIENT [b0]  Dinkelbach from b0 (default 4/3): exact critical ratio + cycle
"""
import sys
from fractions import Fraction
import numpy as np
from strip_dp import build

LIST = {((0, -1), (1, 1)): -1, ((0, 0), (1, -2)): -1, ((0, 0), (2, -1)): -1, ((0, 2), (1, 0)): -1,
        ((1, 0), (2, 2)): -1, ((1, 1), (2, -1)): -1, ((0, 1), (1, -1)): +1, ((0, 1), (2, 0)): +1}
EXC = [((0, 0), (2, 1)), ((0, 1), (2, 0))]


def key(a, b):
    return tuple(sorted((a, b)))


def test(orient):
    s = {'up': 1, 'down': -1}[orient]
    coef = {key((a[0], s * a[1]), (b[0], s * b[1])): c for (a, b), c in LIST.items()}
    exc = {key((a[0], s * a[1]), (b[0], s * b[1])) for a, b in EXC}
    return coef, exc


def charge(F, E, par):
    if E >= 2:
        return 2
    c = 1 if par == 0 else -1
    h = ((1 + c) // 2 + c * (F + 2)) % 3
    return {0: 1, 1: 2, 2: 0}[h]


def graph():
    states, adj, W = build(2)
    src, dst, wt = [], [], []
    for u in range(len(states)):
        for v, w in adj[u]:
            src.append(u); dst.append(v); wt.append(w)
    return states, W, np.array(src), np.array(dst), np.array(wt)


def augment(states, W, src, dst, wt, orient):
    coef, exc = test(orient)
    N = len(states)
    phase = np.array([s[0] for s in states])
    c0 = np.zeros(N, dtype=np.int64); e0 = np.zeros(N, dtype=np.int64)
    for u, s in enumerate(states):
        if s[0] != 0:
            continue
        for e in s[1]:
            k = key((e[0], e[1]), (e[2], e[3]))
            c0[u] += coef.get(k, 0); e0[u] += k in exc
    ca = np.zeros(len(src), dtype=np.int64); ea = np.zeros(len(src), dtype=np.int64)
    for i, (u, v) in enumerate(zip(src, dst)):
        x = states[u][0]; shift = 1 if x == W - 1 else 0
        for e in states[v][1]:
            if (e[0], e[1]) == (x, -shift):
                k = key((e[0], e[1] + shift), (e[2], e[3] + shift))
                ca[i] += coef.get(k, 0); ea[i] += k in exc
    A = 18          # code = par*9 + F*3 + E   (phase-0 nodes use F=E=0)
    S, D, Wt, T = [], [], [], []
    for i, (u, v) in enumerate(zip(src, dst)):
        for par in (0, 1):
            codes = [(0, 0)] if phase[u] == 0 else [(F, E) for F in range(3) for E in range(3)]
            for F, E in codes:
                cin = par * 9 + F * 3 + E
                if phase[u] == 0:
                    F, E = c0[u], e0[u]
                F2 = (F + ca[i]) % 3; E2 = min(E + ea[i], 2)
                if phase[v] == 0:
                    S.append(u * A + cin); D.append(v * A + (1 - par) * 9); Wt.append(wt[i])
                    T.append(charge(F2, E2, par))
                else:
                    S.append(u * A + cin); D.append(v * A + par * 9 + F2 * 3 + E2); Wt.append(wt[i]); T.append(0)
    return np.array(S), np.array(D), np.array(Wt), np.array(T), N * A


def weights(Wt, T, beta):
    p, q = beta.numerator, beta.denominator
    return q * (4 * Wt - 1) - 2 * p * T


def neg_cycle(S, D, ww, M, check_every=10, cap=10 ** 6):
    dist = np.zeros(M, dtype=np.int64)
    parent = np.full(M, -1, dtype=np.int64)
    idx = np.arange(len(S))
    for it in range(1, cap + 1):
        cand = dist[S] + ww
        nd = dist.copy(); np.minimum.at(nd, D, cand)
        if np.array_equal(nd, dist):
            return 'ok', dist, it
        mask = (cand == nd[D]) & (nd[D] < dist[D])
        parent[D[mask]] = idx[mask]
        dist = nd
        if it % check_every == 0:
            cyc = find_parent_cycle(parent, S)
            if cyc is not None:
                assert int(ww[cyc].sum()) < 0
                return 'cycle', cyc, it
    raise RuntimeError('cap')


def find_parent_cycle(parent, S):
    M = len(parent)
    state = np.zeros(M, dtype=np.int8)
    for s0 in np.nonzero(parent >= 0)[0]:
        if state[s0]:
            continue
        path = []; v = s0
        while v >= 0 and state[v] == 0:
            state[v] = 1; path.append(v)
            a = parent[v]; v = S[a] if a >= 0 else -1
        if v >= 0 and state[v] == 1:
            k = path.index(v)
            for x in path:
                state[x] = 2
            return [int(parent[x]) for x in path[k:]]
        for x in path:
            state[x] = 2
    return None


def setup(orient):
    states, W, src, dst, wt = graph()
    S, D, Wt, T, M = augment(states, W, src, dst, wt, orient)
    used = np.zeros(M, dtype=bool); used[S] = True; used[D] = True
    print(f'orient={orient}: base states {len(states)}, aug arcs {len(S)}, used aug nodes {used.sum()}', flush=True)
    return states, S, D, Wt, T, M, used


def certify(orient, beta):
    states, S, D, Wt, T, M, used = setup(orient)
    res, data, it = neg_cycle(S, D, weights(Wt, T, beta), M)
    if res == 'ok':
        print(f'{orient} beta={beta}: converged after {it} passes; potential range '
              f'{data[used].min()}..{data[used].max()} (units 1/(4q))', flush=True)
        np.save(f'frac_pot_{orient}_{beta.numerator}_{beta.denominator}.npy', data)
    else:
        num = int((4 * Wt[data] - 1).sum()); den = int(T[data].sum())
        print(f'{orient} beta={beta}: NEGATIVE CYCLE, {len(data)} arcs, sum(4w-1)={num}, sum t={den}, '
              f'ratio sum(w-1/4)/sum(a) = {Fraction(2 * num, 4 * den) if den else "inf"}', flush=True)
        np.save(f'frac_cycle_{orient}.npy', np.array(data))


def critical(orient, beta):
    """Dinkelbach: beta* = min over cycles of sum(w-1/4)/sum(a) = 2*sum(4w-1)/(4*sum t)."""
    states, S, D, Wt, T, M, used = setup(orient)
    while True:
        res, data, it = neg_cycle(S, D, weights(Wt, T, beta), M)
        if res == 'ok':
            print(f'{orient}: beta* = {beta} = {float(beta):.6f}, converged after {it} passes; potential range '
                  f'{data[used].min()}..{data[used].max()} (units 1/(4q))', flush=True)
            np.save(f'frac_pot_{orient}_{beta.numerator}_{beta.denominator}.npy', data)
            return beta
        num = int((4 * Wt[data] - 1).sum()); den = int(T[data].sum())
        beta = Fraction(2 * num, 4 * den)
        print(f'  negative cycle: {len(data)} arcs, sum(4w-1)={num}, sum t={den} -> beta <= {beta} '
              f'= {float(beta):.6f}', flush=True)
        np.save(f'frac_cycle_{orient}.npy', np.array(data))


if __name__ == '__main__':
    if sys.argv[1] == 'crit':
        critical(sys.argv[2], Fraction(sys.argv[3]) if len(sys.argv) > 3 else Fraction(4, 3))
    else:
        certify(sys.argv[1], Fraction(int(sys.argv[2]), int(sys.argv[3])))
