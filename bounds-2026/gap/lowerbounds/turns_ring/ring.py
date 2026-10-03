"""L1: exact minimum of T - 8n over 2-factors of the n x n knight graph whose interior (cells at depth >= 4 from every
side) is ONE straight-line family with no interior turn. Ring = cells at depth <= 3. Cyclic frontier DP.
r(v) = t(v) - sum over sides of L_depth(v)  (writeup/turns Lemma 'four-column' / corner lemma).
usage: ring.py n [dx dy]   (interior direction, default 2 -1)
"""
import sys
from itertools import combinations
M = [(dx, dy) for dx in (-2, -1, 1, 2) for dy in (-2, -1, 1, 2) if abs(dx) + abs(dy) == 3]


def lower(x, dxs):
    if x == 0: return 1
    if x in (1, 2): return sum(x + d in (0, 3) for d in dxs) - 1
    if x == 3: return 1 - sum(x + d in (1, 2) for d in dxs)
    return 0


def rcost(n, p, a, b):
    x, y = p
    t = int(a[0] + b[0] != 0 or a[1] + b[1] != 0)
    return (t - lower(x, [a[0], b[0]]) - lower(n - 1 - x, [-a[0], -b[0]])
            - lower(y, [a[1], b[1]]) - lower(n - 1 - y, [-a[1], -b[1]]))


def ring_order(n):
    y0 = n // 2
    order = [(x, y) for y in range(y0, n) for x in range(4)]                       # left side up (TL corner)
    order += [(x, y) for x in range(4, n) for y in range(n - 1, n - 5, -1)]           # top strip rightwards (TR corner)
    order += [(x, y) for y in range(n - 5, -1, -1) for x in range(n - 1, n - 5, -1)]  # right side down (BR corner)
    order += [(x, y) for x in range(n - 5, -1, -1) for y in range(4)]                 # bottom strip leftwards (BL)
    order += [(x, y) for y in range(4, y0) for x in range(4)]                         # left side up to start
    assert len(order) == len(set(order)) == n * n - (n - 8) ** 2
    return order


def solve(n, field, keep_witness=False):
    depth = lambda p: min(p[0], p[1], n - 1 - p[0], n - 1 - p[1])
    on = lambda p: 0 <= p[0] < n and 0 <= p[1] < n
    order = ring_order(n); pos = {p: i for i, p in enumerate(order)}
    fmoves = [field, (-field[0], -field[1])]
    fint = {}
    for p in order:
        fi = []
        for d in M:
            q = (p[0] + d[0], p[1] + d[1])
            if on(q) and depth(q) >= 4 and (-d[0], -d[1]) in fmoves: fi.append(d)
        fint[p] = fi
        # interior cells next to the ring must have both forced neighbours on the board
    for x in range(4, n - 4):
        for y in range(4, n - 4):
            for d in fmoves:
                if not on((x + d[0], y + d[1])): return None, 'interior line leaves board'
    front = {frozenset(): (0, None)}
    for i, p in enumerate(order):
        nf = {}
        cands = []
        for d in M:
            q = (p[0] + d[0], p[1] + d[1])
            if on(q) and depth(q) <= 3 and pos[q] > i: cands.append(d)
        for fs, (c0, wit) in front.items():
            inc = [(a[0] - p[0], a[1] - p[1]) for a, b in fs if b == p]
            base = inc + fint[p]
            if len(base) > 2: continue
            rest = frozenset(e for e in fs if e[1] != p)
            for extra in combinations([d for d in cands if d not in base], 2 - len(base)):
                mv = base + list(extra)
                new = frozenset((p, (p[0] + d[0], p[1] + d[1])) for d in extra)
                fs2 = rest | new
                load = {}
                for a, b in fs2: load[b] = load.get(b, 0) + 1
                if any(v + len(fint[b]) > 2 for b, v in load.items()): continue
                c = c0 + rcost(n, p, mv[0], mv[1])
                if fs2 not in nf or c < nf[fs2][0]:
                    nf[fs2] = (c, (wit, p, tuple(mv)) if keep_witness else None)
        front = nf
        if i % 50 == 0 or len(front) > 200000: print('  cell', i, p, 'frontier', len(front), flush=True)
        if not front: return None, f'dead at {p}'
    if frozenset() not in front: return None, 'no closing state'
    return front[frozenset()], max(1, 0)


if __name__ == '__main__':
    n = int(sys.argv[1]); field = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (2, -1)
    res, info = solve(n, field)
    print('n', n, 'field', field, 'min T-8n (single family, no interior turn):', res if res is None else res[0], info, flush=True)
