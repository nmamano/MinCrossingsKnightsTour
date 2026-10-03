"""Single-source shortest paths for cost 2kappa(end)-4g from P (and from Q)."""
import sys, pickle, numpy as np
from collections import Counter
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
k2 = np.array([int(2*K[v][0]) for v in range(len(bstates))])
S = np.array([u for u, v, W, m in rows]); D = np.array([v for u, v, W, m in rows])
P = bstates.index((0, (((0, -2), (1, 0)), ((0, -1), (1, 1)), ((0, -1), (2, 0)), ((1, -1), (3, 0)))))
Q = bstates.index((0, (((1, -2), (0, 0)), ((1, -1), (0, 1)), ((2, -1), (0, 0)), ((3, -1), (1, 0)))))
for k in (0, 1):
    C = np.array([k2[v] - 4*g_of(m, k) for u, v, W, m in rows])
    for name, src in (('P', P), ('Q', Q)):
        d = np.full(len(bstates), 10**9); d[src] = 0
        for it in range(3000):
            nd = d.copy(); np.minimum.at(nd, D, d[S] + C)
            if np.array_equal(nd, d): break
            d = nd
        print('orient', k, 'from', name, 'min', d.min(), 'max', d.max(), 'neg states', int((d < 0).sum()), 'd(P),d(Q)', d[P], d[Q])
