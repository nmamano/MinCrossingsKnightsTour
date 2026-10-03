"""Chord model of a gentle-seam corner nest (KT Structures, 2026-10-03).

Lines c (left-edge index, A' family c = x - 2y). Left pairing lam (periodic, period PER lines), seam map
f(c) = c + s[c % 3], top pairing tau = P on top indices (k <-> k-3 for k even). Lines outside [0, N) are 'outside'.
A line is trapped if its cycle under (lam, f, tau) never leaves [0, N).
"""
import itertools, sys

def P(c):
    return c - 3 if c % 2 == 0 else c + 3

def trapped_count(lam, s, N=600, margin=60):
    f = lambda c: c + s[c % 3]
    finv = {}
    for c in range(-200, N + 200):
        finv[f(c)] = c
    seen = set(); trapped = 0
    for c0 in range(margin, N - margin):
        if c0 in seen: continue
        cyc = []; c = c0; ok = True
        for _ in range(4 * N):
            cyc.append(c)
            k = f(c); k2 = P(k); c2 = finv[k2]; c3 = lam(c2)
            cyc.append(c2)
            if not (0 <= c3 < N) or not (0 <= c2 < N):
                ok = False; break
            c = c3
            if c == c0: break
        for v in cyc: seen.add(v)
        if ok: trapped += len(set(cyc))
    return trapped

def periodic(deltas):
    per = len(deltas)
    return lambda c: c + deltas[c % per]

if __name__ == '__main__':
    for s in [(0, 1, -1), (2, 1, -1), (0, 1, 5), (3, 1, -1)]:
        print('seam s =', s, ' P: trapped', trapped_count(P, s), '  full flip:', trapped_count(periodic([5, -5]), s))
