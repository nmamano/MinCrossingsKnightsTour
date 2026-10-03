import sys, pickle
from collections import Counter
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
def parts(m, k=0):
    coef, exc = tests[k]
    F = sum(c for e, c in coef.items() if m & bits[e]) % 3
    E = all(m & bits[e] for e in exc)
    V = any(m & v == v for v, a, b, ov in vis[k])
    return F, int(E), int(V)
c = Counter(); ex = {}
for j, (u, v, W, m) in enumerate(rows):
    g = g_of(m, 0)
    if g and K[v][0] < 2:
        key = (K[v][0], parts(m), K[u][0] - 2*g_of(0, 0) if False else K[u][0])
        c[(K[v][0], parts(m))] += 1; ex.setdefault((K[v][0], parts(m)), j)
for k, n in sorted(c.items()): print(k, n)
for key, j in ex.items():
    u, v, W, m = rows[j]
    print(key, 'W', W, 'before', bstates[u][1], '\n   after', bstates[v][1], '\n   mask', [es[i] for i in range(20) if m >> i & 1], dict(K[v][1]))
