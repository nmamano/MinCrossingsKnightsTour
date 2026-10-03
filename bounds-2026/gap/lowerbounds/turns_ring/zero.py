import sys, pickle, networkx as nx
from math import gcd
W = int(sys.argv[1])
states, arcs = pickle.load(open(f'/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring/strip_W{W}.pkl', 'rb'))
Z = nx.DiGraph(); Z.add_edges_from((u, v) for u, v, c, ch in arcs if c == 0)
print('zero arcs', Z.number_of_edges(), 'nodes', Z.number_of_nodes())
sccs = [c for c in nx.strongly_connected_components(Z) if len(c) > 1 or Z.has_edge(next(iter(c)), next(iter(c)))]
print('recurrent zero classes', len(sccs), sorted(map(len, sccs), reverse=True)[:20])
for c in sorted(sccs, key=len):
    sub = Z.subgraph(c)
    # period: gcd of (level differences) via BFS levels
    r = next(iter(c)); lev = {r: 0}; q = [r]; g = 0
    while q:
        x = q.pop()
        for y in sub.successors(x):
            if y not in lev: lev[y] = lev[x] + 1; q.append(y)
            else: g = gcd(g, lev[x] + 1 - lev[y])
    print('class size', len(c), 'period', g)
pickle.dump(sccs, open(f'/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring/zero_W{W}.pkl', 'wb'))
