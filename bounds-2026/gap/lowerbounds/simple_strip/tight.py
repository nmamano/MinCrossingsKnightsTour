"""Row-level tight structure. cost = 4W - 4 - 4*lam*g. Prints SCCs of tight arcs and short cycles."""
import pickle, sys, numpy as np, networkx as nx
from collections import Counter
G = pickle.load(open('gap/lowerbounds/simple_strip/graph.pkl', 'rb')); R = pickle.load(open('gap/lowerbounds/simple_strip/rows.pkl', 'rb'))
states, nodes, es, vis, tests = G['states'], G['nodes'], G['es'], G['vispairs'], G['tests']
bits = {e: 1 << i for i, e in enumerate(es)}
def g_of(m, k):
    coef, exc = tests[k]
    F = sum(c for e, c in coef.items() if m & bits[e]) % 3
    E = all(m & bits[e] for e in exc)
    V = any(m & v == v for v, a, b, ov in vis[k])
    return int(F != 2 or E or V), F, int(E), int(V)
lam = int(sys.argv[1]) if len(sys.argv) > 1 else 0
bnd = R['bnd']; rows = R['rows']
bi = {b: i for i, b in enumerate(bnd)}
S = np.array([bi[u] for u, v, W, m in rows]); D = np.array([bi[v] for u, v, W, m in rows])
GG = [g_of(m, 0) for u, v, W, m in rows]
C = np.array([4*W - 4 - 4*lam*gg[0] for (u, v, W, m), gg in zip(rows, GG)])
d = np.zeros(len(bnd), dtype=np.int64)
for it in range(500):
    nd = d.copy(); np.minimum.at(nd, D, d[S] + C)
    if np.array_equal(nd, d): break
    d = nd
else: raise SystemExit('no fixed point')
print('lam', lam, 'passes', it, 'range', d.min(), d.max())
sl = C + d[S] - d[D]
T = nx.DiGraph()
for j in np.nonzero(sl == 0)[0]: T.add_edge(int(S[j]), int(D[j]), j=int(j))
sccs = [c for c in nx.strongly_connected_components(T) if len(c) > 1 or any(T.has_edge(x, x) for x in c)]
print('tight SCCs:', len(sccs), 'sizes', sorted(map(len, sccs), reverse=True)[:20])
def show(u):
    return ' '.join(f'{a}->{b}' for a, b, c in states[nodes[bnd[u]][0]][1])
for c in sorted(sccs, key=len)[:12]:
    sub = T.subgraph(c)
    cyc = next(nx.simple_cycles(sub))
    print('--- SCC size', len(c), 'cycle len', len(cyc))
    for k, x in enumerate(cyc):
        y = cyc[(k+1) % len(cyc)]; j = T[x][y]['j']
        print('  ', show(x), '| W', rows[j][2], 'g', GG[j])
pickle.dump(dict(d=d, sl=sl), open(f'gap/lowerbounds/simple_strip/tight_{lam}.pkl', 'wb'))
