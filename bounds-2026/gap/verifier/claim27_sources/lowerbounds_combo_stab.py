#!/usr/bin/env python3
"""Combined credit certificate (gap/turnstheory/FINDINGS.md "Route past 52/11", (N1)/(N2)).

Row-level transfer graph on the width-two forest strip (strip_dp.build(2)). A row arc is a path of 4 cell arcs
from a phase-0 state; it carries W = sum(4w-1), W0 = sum(4w0-1) (w0 = crossings whose two edges both touch
column 0), the endpoint residue data (F mod 3, EXC count) of frac_stab.py, and the strip degrees of the ghost
cells (2,r) and (3,r) (incoming + newly selected edges).

Blocked row y (Turns Theory (1)): d3(y) = 0 and d2(y-2) = d2(y+2) = 2. History after row r, 4 bits:
cand(r-1), cand(r), b2(r-1), b2(r), with b2 = [d2 == 2], cand(y) = [d3(y) == 0 and d2(y-2) == 2].
Processing row r+1 emits blocked(r-1) = cand(r-1) and b2(r+1). Run counter c in 0..4: on a blocked row
k = [c == 4], c = min(c+1, 4); otherwise k = 0, c = 0. Charges K = sum max(0, l-4) per run.
Node = (phase-0 state, parity, history, c). Arc weight for beta = p/q:
    q*W + p*W0 + 4q*k - 2p*t,     t = 2a (frac_stab.charge) for the row just completed.
Bellman-Ford from 0 at every node (all initial parities, histories and counters).

usage: combo_stab.py ORIENT p q  |  combo_stab.py crit ORIENT [b0]
"""
import sys, time
from fractions import Fraction
import numpy as np
import os
import frac_stab as FS
CAP = int(os.environ.get('CAP', '4'))   # run constant: K = sum max(0, l - CAP)
NC = CAP + 1
NS = 32 * NC
from r1_stab import arc_w0


def row_arcs(orient):
    states, W, src, dst, wt = FS.graph()
    w0 = arc_w0(states, W, src, dst, wt)
    coef, exc = FS.test(orient)
    N = len(states)
    phase = np.array([s[0] for s in states])
    c0 = np.zeros(N, dtype=np.int64); e0 = np.zeros(N, dtype=np.int64)
    for u, s in enumerate(states):
        if s[0] == 0:
            for e in s[1]:
                k = FS.key((e[0], e[1]), (e[2], e[3])); c0[u] += coef.get(k, 0); e0[u] += k in exc
    ca = np.zeros(len(src), dtype=np.int64); ea = np.zeros(len(src), dtype=np.int64)
    gd = np.zeros(len(src), dtype=np.int64)
    for i, (u, v) in enumerate(zip(src, dst)):
        x = states[u][0]; shift = 1 if x == W - 1 else 0
        new = [e for e in states[v][1] if (e[0], e[1]) == (x, -shift)]
        for e in new:
            k = FS.key((e[0], e[1] + shift), (e[2], e[3] + shift)); ca[i] += coef.get(k, 0); ea[i] += k in exc
        inc = sum(1 for e in states[u][1] if (e[2], e[3]) == (x, 0))
        gd[i] = inc + len(new)
    out = {}
    for i, u in enumerate(src):
        out.setdefault(int(u), []).append(i)
    R = []
    for u0 in np.nonzero(phase == 0)[0]:
        u0 = int(u0)
        stack = [(u0, 0, 0, 0, int(c0[u0]), int(e0[u0]), -1, -1)]
        while stack:
            u, d, Wa, W0a, F, E, d2, d3 = stack.pop()
            if d == 4:
                R.append((u0, u, Wa, W0a, F % 3, min(E, 2), d2, d3)); continue
            for i in out.get(u, []):
                assert phase[u] == d
                nd2 = gd[i] if d == 2 else d2; nd3 = gd[i] if d == 3 else d3
                stack.append((int(dst[i]), d + 1, Wa + 4 * int(wt[i]) - 1, W0a + 4 * int(w0[i]) - 1,
                              F + int(ca[i]), E + int(ea[i]), int(nd2), int(nd3)))
    return np.array(R, dtype=np.int64), N


def augment(R, N):
    u0, v0, Wr, W0r, F, E, d2, d3 = R.T
    nR = len(R)
    par = np.arange(2); h = np.arange(16); c = np.arange(NC)
    P, H, C = np.meshgrid(par, h, c, indexing='ij')
    P = P.ravel(); H = H.ravel(); C = C.ravel()              # NS combos
    cand1 = (H >> 3) & 1; cand2 = (H >> 2) & 1; b2a = (H >> 1) & 1; b2b = H & 1
    b2new = (d2 == 2).astype(np.int64); z3new = (d3 == 0).astype(np.int64)
    # t per (row arc, parity)
    tt = np.zeros((nR, 2), dtype=np.int64)
    for p_ in (0, 1):
        tt[:, p_] = [FS.charge(f, e, p_) for f, e in zip(F, E)]
    blocked = cand1[None, :] & b2new[:, None]
    newcand = z3new[:, None] & b2a[None, :]
    H2 = (cand2[None, :] << 3) | (newcand << 2) | (b2b[None, :] << 1) | b2new[:, None]
    k = blocked & (C[None, :] == CAP)
    C2 = np.where(blocked == 1, np.minimum(C[None, :] + 1, CAP), 0)
    P2 = 1 - P[None, :]
    S = (u0[:, None] * NS + P[None, :] * 16 * NC + H[None, :] * NC + C[None, :]).ravel().astype(np.int32)
    D = (v0[:, None] * NS + P2 * 16 * NC + H2 * NC + C2).ravel().astype(np.int32)
    T = tt[np.arange(nR)[:, None], P[None, :]].ravel().astype(np.int8)
    Wa = np.repeat(Wr, NS).astype(np.int16); W0a = np.repeat(W0r, NS).astype(np.int16)
    K = k.ravel().astype(np.int8)
    return S, D, Wa, W0a, K, T, N * NS


class BF:
    def __init__(self, S, D, M):
        o = np.argsort(D, kind='stable')
        self.o = o; self.S = S[o]; self.D = D[o]; self.M = M
        self.starts = np.r_[0, np.nonzero(np.diff(self.D))[0] + 1]
        self.heads = self.D[self.starts]

    def run(self, w, cap=100000, check_every=25):
        w = w[self.o]
        dist = np.zeros(self.M, dtype=np.int64)
        parent = np.full(self.M, -1, dtype=np.int64)
        for it in range(1, cap + 1):
            cand = dist[self.S] + w
            mins = np.minimum.reduceat(cand, self.starts)
            better = mins < dist[self.heads]
            if not better.any():
                return 'ok', dist, it
            hb = self.heads[better]
            dist[hb] = mins[better]
            imp = np.zeros(self.M, dtype=bool); imp[hb] = True
            mask = imp[self.D] & (cand == dist[self.D])
            parent[self.D[mask]] = np.nonzero(mask)[0]
            if it % check_every == 0:
                cyc = find_cycle(parent, self.S)
                if cyc is not None:
                    tot = int(w[cyc].sum())
                    if tot < 0:
                        return 'cycle', self.o[cyc], it
        raise RuntimeError('cap')


def find_cycle(parent, S):
    """Follow parent arcs (vectorised pointer doubling is overkill; simple walk with colouring)."""
    M = len(parent)
    pred = np.where(parent >= 0, S[np.maximum(parent, 0)], -1)
    state = np.zeros(M, dtype=np.int8)
    for s0 in np.nonzero(pred >= 0)[0]:
        if state[s0]: continue
        path = []; v = int(s0)
        while v >= 0 and state[v] == 0:
            state[v] = 1; path.append(v); v = int(pred[v])
        if v >= 0 and state[v] == 1:
            k = path.index(v)
            for x in path: state[x] = 2
            return np.array([parent[x] for x in path[k:]])
        for x in path: state[x] = 2
    return None


def setup(orient):
    t0 = time.time()
    R, N = row_arcs(orient)
    S, D, Wa, W0a, K, T, M = augment(R, N)
    print(f'CAP={CAP} orient={orient}: row arcs {len(R)}, aug arcs {len(S)}, node slots {M}, '
          f'blocked-k arcs {int(K.sum())}, built in {time.time() - t0:.0f}s', flush=True)
    return S, D, Wa, W0a, K, T, M


def weights(Wa, W0a, K, T, beta):
    p, q = beta.numerator, beta.denominator
    return q * Wa.astype(np.int64) + p * W0a.astype(np.int64) + 4 * q * K.astype(np.int64) - 2 * p * T.astype(np.int64)


def critical(orient, beta):
    S, D, Wa, W0a, K, T, M = setup(orient)
    bf = BF(S, D, M)
    used = np.zeros(M, dtype=bool); used[S] = True; used[D] = True
    while True:
        res, data, it = bf.run(weights(Wa, W0a, K, T, beta))
        if res == 'ok':
            print(f'{orient}: beta = {beta} = {float(beta):.6f} converged after {it} passes; potential range '
                  f'{data[used].min()}..{data[used].max()} (units 1/(4q))', flush=True)
            np.save(f'combo_pot_{orient}_{beta.numerator}_{beta.denominator}_cap{CAP}.npy', data)
            return beta
        cyc = data
        a = int(Wa[cyc].astype(np.int64).sum()) + 4 * int(K[cyc].astype(np.int64).sum()); b = int(W0a[cyc].astype(np.int64).sum()); t = int(T[cyc].astype(np.int64).sum())
        print(f'  negative cycle: {len(cyc)} rows, sum(4w-1)={a - 4 * int(K[cyc].astype(np.int64).sum())}, sum k={int(K[cyc].astype(np.int64).sum())}, '
              f'sum(4w0-1)={b}, sum t={t}', flush=True)
        np.save(f'combo_cycle_{orient}.npy' if CAP == 4 else f'combo_cycle_{orient}_cap{CAP}.npy', cyc)
        assert 2 * t - b > 0
        beta = Fraction(a, 2 * t - b)
        print(f'    -> beta <= {beta} = {float(beta):.6f}', flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'crit':
        critical(sys.argv[2], Fraction(sys.argv[3]) if len(sys.argv) > 3 else Fraction(8, 3))
    else:
        S, D, Wa, W0a, K, T, M = setup(sys.argv[1])
        bf = BF(S, D, M)
        beta = Fraction(int(sys.argv[2]), int(sys.argv[3]))
        res, data, it = bf.run(weights(Wa, W0a, K, T, beta))
        print(sys.argv[1], beta, res, it)
