"""Independent check of a periodic gadget: unroll K periods of the bottom strip on a band with
lines above, then check degrees, trace paths between terminals, check lane pairing, and count
crossings per period by brute force geometry (difference between K and K-2 periods, middle part)."""
from collections import defaultdict
from .core import MI, MJ, seg_cross

def unroll_bottom(tpl, K, s=4, off=0, extra_rows=6):
    rows = [r.split(' ') for r in tpl]
    D, P = len(rows), len(rows[0])
    adj = defaultdict(set)
    W = K * P
    for k in range(K):
        for r, row in enumerate(rows):
            y = D - 1 - r
            for x0, code in enumerate(row):
                x = x0 + k * P
                for m in code:
                    d = (MJ[int(m)], -MI[int(m)])
                    adj[(x, y)].add((x + d[0], y + d[1]))
    # line cells above
    for y in range(D, D + extra_rows):
        for x in range(-2 * extra_rows - 4, W + 4):
            adj[(x, y)].add((x + 2, y - 1)); adj[(x, y)].add((x - 2, y + 1))
    return adj, P, D, W

def check_bottom(tpl, K=6, s=4, off=0):
    adj, P, D, W = unroll_bottom(tpl, K, s, off)
    # symmetry + degree in the middle periods
    bad = []
    for k in range(1, K - 1):
        for x in range(k * P, (k + 1) * P):
            for y in range(D):
                u = (x, y)
                if len(adj[u]) != 2: bad.append(('deg', u, adj[u]))
                for v in adj[u]:
                    if u not in adj[v]: bad.append(('asym', u, v))
                    if v[1] < 0: bad.append(('offboard', u, v))
    # trace paths starting at terminals (row D-1 cells, whose up-edge goes to (x-2, D))
    lane = lambda u: ((u[0] + 2 * u[1]) - off) // s
    pairs = []
    seen = set()
    for x in range(P, (K - 1) * P):
        t = (x, D - 1)
        if t in seen: continue
        prev, cur = (x - 2, D), t
        path = [t]
        steps = 0
        while True:
            nxts = [v for v in adj[cur] if v != prev]
            if len(nxts) != 1: break
            prev, cur = cur, nxts[0]
            path.append(cur)
            steps += 1
            if cur[1] >= D or steps > 10 * P * K: break
        end = path[-2] if cur[1] >= D else None
        seen.add(t)
        if end is not None: seen.add(end)
        pairs.append((t, end, len(path)))
    lane_ok = all(e is not None and lane(t) // 2 == lane(e) // 2 and lane(t) % 2 != lane(e) % 2 for t, e, _ in pairs)
    # crossings: count crossings among edges with at least one endpoint in rows < D within x-window
    def count(x0, x1):
        E = set()
        for (x, y), nb in adj.items():
            if x0 <= x < x1 and 0 <= y < D:
                for v in nb:
                    E.add(tuple(sorted([(x, y), v])))
        E = list(E)
        c = 0
        for i in range(len(E)):
            for j in range(i + 1, len(E)):
                if abs(E[i][0][0] - E[j][0][0]) <= 4 and seg_cross(*E[i], *E[j]):
                    c += 1
        return c
    per_period = count(P, (K - 1) * P) - count(P, (K - 2) * P)
    cycles = 0
    return dict(bad=bad[:5], lane_ok=lane_ok, n_paths=len(pairs), crossings_per_period=per_period,
                sample=[(t, e) for t, e, _ in pairs[:8]])
