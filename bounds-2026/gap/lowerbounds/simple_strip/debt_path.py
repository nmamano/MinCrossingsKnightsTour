"""Shortest (cost 2kappa(end)-4g, UP) path Q -> P: shows a g-row debt that no bounded window can pay."""
import sys, pickle, numpy as np
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
k2 = [int(2*K[v][0]) for v in range(len(bstates))]
P = bstates.index((0, (((0, -2), (1, 0)), ((0, -1), (1, 1)), ((0, -1), (2, 0)), ((1, -1), (3, 0)))))
Q = bstates.index((0, (((1, -2), (0, 0)), ((1, -1), (0, 1)), ((2, -1), (0, 0)), ((3, -1), (1, 0)))))
INF = 10**9; d = [INF]*len(bstates); pred = [None]*len(bstates); d[Q] = 0
arcs = [(u, v, W, m, k2[v] - 4*g_of(m, 0)) for u, v, W, m in rows]
for it in range(200):
    ch = False
    for j, (u, v, W, m, c) in enumerate(arcs):
        if d[u] < INF and d[u] + c < d[v]: d[v] = d[u] + c; pred[v] = j; ch = True
    if not ch: break
print('d(Q->P) =', d[P])
path = []; x = P
while x != Q:
    j = pred[x]; path.append(j); x = arcs[j][0]
for j in reversed(path):
    u, v, W, m, c = arcs[j]
    print(f'W={W} g={g_of(m,0)} 2kappa(end)={k2[v]} cost={c} new-row edges={sorted(e for e in [es[i] for i in range(20) if m>>i&1] if min(e[0][1],e[1][1])==0)}')
