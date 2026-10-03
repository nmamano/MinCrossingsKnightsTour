import pickle, numpy as np
from collections import defaultdict, Counter
G = pickle.load(open('gap/lowerbounds/simple_strip/graph.pkl', 'rb')); R = pickle.load(open('gap/lowerbounds/simple_strip/rows.pkl', 'rb'))
states, nodes, es, vis, tests = G['states'], G['nodes'], G['es'], G['vispairs'], G['tests']
bits = {e: 1 << i for i, e in enumerate(es)}
def g_of(m, k):
    coef, exc = tests[k]
    F = sum(c for e, c in coef.items() if m & bits[e]) % 3
    E = all(m & bits[e] for e in exc)
    V = any(m & v == v for v, a, b, ov in vis[k])
    return int(F != 2 or E or V)
bnd = R['bnd']; rows = R['rows']
for k, name in enumerate(('up', 'down')):
    h = np.load(f'gap/verifier/claim42_potential_{name}.npy')
    sl = [4*W - 4 - 4*g_of(m, k) + h[u] - h[v] for u, v, W, m in rows]
    print(name, 'min row slack', min(sl), 'boundary h range', h[bnd].min(), h[bnd].max(), Counter(h[bnd]).most_common())
