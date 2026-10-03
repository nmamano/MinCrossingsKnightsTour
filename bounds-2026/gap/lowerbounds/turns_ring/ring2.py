"""L1: ring DP for one straight interior family, single start state s0 at the left-side middle cut (rows y0-1 | y0).
Exact for that s0. Pruning: cost so far + optimistic rest (corner -7 or per-cell minima, else 0) > UB is dropped.
usage: ring2.py n UB [dx dy]   (s0 runs over the states of the zero classes of the steep strip graph)
"""
import sys, pickle, time
from itertools import combinations
sys.path.insert(0, '/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring')
from ring import M, lower, rcost, ring_order

STEEP = '/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring/fstrip_2_-1.pkl'


def solve(n, field, s0, UB, witness=False):
    y0 = n // 2
    depth = lambda p: min(p[0], p[1], n - 1 - p[0], n - 1 - p[1])
    on = lambda p: 0 <= p[0] < n and 0 <= p[1] < n
    order = ring_order(n); pos = {p: i for i, p in enumerate(order)}
    fm = [field, (-field[0], -field[1])]
    fint = {p: [d for d in M if on((p[0]+d[0], p[1]+d[1])) and depth((p[0]+d[0], p[1]+d[1])) >= 4 and (-d[0], -d[1]) in fm]
            for p in order}
    crosses = lambda a, b: (a[1] < y0) != (b[1] < y0) and a[0] < 4 and b[0] < 4
    corners = [[(x, y) for x in xs for y in ys] for xs in (range(4), range(n-4, n)) for ys in (range(4), range(n-4, n))]
    def cmin(p):
        return min(rcost(n, p, a, b) for a, b in combinations([d for d in M if on((p[0]+d[0], p[1]+d[1]))], 2))
    cm = {p: cmin(p) for c in corners for p in c}
    rem = []
    for i in range(len(order) + 1):
        s = 0
        for c in corners:
            left = [p for p in c if pos[p] >= i]
            s += -7 if len(left) == 16 else sum(cm[p] for p in left)
        rem.append(s)
    # s0: steep frame (x, yy, dx, dy) relative to row y0 -> absolute edge (low, high); flagged
    start = frozenset(((x, y0 + yy), (x + dx, y0 + yy + dy), 1) for (x, yy, dx, dy) in s0)
    front = {start: (0, None)}
    for i, p in enumerate(order):
        nf = {}
        cands = []
        for d in M:
            q = (p[0]+d[0], p[1]+d[1])
            if on(q) and depth(q) <= 3 and pos[q] > i and not crosses(p, q): cands.append(d)
        for fs, (c0, wit) in front.items():
            if c0 + rem[i] > UB: continue
            inc = [(a, fl) for a, b, fl in fs if b == p]
            base = [(a[0]-p[0], a[1]-p[1]) for a, fl in inc] + fint[p]
            if len(base) > 2: continue
            rest = frozenset(e for e in fs if e[1] != p) | frozenset((p, a, 0) for a, fl in inc if fl)
            for extra in combinations([d for d in cands if d not in base], 2 - len(base)):
                mv = base + list(extra)
                fs2 = rest | frozenset((p, (p[0]+d[0], p[1]+d[1]), 0) for d in extra)
                load = {}
                for a, b, fl in fs2: load[b] = load.get(b, 0) + 1
                if any(v + len(fint[b]) > 2 for b, v in load.items()): continue
                c = c0 + rcost(n, p, mv[0], mv[1])
                if fs2 not in nf or c < nf[fs2][0]:
                    nf[fs2] = (c, (wit, p, tuple(mv)) if witness else None)
        front = nf
        if not front: return None
    best = front.get(frozenset())
    return best


if __name__ == '__main__':
    n = int(sys.argv[1]); UB = int(sys.argv[2]); field = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (2, -1)
    states, arcs, zc = pickle.load(open(STEEP, 'rb'))
    cand = sorted(set().union(*[c for c, g in zc]))
    t0 = time.time(); results = {}
    for s in cand:
        r = solve(n, field, states[s], UB)
        results[s] = None if r is None else r[0]
        print('n', n, 's0', s, sorted(states[s]), '->', results[s], f'{time.time()-t0:.0f}s', flush=True)
    vals = [v for v in results.values() if v is not None]
    print('n', n, 'field', field, 'MIN over zero-class s0:', min(vals) if vals else f'none <= {UB}', flush=True)
