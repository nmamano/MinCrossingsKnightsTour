import sys, itertools
sys.path.insert(0, '/home/nil/nil/knight-formation-research/w-lowerbounds')
from fold_complete2 import base
import networkx as nx
n = int(sys.argv[1])
res = []
for t in range(-3, 4):
    for m in range(-3, 4):
        ts = (t, t, t, t); ms = (m, m, m, m)
        E, deg = base(n, ts=ts, ms=ms)
        G = nx.Graph(); G.add_edges_from(E)
        comps = list(nx.connected_components(G))
        cyc = sum(1 for c in comps if all(deg[p] == 2 for p in c))
        bad = sum(1 for p in G if deg[p] != 2) + sum(1 for x in range(n) for y in range(n) if deg[(x,y)] == 0)
        print(ts[0], ms[0], 'comps', len(comps), 'cycles', cyc, 'bad', bad, flush=True)
