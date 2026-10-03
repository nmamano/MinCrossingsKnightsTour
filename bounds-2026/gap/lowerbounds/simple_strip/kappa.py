"""Local excess kappa(r) per square row from the exact identity
   2X_S - 2n = sum_r kappa(r),  kappa = H0 + sum_col1 |m-1|/2 + W3_01 + Cred_{>=2} + X1 + c/2-per-row.
Computed from the pending set at the end of row r (square row -1 in shifted coordinates)."""
import sys, numpy as np
from collections import Counter
from itertools import combinations
from fractions import Fraction
sys.path.insert(0, 'gap/verifier'); sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from claim37_check import tile
from claim26_certificate import edge, cross
from nocyc_common import *
def qs(e): return {(x, y, q) for (x, y), h in tile(e) for q in h}
QS = {}
def tq(e):
    if e not in QS: QS[e] = qs(e)
    return QS[e]
def kappa2(pend, row=-1):
    """2*kappa as integer, plus breakdown."""
    ess = [edge(a, b) for a, b in pend]
    mult = Counter()
    for e in ess: mult.update(q for q in tq(e) if q[1] == row)
    H0 = sum(1 for q in range(4) if mult[(0, row, q)] == 0) if False else None
    quarters01 = [(x, row, q) for x in (0, 1) for q in 'BRTL']
    # quarter labels from tile(): discover them
    return mult
# discover quarter label set
labs = set()
for s in bstates:
    for a, b in s[1]:
        for q in tq(edge(a, b)): labs.add(q[2])
LAB = sorted(labs); print('quarter labels', LAB)
def kappa(pend, row=-1):
    ess = [edge(a, b) for a, b in pend]
    mult = Counter()
    for e in ess: mult.update(q for q in tq(e) if q[1] == row)
    k = Fraction(0); br = Counter()
    for q in LAB:
        m0 = mult[(0, row, q)]; m1 = mult[(1, row, q)]
        br['H0'] += (m0 == 0); br['col1'] += Fraction(abs(m1 - 1), 2)
        br['W3'] += (m0-1)*(m0-2)//2 if m0 >= 1 else 0; br['W3'] += (m1-1)*(m1-2)//2 if m1 >= 1 else 0
    for (x, y, q), m in mult.items():
        if x >= 2: br['C2'] += m*(m-1)//2
    for e, f in combinations(ess, 2):
        ov = tq(e) & tq(f)
        if len(ov) == 1 and next(iter(ov))[1] == row: br['X1'] += 1
    for (x0, y0), (x1, y1) in pend:
        if {x0, x1} == {1, 2}: br['c'] += Fraction(1, 2)
    return sum(br.values()), br
K = [kappa(s[1]) for s in bstates]
loops = [(u, W, m) for u, v, W, m in rows if u == v]
bad = [(u, W) for u, W, m in loops if K[u][0] != 2*W - 2]
print('self loops', len(loops), 'identity failures', len(bad), bad[:5])
for k in (0, 1):
    cnt = Counter()
    for u, v, W, m in rows:
        g = g_of(m, k)
        kk = K[v][0] if k == 0 else K[u][0]   # DOWN: square row r-1 = pending at START of row r
        cnt[(g, kk >= 2*g)] += 1
    print('orient', k, Counter(cnt))
import pickle; pickle.dump(K, open('gap/lowerbounds/simple_strip/kappa.pkl', 'wb'))
