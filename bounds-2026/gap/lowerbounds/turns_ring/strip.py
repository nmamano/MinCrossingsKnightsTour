"""L1 step 1: side strip of width W (columns 0..W-1, side at x=0), rows infinite. Moves into x>=W are free (relaxation).
Row-level transfer graph on cut states (set of in-strip edges crossing the cut). Cost per cell r = t - L_x (L of
writeup/turns Lemma 'four-column'). Prints sizes, min cycle mean check, critical (zero-cost) structure."""
import sys, pickle
from itertools import combinations
M = [(dx, dy) for dx in (-2, -1, 1, 2) for dy in (-2, -1, 1, 2) if abs(dx) + abs(dy) == 3]
def lower(x, dxs):
    if x == 0: return 1
    if x in (1, 2): return sum(x + d in (0, 3) for d in dxs) - 1
    if x == 3: return 1 - sum(x + d in (1, 2) for d in dxs)
    return 0
def rcost(x, a, b):
    t = int(a[0] + b[0] != 0 or a[1] + b[1] != 0)
    return t - lower(x, [a[0], b[0]])
def row_arcs(state, W):
    """state: frozenset of moves pending as (x0, y0, dx, dy) with y0<0<=y0+dy, both ends in strip. Yields (next, cost, choice)."""
    inc = {}
    for (x0, y0, dx, dy) in state:
        if y0 + dy == 0: inc.setdefault(x0 + dx, []).append((-dx, -dy))
    if any(len(v) > 2 for v in inc.values()): return
    opts = []
    for x in range(W):
        forced = inc.get(x, [])
        free = [d for d in M if x + d[0] >= 0 and (x + d[0] >= W or d[1] > 0)]
        free = [d for d in free if d not in forced]
        cs = []
        for extra in combinations(free, 2 - len(forced)):
            mv = forced + list(extra)
            cs.append((tuple(mv), rcost(x, mv[0], mv[1])))
        opts.append(cs)
    def rec(x, acc, cost):
        if x == W: yield acc, cost; return
        for mv, c in opts[x]: yield from rec(x + 1, acc + [(x, mv)], cost + c)
    keep = [(x0, y0, dx, dy) for (x0, y0, dx, dy) in state if y0 + dy > 0]
    for choice, cost in rec(0, [], 0):
        new = [(x, 0, dx, dy) for x, mv in choice for dx, dy in mv if dy > 0 and x + dx < W]
        load = {}
        for (x0, y0, dx, dy) in keep + new:
            k = (x0 + dx, y0 + dy); load[k] = load.get(k, 0) + 1
        if any(v > 2 for v in load.values()): continue
        nxt = frozenset((x0, y0 - 1, dx, dy) for (x0, y0, dx, dy) in keep + new)
        yield nxt, cost, choice
def build(W):
    start = frozenset(); states = [start]; ids = {start: 0}; arcs = []
    for s in states:
        best = {}
        for t, c, ch in row_arcs(s, W):
            if t not in ids: ids[t] = len(states); states.append(t)
            v = ids[t]
            if v not in best or c < best[v][0]: best[v] = (c, ch)
        for v, (c, ch) in best.items(): arcs.append((ids[s], v, c, ch))
    return states, arcs
if __name__ == '__main__':
    W = int(sys.argv[1])
    states, arcs = build(W)
    print('W', W, 'states', len(states), 'arcs (min-cost per pair)', len(arcs), 'min arc cost', min(a[2] for a in arcs), flush=True)
    pickle.dump((states, arcs), open(f'/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring/strip_W{W}.pkl', 'wb'))
