"""Corner charge Q (exact): loop = boundary path at depth 1/2 (down the left edge, along the bottom)
+ first segments of the two connectors. Edges: pattern A on the left (rows >= 4), transposed pattern B
on the bottom (cols >= 4); corner cells K = {(0,y): y<4} u {(x,0): 1<=x<4} take every possible pair of
knight moves (consistently). If Q != 0 mod 3 for every option, the corner is charged."""
import sys, itertools
from strip_dp import cross
chi = lambda p: 1 if (p[0] + p[1]) % 2 == 0 else -1
KM = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
def pattern_edges(kind, rows):
    s = 1 if kind == 'P' else -1
    out = set()
    for y in rows:
        for a, b in [((0, y), (2, y + s)), ((0, y), (1, y + 2 * s)), ((1, y), (3, y + s))]:
            if min(a[1], b[1]) >= 0: out.add(tuple(sorted([a, b])))
    return out
def phi(E, A, B):
    t = 0
    for e in E:
        if cross((*A, *B), (*e[0], *e[1])):
            side = lambda P: (B[0] - A[0]) * (P[1] - A[1]) - (B[1] - A[1]) * (P[0] - A[0])
            left = e[0] if side(e[0]) > 0 else e[1]
            t += chi(left)
    return t
def cright(A, B):
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    dx, dy = B[0] - A[0], B[1] - A[1]
    rx, ry = dy, -dx          # right normal
    return (round(mx + 0.5 * rx), round(my + 0.5 * ry))
def Q(E, R):
    pts = [(0.5, R + 0.5 - k) for k in range(R + 1)] + [(0.5 + k, 0.5) for k in range(1, R + 1)]
    pts += [(R + 0.5, 1.5)]                       # bottom connector first segment (up)
    segs = list(zip(pts, pts[1:])) + [((1.5, R + 0.5), (0.5, R + 0.5))]   # left connector first seg (west)
    return sum(phi(E, A, B) - chi(cright(A, B)) for A, B in segs)
K = [(0, y) for y in range(4)] + [(x, 0) for x in range(1, 4)]
on = lambda p: p[0] >= 0 and p[1] >= 0
for A_, B_ in itertools.product('PQ', 'PQ'):
    for R in (12, 13, 14, 15):
        base = pattern_edges(A_, range(4, R + 8))
        base |= {tuple(sorted([(a[1], a[0]), (b[1], b[0])])) for a, b in pattern_edges(B_, range(4, R + 8))}
        # degree already used at K cells by base edges
        used = {c: sum(1 for e in base if c in e) for c in K}
        opts = {c: [] for c in K}
        for c in K:
            nb = [(c[0] + dx, c[1] + dy) for dx, dy in KM if on((c[0] + dx, c[1] + dy))]
            for pair in itertools.combinations(nb, 2 - used[c]) if used[c] <= 2 else []:
                opts[c].append(pair)
        vals = set()
        for choice in itertools.product(*[opts[c] for c in K]):
            E = set(base)
            for c, pair in zip(K, choice):
                for q in pair: E.add(tuple(sorted([c, q])))
            # consistency: an edge between two K cells must be chosen by both; degree <= 2 everywhere
            deg = {}
            for e in E:
                for p in e: deg[p] = deg.get(p, 0) + 1
            if any(deg[c] != 2 for c in K):
                continue
            vals.add(Q(E, R) % 3)
        print(f'left={A_} bottom={B_} R={R}: possible Q mod 3 = {sorted(vals)}', flush=True)
