"""Fold field (from w-lowerbounds/fold_board.py) + configurable edge U-turns (KT Structures)."""
import sys
from collections import Counter, defaultdict
sys.path.insert(0, '/home/nil/nil/knight-formation-research/w-lowerbounds')
from fold_board import field
import networkx as nx

def rot(p, n):            # 90 deg CCW map used to place edge r=0 (left) onto other edges
    return (n - 1 - p[1], p[0])

def build(n, ts=(0, 0, 0, 0), ms=(0, 0, 0, 0), uturn=None):
    """uturn(r, y, parity) -> +1/-1 : direction of the U-turn partner (1, y + 2*dir) in the
    frame of edge r (r=0 left edge column 0, rotated r times CCW about the board)."""
    v = field(n, ts=ts, ms=ms)
    on = lambda p: 0 <= p[0] < n and 0 <= p[1] < n
    E = set()
    for p, d in v.items():
        q = (p[0] + d[0], p[1] + d[1])
        if on(q):
            E.add(tuple(sorted([p, q])))
    deg = Counter()
    for e in E:
        deg[e[0]] += 1; deg[e[1]] += 1
    def R(p, k):
        for _ in range(k):
            p = rot(p, n)
        return p
    U = set()
    for r in range(4):
        for y in range(n):
            p = R((0, y), r)
            if deg[p] != 1:
                continue
            dr = uturn(r, y, y % 2) if uturn else 1
            q = R((1, y + 2 * dr), r)
            if on(q) and deg[q] == 1:
                e = tuple(sorted([p, q]))
                if e not in E:
                    E.add(e); U.add(e); deg[p] += 1; deg[q] += 1
    return E, deg, U

def stats(n, E, deg):
    G = nx.Graph(); G.add_edges_from(E)
    comps = list(nx.connected_components(G))
    cyc = [c for c in comps if all(deg[p] == 2 for p in c)]
    bad = [p for p in G if deg[p] != 2]
    return len(comps), len(cyc), len(bad), sorted(len(c) for c in comps)
