"""Run-aware stability: largest kappa with  sum(w - 1/4) >= kappa * sum_runs (3k + 3) - C,
where a run is a maximal block of k consecutive bad rows. States (s, flag_this_row, prev_row_bad)."""
import numpy as np
from fractions import Fraction
exec(open('alpha_star.py').read().split("lo, hi = Fraction(0), Fraction(2)")[0])
phase = np.array([states[v][0] for v in range(N)])
S2, D2, Wt2, L2 = [], [], [], []
rowend = (phase[dst] == 0)
for f in (0, 1):
    for pb in (0, 1):
        nf = np.maximum(f, nc)
        # at row end: loss = 3*nf + 3*nf*(1-pb); new state flag 0, prev_bad = nf
        loss = np.where(rowend, 3 * nf + 3 * nf * (1 - pb), 0)
        tf = np.where(rowend, 0, nf)
        tpb = np.where(rowend, nf, pb)
        S2.append(src * 4 + f * 2 + pb); D2.append(dst * 4 + tf * 2 + tpb); Wt2.append(wt); L2.append(loss)
S2 = np.concatenate(S2); D2 = np.concatenate(D2); Wt2 = np.concatenate(Wt2); L2 = np.concatenate(L2)
M = 4 * N
def ok3(kappa, cap):
    p, q = kappa.numerator, kappa.denominator
    ww = q * (4 * Wt2 - 1) - 4 * p * L2
    dist = np.zeros(M, dtype=np.int64)
    for it in range(cap):
        cand = dist[S2] + ww
        nd = dist.copy(); np.minimum.at(nd, D2, cand)
        if np.array_equal(nd, dist): return True, dist
        dist = nd
    return False, None
lo, hi = Fraction(1, 12), Fraction(1)
assert ok3(lo, 10**7)[0]
for _ in range(11):
    mid = (lo + hi) / 2
    if ok3(mid, 4000)[0]: lo = mid
    else: hi = mid
good, dist = ok3(lo, 10**7)
print('kappa* in [', lo, ',', hi, ']', float(lo), float(hi), 'certified lo:', good, 'range', dist.min() if good else None)
