"""Potential for cost 2*kappa(r) - 4*g(r) on the no-cycle row graph (UP: kappa of end state; DOWN: of start state)."""
import sys, pickle, numpy as np
from collections import Counter
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
S = np.array([u for u, v, W, m in rows]); D = np.array([v for u, v, W, m in rows])
for k, us in ((0, 0), (0, 1), (1, 0), (1, 1)):
    C = np.array([int(2*(K[u][0] if us else K[v][0])) - 4*g_of(m, k) for u, v, W, m in rows])
    d = np.zeros(len(bstates), dtype=np.int64)
    for it in range(2000):
        nd = d.copy(); np.minimum.at(nd, D, d[S] + C)
        if np.array_equal(nd, d): break
        d = nd
    else: print('NO fixed point (negative cycle)'); continue
    print("orient", k, "start-kappa" if us else "end-kappa", 'passes', it, 'range', d.min(), d.max(), Counter(d).most_common(12))
    np.save(f'gap/lowerbounds/simple_strip/kpot_{k}_{us}.npy', d)
