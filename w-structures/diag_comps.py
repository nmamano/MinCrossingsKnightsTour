import sys, ast
sys.path.insert(0, '/home/nil/nil/knight-formation-research/w-lowerbounds')
from fold_complete2 import base
import networkx as nx
from collections import Counter
n = int(sys.argv[1]); ts = ast.literal_eval(sys.argv[2]); ms = ast.literal_eval(sys.argv[3])
E, deg = base(n, ts=ts, ms=ms)
G = nx.Graph(); G.add_edges_from(E)
def lab(p):
    x, y = p
    s = lambda v: 'L' if v < n // 3 else ('H' if v >= 2 * n // 3 else 'M')
    return s(x) + s(y)
out = Counter()
for c in nx.connected_components(G):
    closed = all(deg[p] == 2 for p in c)
    labs = Counter(lab(p) for p in c)
    key = ('cyc' if closed else 'path') + ':' + '+'.join(sorted(labs))
    out[key] += 1
for k, v in sorted(out.items()):
    print(v, k)
