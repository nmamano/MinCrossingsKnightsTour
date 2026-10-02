"""Fold field + U-turns with per-position choice (cheap or flipped). KT Structures 2026-10-02."""
import sys
from collections import Counter
sys.path.insert(0, '/home/nil/nil/knight-formation-research/w-lowerbounds')
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
from fold_board import field
import networkx as nx

def build(n, ts=(0, 0, 0, 0), ms=(0, 0, 0, 0), flip=None):
    """flip(r, y) -> bool: use the flipped (non-cheap) U-turn at end cell (0,y) of edge frame r."""
    v = field(n, ts=ts, ms=ms)
    on = lambda p: 0 <= p[0] < n and 0 <= p[1] < n
    E = set()
    for p, d in v.items():
        q = (p[0] + d[0], p[1] + d[1])
        if on(q):
            E.add(tuple(sorted([p, q])))
    adj = {p: [] for p in v}
    for a, b in E:
        adj[a].append(b); adj[b].append(a)
    deg = Counter({p: len(adj[p]) for p in v})
    rot = lambda p: (n - 1 - p[1], p[0])
    def R(p, k):
        for _ in range(k):
            p = rot(p)
        return p
    U = []
    for r in range(4):
        for y in range(n):
            p = R((0, y), r)
            if deg[p] != 1:
                continue
            nb = adj[p][0]
            dy = [d for d in (1, -1) if R((2, y + d), r) == nb]
            if not dy:
                continue
            dy = dy[0]
            if flip and flip(r, y):
                dy = -dy
            q = R((1, y + 2 * dy), r)
            if on(q) and deg[q] == 1:
                e = tuple(sorted([p, q]))
                if e not in E:
                    E.add(e); U.append(e); deg[p] += 1; deg[q] += 1
                    adj[p].append(q); adj[q].append(p)
    return E, deg

def comps(n, E, deg):
    G = nx.Graph(); G.add_nodes_from((x, y) for x in range(n) for y in range(n)); G.add_edges_from(E)
    cs = list(nx.connected_components(G))
    cyc = [c for c in cs if all(deg[p] == 2 for p in c)]
    bad = sorted(p for p in G if deg[p] != 2)
    return cs, cyc, bad
