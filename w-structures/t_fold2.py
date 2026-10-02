import sys
from fold2 import build, stats
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
from kt.core import crossing_list
import networkx as nx
for n in (48, 96):
    E, deg, U = build(n)
    X = len(crossing_list(E))
    c = stats(n, E, deg)
    bad = sorted((p, deg[p]) for p in deg if deg[p] != 2)
    zero = [(x, y) for x in range(n) for y in range(n) if deg[(x, y)] == 0]
    print(n, 'X', X, 'X-4n', X - 4 * n, 'comps', c[:3], 'sizes', c[3])
    print('  bad', bad, 'deg0', zero)
