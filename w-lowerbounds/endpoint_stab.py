#!/usr/bin/env python3
"""Turns Theory QUESTIONS.md 'New finite task after the one-row corner lemma' (FINDINGS 10.4).

Width-two strip graph (strip_dp.build(2), crossings). At scan row R, F = sum of the coefficients of the
selected edges in LIST (coordinates relative to row R). The row passes iff F == 2 (mod 3) and the two
EXC edges are not both selected. b = 1 for a failed row. Find the largest beta with no negative cycle for
the integer weights q*(4w-1) - 4*p*b (beta = p/q).

Augmented node = (base state, F mod 3, number of EXC edges seen, capped at 2), only at phases 1..3;
phase-0 nodes carry (0,0). Leaving a phase-0 node adds the pending edges of that state (all edges that
straddle row R with lower end below R); every arc adds the edges introduced at its cell (lower end on
row R). The arc that ends the row charges b and resets.

usage: endpoint_stab.py ORIENT [beta_num beta_den]   ORIENT = up | down | both
  without beta: search beta (capped iterations only steer the search) and then certify the final
  lower value by a converged run.
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


def tests(orient):
    """Return list of (coef dict, exc set) in canonical edge keys."""
    out = []
    for sgn in ((1,) if orient == 'up' else (-1,) if orient == 'down' else (1, -1)):
        coef = {key((a[0], sgn * a[1]), (b[0], sgn * b[1])): c for (a, b), c in LIST.items()}
        exc = {key((a[0], sgn * a[1]), (b[0], sgn * b[1])) for a, b in EXC}
        out.append((coef, exc))
    return out


def graph():
    states, adj, W = build(2)
    N = len(states)
    src, dst, wt = [], [], []
    for u in range(N):
        for v, w in adj[u]:
            src.append(u); dst.append(v); wt.append(w)
    return states, W, np.array(src), np.array(dst), np.array(wt)


def edge_keys(edges):
    return [key((e[0], e[1]), (e[2], e[3])) for e in edges]


def augment(states, W, src, dst, wt, orient):
    T = tests(orient)
    nt = len(T)
    N = len(states)
    phase = np.array([s[0] for s in states])
    # pending contribution at phase-0 states, per test
    c0 = np.zeros((nt, N), dtype=np.int64); e0 = np.zeros((nt, N), dtype=np.int64)
    for u, s in enumerate(states):
        if s[0] != 0: continue
        for k in edge_keys(s[1]):
            for t, (coef, exc) in enumerate(T):
                c0[t, u] += coef.get(k, 0); e0[t, u] += k in exc
    # introduced edges per arc: edges of the target whose lower end is the current cell
    ca = np.zeros((nt, len(src)), dtype=np.int64); ea = np.zeros((nt, len(src)), dtype=np.int64)
    for i, (u, v) in enumerate(zip(src, dst)):
        x = states[u][0]; shift = 1 if x == W - 1 else 0
        for e in states[v][1]:
            if (e[0], e[1]) == (x, -shift):
                k = key((e[0], e[1] + shift), (e[2], e[3] + shift))
                for t, (coef, exc) in enumerate(T):
                    ca[t, i] += coef.get(k, 0); ea[t, i] += k in exc
    # augmented node id: base * A + code, code over (F mod 3, exc count 0..2) per test
    A = 9 ** nt
    def code(F, E):
        c = 0
        for t in range(nt):
            c = c * 9 + (F[t] % 3) * 3 + min(E[t], 2)
        return c
    def decode(c):
        F, E = [0] * nt, [0] * nt
        for t in reversed(range(nt)):
            r = c % 9; c //= 9; F[t], E[t] = r // 3, r % 3
        return F, E
    S, D, Wt, B = [], [], [], []
    for i, (u, v) in enumerate(zip(src, dst)):
        codes = [0] if phase[u] == 0 else range(A)
        for c in codes:
            F, E = decode(c)
            if phase[u] == 0:
                F = [c0[t, u] for t in range(nt)]; E = [e0[t, u] for t in range(nt)]
            F = [F[t] + ca[t, i] for t in range(nt)]; E = [E[t] + ea[t, i] for t in range(nt)]
            if phase[v] == 0:
                fail = any(F[t] % 3 != 2 or E[t] >= 2 for t in range(nt))
                S.append(u * A + c); D.append(v * A); Wt.append(wt[i]); B.append(int(fail))
            else:
                S.append(u * A + c); D.append(v * A + code(F, E)); Wt.append(wt[i]); B.append(0)
    S = np.array(S); D = np.array(D); Wt = np.array(Wt); B = np.array(B)
    # keep only nodes reachable from phase-0 nodes (others are unused codes)
    return S, D, Wt, B, N * A


def bellman(S, D, Wt, B, M, beta, cap):
    p, q = beta.numerator, beta.denominator
    ww = q * (4 * Wt - 1) - 4 * p * B
    dist = np.zeros(M, dtype=np.int64)
    for it in range(cap):
        cand = dist[S] + ww
        nd = dist.copy(); np.minimum.at(nd, D, cand)
        if np.array_equal(nd, dist):
            return True, dist, it
        dist = nd
    return False, dist, cap


def main():
    orient = sys.argv[1]
    states, W, src, dst, wt = graph()
    S, D, Wt, B, M = augment(states, W, src, dst, wt, orient)
    used = np.zeros(M, dtype=bool); used[S] = True; used[D] = True
    print(f'orient={orient}: base states {len(states)}, aug arcs {len(S)}, used aug nodes {used.sum()}', flush=True)
    if len(sys.argv) > 2:
        beta = Fraction(int(sys.argv[2]), int(sys.argv[3]))
        ok, dist, it = bellman(S, D, Wt, B, M, beta, 10 ** 7)
        print('beta', beta, 'converged' if ok else 'NOT converged', 'after', it, 'passes;',
              'potential range', dist[used].min(), dist[used].max(), '(units 1/(4q))')
        if ok:
            np.save(f'endpoint_pot_{orient}_{beta.numerator}_{beta.denominator}.npy', dist)
        return
    lo, hi = Fraction(0), Fraction(4)
    assert bellman(S, D, Wt, B, M, lo, 10 ** 7)[0]
    for _ in range(14):
        mid = (lo + hi) / 2
        ok = bellman(S, D, Wt, B, M, mid, 6000)[0]
        if ok: lo = mid
        else: hi = mid
        print('  beta', mid, float(mid), 'converged' if ok else 'no convergence in cap', flush=True)
    ok, dist, it = bellman(S, D, Wt, B, M, lo, 10 ** 7)
    print('search: beta* in [', lo, ',', hi, ']', float(lo), float(hi), '; lower end certified:', ok,
          'passes', it, 'potential range', dist[used].min(), dist[used].max())



def neg_cycle(S, D, Wt, B, M, beta, check_every=10, cap=10 ** 6):
    """Bellman-Ford with parent pointers. Returns ('ok', dist) if it converges, or ('cycle', arcs) with an
    explicit negative cycle found in the parent graph."""
    p, q = beta.numerator, beta.denominator
    ww = q * (4 * Wt - 1) - 4 * p * B
    dist = np.zeros(M, dtype=np.int64)
    parent = np.full(M, -1, dtype=np.int64)
    idx = np.arange(len(S))
    for it in range(1, cap + 1):
        cand = dist[S] + ww
        nd = dist.copy(); np.minimum.at(nd, D, cand)
        if np.array_equal(nd, dist):
            return 'ok', dist
        mask = (cand == nd[D]) & (nd[D] < dist[D])
        parent[D[mask]] = idx[mask]
        dist = nd
        if it % check_every == 0:
            cyc = find_parent_cycle(parent, S)
            if cyc is not None:
                tot = int(ww[cyc].sum())
                assert tot < 0, tot
                return 'cycle', cyc
    raise RuntimeError('cap')


def find_parent_cycle(parent, S):
    M = len(parent)
    state = np.zeros(M, dtype=np.int8)   # 0 new, 1 on stack, 2 done
    for s0 in np.nonzero(parent >= 0)[0]:
        if state[s0]: continue
        path = []; v = s0
        while v >= 0 and state[v] == 0:
            state[v] = 1; path.append(v)
            a = parent[v]; v = S[a] if a >= 0 else -1
        if v >= 0 and state[v] == 1:
            k = path.index(v)
            cyc_nodes = path[k:]
            for x in path: state[x] = 2
            return [int(parent[x]) for x in cyc_nodes]
        for x in path: state[x] = 2
    return None


def critical(orient, start=Fraction(1)):
    """Dinkelbach iteration: exact beta* = min over cycles of sum(4w-1) / (4 sum b)."""
    states, W, src, dst, wt = graph()
    S, D, Wt, B, M = augment(states, W, src, dst, wt, orient)
    used = np.zeros(M, dtype=bool); used[S] = True; used[D] = True
    beta = start
    while True:
        res, data = neg_cycle(S, D, Wt, B, M, beta)
        if res == 'ok':
            print(f'{orient}: beta = {beta} = {float(beta):.6f} converged; potential range '
                  f'{data[used].min()}..{data[used].max()} (units 1/(4q))', flush=True)
            np.save(f'endpoint_pot_{orient}_{beta.numerator}_{beta.denominator}.npy', data)
            return beta
        cyc = data
        num = int((4 * Wt[cyc] - 1).sum()); den = 4 * int(B[cyc].sum())
        beta = Fraction(num, den)
        print(f'  negative cycle: length {len(cyc)} arcs, sum(4w-1) = {num}, failed rows = {den // 4}'
              f' -> beta <= {beta} = {float(beta):.6f}', flush=True)
        np.save(f'endpoint_cycle_{orient}.npy', np.array(cyc))


if __name__ == '__main__':
    if sys.argv[1] == 'crit':
        critical(sys.argv[2], Fraction(sys.argv[3]) if len(sys.argv) > 3 else Fraction(1))
    else:
        main()
