import sys, pickle, numpy as np
from fractions import Fraction as Fr
from collections import Counter
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
k2 = np.array([int(2*K[v][0]) for v in range(len(bstates))])
for k in (0, 1):
    G = [g_of(m, k) for u, v, W, m in rows]
    for a in [Fr(i, 8) for i in range(9)]:
        fails = sum(1 for (u, v, W, m), g in zip(rows, G) if a*k2[u] + (1-a)*k2[v] < 4*g)
        print('orient', k, 'alpha(start weight)', a, 'fails', fails)
