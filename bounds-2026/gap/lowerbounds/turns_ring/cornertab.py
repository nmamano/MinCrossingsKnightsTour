"""BL corner table for a single-family straight interior (field f, interior = x>=4 and y>=4, quadrant board).
Block = {x<4, y<D} U {y<4, x<D}. Output: dict (left cut at row D, bottom cut at column D) -> min sum r over the block.
Left cut in steep-strip frame (x, y-D, dx, dy); bottom cut in grazing frame (X,Y)=(y,x): (y0, x0-D, dy, dx)."""
import sys, pickle
from itertools import combinations
sys.path.insert(0, '/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring')
from strip import M, lower


def rq(p, a, b):
    t = int(a[0] + b[0] != 0 or a[1] + b[1] != 0)
    return t - lower(p[0], [a[0], b[0]]) - lower(p[1], [a[1], b[1]])


def corner_table(f, D=8, budget=None):
    fm = [f, (-f[0], -f[1])]
    interior = lambda q: q[0] >= 4 and q[1] >= 4
    inblock = lambda q: (q[0] < 4 and 0 <= q[1] < D) or (q[1] < 4 and 0 <= q[0] < D)
    # order: corner square column-wise, then bottom arm columns 4..D-1, then left arm rows 4..D-1
    order = [(x, y) for y in range(4) for x in range(4)]
    order += [(x, y) for x in range(4, D) for y in range(4)] + [(x, y) for y in range(4, D) for x in range(4)]
    pos = {p: i for i, p in enumerate(order)}
    # interior cells whose line points into the block: forced edges
    fint = {p: [d for d in M if interior((p[0] + d[0], p[1] + d[1])) and (-d[0], -d[1]) in fm] for p in order}
    # optimistic remaining bound: per-cell minimum of r
    def cellmin(p):
        ds = [d for d in M if p[0] + d[0] >= 0 and p[1] + d[1] >= 0]
        return min(rq(p, a, b) for a, b in combinations(ds, 2))
    rem = [0] * (len(order) + 1)
    for i in range(len(order) - 1, -1, -1): rem[i] = rem[i + 1] + min(0, cellmin(order[i]))
    front = {frozenset(): 0}
    for i, p in enumerate(order):
        nf = {}
        cands = []
        for d in M:
            q = (p[0] + d[0], p[1] + d[1])
            if q[0] < 0 or q[1] < 0 or interior(q): continue
            if inblock(q) and pos[q] < i: continue
            cands.append(d)
        for fs, c0 in front.items():
            if budget is not None and c0 + rem[i] > budget: continue
            inc = [(a[0] - p[0], a[1] - p[1]) for a, b in fs if b == p]
            base = inc + fint[p]
            if len(base) > 2: continue
            rest = frozenset(e for e in fs if e[1] != p)
            for extra in combinations([d for d in cands if d not in base], 2 - len(base)):
                mv = base + list(extra)
                fs2 = rest | frozenset((p, (p[0] + d[0], p[1] + d[1])) for d in extra)
                load = {}
                for a, b in fs2: load[b] = load.get(b, 0) + 1
                if any(v > 2 for v in load.values()): continue
                c = c0 + rq(p, mv[0], mv[1])
                if c < nf.get(fs2, 10 ** 9): nf[fs2] = c
        front = nf
    table = {}
    for fs, c in front.items():
        if budget is not None and c > budget: continue
        L = frozenset((a[0], a[1] - D, b[0] - a[0], b[1] - a[1]) for a, b in fs if b[1] >= D)
        B = frozenset((a[1], a[0] - D, b[1] - a[1], b[0] - a[0]) for a, b in fs if b[0] >= D)
        assert len(L) + len(B) == len(fs)
        table[(L, B)] = min(table.get((L, B), 10 ** 9), c)
    return table


if __name__ == '__main__':
    f = (int(sys.argv[1]), int(sys.argv[2])); D = int(sys.argv[3]); budget = int(sys.argv[4])
    T = corner_table(f, D, budget)
    vals = sorted(T.values())
    print('field', f, 'D', D, 'budget', budget, 'table entries', len(T), 'min', vals[0] if vals else None,
          'distribution', {v: vals.count(v) for v in sorted(set(vals))[:10]}, flush=True)
    pickle.dump(T, open(f'/home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring/corner_{f[0]}_{f[1]}_D{D}.pkl', 'wb'))
