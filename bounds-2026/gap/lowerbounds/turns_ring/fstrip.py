"""Width-4 side strip with a forced straight interior (one line family f in the strip frame: X inward, Y along).
Interior cells X>=4 are straight in direction +-f, so strip cells must take exactly the moves into X>=4 that are +-f."""
import sys, pickle
from itertools import combinations
from math import gcd
sys.path.insert(0, '/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring')
from strip import M, lower, rcost
import networkx as nx
WD = 4
def row_arcs(state, f):
    fm = [f, (-f[0], -f[1])]
    inc = {}
    for (x0, y0, dx, dy) in state:
        if y0 + dy == 0: inc.setdefault(x0 + dx, []).append((-dx, -dy))
    if any(len(v) > 2 for v in inc.values()): return
    opts = []
    for x in range(WD):
        forced = inc.get(x, []) + [d for d in fm if x + d[0] >= WD]
        if len(forced) > 2: return
        free = [d for d in M if 0 <= x + d[0] < WD and d[1] > 0 and d not in forced]
        cs = []
        for extra in combinations(free, 2 - len(forced)):
            mv = forced + list(extra); cs.append((tuple(mv), rcost(x, mv[0], mv[1])))
        opts.append(cs)
    def rec(x, acc, cost):
        if x == WD: yield acc, cost; return
        for mv, c in opts[x]: yield from rec(x + 1, acc + [(x, mv)], cost + c)
    keep = [e for e in state if e[1] + e[3] > 0]
    for choice, cost in rec(0, [], 0):
        new = [(x, 0, dx, dy) for x, mv in choice for dx, dy in mv if dy > 0 and x + dx < WD]
        load = {}
        for (x0, y0, dx, dy) in keep + new:
            k = (x0 + dx, y0 + dy); load[k] = load.get(k, 0) + 1
        if any(v > 2 for v in load.values()): continue
        yield frozenset((x0, y0 - 1, dx, dy) for (x0, y0, dx, dy) in keep + new), cost, choice
def build(f):
    states = [frozenset()]; ids = {states[0]: 0}; arcs = []
    for s in states:
        best = {}
        for t, c, ch in row_arcs(s, f):
            if t not in ids: ids[t] = len(states); states.append(t)
            v = ids[t]
            if v not in best or c < best[v][0]: best[v] = (c, ch)
        for v, (c, ch) in best.items(): arcs.append((ids[s], v, c, ch))
    return states, arcs
def zero_classes(states, arcs):
    Z = nx.DiGraph(); Z.add_edges_from((u, v) for u, v, c, ch in arcs if c == 0)
    out = []
    for comp in nx.strongly_connected_components(Z):
        r = next(iter(comp))
        if len(comp) == 1 and not Z.has_edge(r, r): continue
        sub = Z.subgraph(comp); lev = {r: 0}; q = [r]; g = 0
        while q:
            x = q.pop()
            for y in sub.successors(x):
                if y not in lev: lev[y] = lev[x] + 1; q.append(y)
                else: g = gcd(g, lev[x] + 1 - lev[y])
        out.append((comp, g))
    return out
if __name__ == '__main__':
    for name, f in (('steep (left side, field (2,-1))', (2, -1)), ('grazing (bottom side, field (1,-2) in frame)', (1, -2))):
        states, arcs = build(f)
        zc = zero_classes(states, arcs)
        print(name, 'states', len(states), 'arcs', len(arcs), 'zero classes (size, period):', [(len(c), g) for c, g in zc], flush=True)
        pickle.dump((states, arcs, zc), open(f'/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring/fstrip_{f[0]}_{f[1]}.pkl', 'wb'))
