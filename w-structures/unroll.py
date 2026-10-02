"""Independent unrolled check of a seam/wall solution (KT Structures, 2026-10-02).
Builds K periods explicitly (band cells from the solution, side cells as straight lines),
then (1) checks degree 2 + symmetry in the middle periods, (2) traces every strand that
enters the band from side 1 in the middle periods and checks where it leaves,
(3) counts crossings per period by brute force geometry (difference of two windows),
(4) counts turns per period."""
from collections import defaultdict
from seam import cell_moves, add, neg, dot
import sys
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
from kt.core import seg_cross


def unroll(st, chosen, K=8, margin=8):
    dirs = cell_moves(st, chosen)
    adj = defaultdict(set)
    band = set()
    for k in range(K):
        for u, ds in dirs.items():
            c = st.shiftc(u, k)
            band.add(c)
            for d in ds:
                adj[c].add(add(c, d))
    # side cells: all cells near the band in the K-period window get their line edges
    cells = set()
    for c in band:
        for dx in range(-margin, margin + 1):
            for dy in range(-margin, margin + 1):
                cells.add((c[0] + dx, c[1] + dy))
    for c in cells:
        sd = st.side(c)
        if sd == 1:
            f = st.f1
        elif sd == 2 and not st.wall:
            f = st.f2
        else:
            continue
        for d in (f, neg(f)):
            v = add(c, d)
            if st.side(v) != 0 or v in band:
                adj[c].add(v)
                if st.side(v) == 0:
                    adj[v]  # band cell already has it
    return adj, band


def check(st, chosen, K=8):
    adj, band = unroll(st, chosen, K)
    mid = lambda c: 2 <= st.canon(c)[1] < K - 2
    bad = []
    for c in band:
        if not mid(c):
            continue
        if len(adj[c]) != 2:
            bad.append(('deg', c, sorted(adj[c])))
        for v in adj[c]:
            if c not in adj[v]:
                bad.append(('asym', c, v))
    # trace strands from side-1 entry terminals in middle periods
    res = []
    ok = True
    for c in sorted(band):
        if not mid(c):
            continue
        for v in adj[c]:
            if st.side(v) == 1:
                prev, cur, n = v, c, 0
                path = [c]
                while st.side(cur) == 0 and n < 10000:
                    nx = [w for w in adj[cur] if w != prev]
                    if len(nx) != 1:
                        break
                    prev, cur = cur, nx[0]
                    path.append(cur); n += 1
                sd_out = st.side(cur)
                last = path[-2]
                if st.wall:
                    l1, l2 = st.lane(c, 1), st.lane(last, 1)
                    good = sd_out == 1 and l1 // 2 == l2 // 2 and l1 % 2 != l2 % 2
                else:
                    l1, l2 = st.lane(c, 1), st.lane(last, 2)
                    good = sd_out == 2 and l2 == l1 + st.shift
                ok &= good
                res.append((c, last, sd_out, l1, l2, good))
    # crossings: edges with >=1 band endpoint, by window of periods
    def edges_in(k0, k1):
        E = set()
        for c in band:
            if k0 <= st.canon(c)[1] < k1:
                for v in adj[c]:
                    E.add(tuple(sorted([c, v])))
        return list(E)
    def count(E):
        n = 0
        for i in range(len(E)):
            for j in range(i + 1, len(E)):
                a, b = E[i], E[j]
                if abs(a[0][0] - b[0][0]) + abs(a[0][1] - b[0][1]) <= 8 and seg_cross(*a, *b):
                    n += 1
        return n
    # crossings involving edges of band cells: count(E[1..K-1]) - count(E[1..K-2]) = per-period
    X = count(edges_in(1, K - 1)) - count(edges_in(1, K - 2))
    turns = 0
    for c in band:
        if st.canon(c)[1] == 3:
            ds = [(v[0] - c[0], v[1] - c[1]) for v in adj[c]]
            if len(ds) == 2 and ds[0] != neg(ds[1]):
                turns += 1
    return dict(bad=bad[:5], strands_ok=ok, n_strands=len(res), X_per_period=X, T_per_period=turns,
                sample=res)
