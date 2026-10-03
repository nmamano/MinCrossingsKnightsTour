"""Constants for the stability lemma (width-2 strip transfer graph, crossings).
Exact potential d = shortest distance from the start with weights w - 1/4 (Bellman-Ford, integers x4).
Reduced cost red(u,v) = w - 1/4 + d(u) - d(v) >= 0, all in (1/4)Z. Report: rho = min positive reduced cost,
the critical (tight) cycles, T* = longest path in (tight graph minus critical-cycle edges), and the
range of d over states reachable from the start (for the additive constant)."""
import sys
from fractions import Fraction
import networkx as nx
from strip_dp import build
states, adj, W = build(2)
n = len(states)
# integer weights scaled by 4: w4 = 4w - 1
INF = 10**18
d = [INF] * n; d[0] = 0
for it in range(n + 1):
    ch = False
    for u in range(n):
        if d[u] == INF: continue
        for v, w in adj[u]:
            nd = d[u] + 4 * w - 1
            if nd < d[v]: d[v] = nd; ch = True
    if not ch: break
assert not ch, 'negative cycle'
reach = [u for u in range(n) if d[u] < INF]
red = {}
G = nx.DiGraph()
pos = []
for u in reach:
    for v, w in adj[u]:
        r = 4 * w - 1 + d[u] - d[v]
        assert r >= 0
        if r == 0: G.add_edge(u, v)
        else: pos.append(r)
print('states', n, 'reachable', len(reach), 'd range (x1/4):', min(d[u] for u in reach), max(d[u] for u in reach))
print('rho (x1/4) =', min(pos))
sccs = [c for c in nx.strongly_connected_components(G) if len(c) > 1 or any(G.has_edge(x, x) for x in c)]
print('tight SCCs', [len(c) for c in sccs])
cyc_edges = set()
for c in sccs:
    H = G.subgraph(c)
    cy = list(nx.simple_cycles(H)); assert len(cy) == 1 and len(cy[0]) == len(c), 'SCC is not a single cycle'
    cyc = cy[0]
    for i in range(len(cyc)): cyc_edges.add((cyc[i], cyc[(i + 1) % len(cyc)]))
    print(' cycle states:', [states[s] for s in cyc])
G2 = G.copy(); G2.remove_edges_from(cyc_edges)
assert nx.is_directed_acyclic_graph(G2)
print('T* (longest tight path avoiding critical-cycle edges, in cell steps) =', nx.dag_longest_path_length(G2))
