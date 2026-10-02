"""Per-row stability: largest beta with  sum(w - 1/4) >= beta * (#bad rows) - C  for every walk,
where a row is bad if one of its 4 arcs is not a tight-cycle arc. Augmented states (s, flag)."""
import numpy as np
from fractions import Fraction
exec(open('alpha_star.py').read().split("lo, hi = Fraction(0), Fraction(2)")[0])
phase = np.array([states[v][0] for v in range(N)])
# augmented arcs
S2, D2, Wt2, B2 = [], [], [], []
for f in (0, 1):
    nf = np.maximum(f, nc)
    rowend = (phase[dst] == 0)
    tgt_flag = np.where(rowend, 0, nf)
    S2.append(src * 2 + f); D2.append(dst * 2 + tgt_flag); Wt2.append(wt); B2.append(np.where(rowend, nf, 0))
S2 = np.concatenate(S2); D2 = np.concatenate(D2); Wt2 = np.concatenate(Wt2); B2 = np.concatenate(B2)
M = 2 * N
CAP = 4000
def ok2(beta):
    p, q = beta.numerator, beta.denominator
    ww = q * (4 * Wt2 - 1) - 4 * p * B2
    dist = np.zeros(M, dtype=np.int64)
    for it in range(CAP):
        cand = dist[S2] + ww
        nd = dist.copy(); np.minimum.at(nd, D2, cand)
        if np.array_equal(nd, dist): return True, dist
        dist = nd
    return False, None
lo, hi = Fraction(1, 5), Fraction(4)
assert ok2(lo)[0]
for _ in range(12):
    mid = (lo + hi) / 2
    if ok2(mid)[0]: lo = mid
    else: hi = mid
print("note: search uses an iteration cap; final lo is certified by convergence")
print('beta* in [', lo, ',', hi, ']', float(lo), float(hi))
