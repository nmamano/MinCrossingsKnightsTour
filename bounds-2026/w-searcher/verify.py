"""Independent unrolled check of a periodic edge gadget, bottom or left (w-searcher).
Unrolls K periods, adds plain line cells (x+2y=c, '26') outside the band, then checks:
degrees + symmetry, every middle band cell lies on a terminal-to-terminal path (no cycles),
lane-pair rule (lane 2j <-> 2j+1, lane = (c-off)//s), and crossings per period by geometry."""
import os, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kt.core import MI, MJ, seg_cross

def unroll(kind, tpl, K, extra=8):
    rows = [r.split(' ') for r in tpl]
    if kind == 'bottom':
        D, P = len(rows), len(rows[0])
    else:
        P, D = len(rows), len(rows[0])
    adj = defaultdict(set)
    band = set()
    for k in range(K):
        for r, row in enumerate(rows):
            for cidx, code in enumerate(row):
                if kind == 'bottom':
                    u = (cidx + k * P, D - 1 - r)
                else:
                    u = (cidx, P - 1 - r + k * P)
                band.add(u)
                for m in code:
                    d = (MJ[int(m)], -MI[int(m)])
                    adj[u].add((u[0] + d[0], u[1] + d[1]))
    span = K * P
    for a in range(D, D + extra):
        for b in range(-3 * extra - 6, span + 3 * extra + 6):
            u = (b, a) if kind == 'bottom' else (a, b)
            adj[u].add((u[0] + 2, u[1] - 1)); adj[u].add((u[0] - 2, u[1] + 1))
    return adj, band, P, D

def check(kind, tpl, s=4, off=0, K=8):
    adj, band, P, D = unroll(kind, tpl, K)
    along = (lambda u: u[0]) if kind == 'bottom' else (lambda u: u[1])
    depth = (lambda u: u[1]) if kind == 'bottom' else (lambda u: u[0])
    mid = lambda u: 2 * P <= along(u) < (K - 2) * P
    bad = []
    for u in band:
        if not (P <= along(u) < (K - 1) * P):
            continue
        if len(adj[u]) != 2: bad.append(('deg', u))
        for v in adj[u]:
            if u not in adj[v]: bad.append(('asym', u, v))
            if depth(v) < 0: bad.append(('offboard', u, v))
    lane = lambda u: ((u[0] + 2 * u[1]) - off) // s
    terms = sorted(u for u in band if mid(u) and any(depth(v) >= D for v in adj[u]))
    covered = set()
    pairs = []
    for t in terms:
        prev = next(v for v in adj[t] if depth(v) >= D)
        cur = t; path = [t]
        while True:
            nx = [v for v in adj[cur] if v != prev]
            if len(nx) != 1: path = None; break
            prev, cur = cur, nx[0]
            if depth(cur) >= D: break
            path.append(cur)
            if len(path) > 20 * P: path = None; break
        if path is None:
            bad.append(('trace', t)); continue
        covered.update(path)
        pairs.append((t, path[-1]))
    lane_ok = all(lane(a) // 2 == lane(b) // 2 and lane(a) % 2 != lane(b) % 2 for a, b in pairs)
    # cells of the middle periods not on any terminal path -> finite or winding cycle
    inner = [u for u in band if 3 * P <= along(u) < (K - 3) * P]
    uncovered = [u for u in inner if u not in covered]
    def count(a0, a1):
        E = set()
        for u in band:
            if a0 <= along(u) < a1:
                for v in adj[u]:
                    E.add(tuple(sorted([u, v])))
        E = list(E); c = 0
        for i in range(len(E)):
            for j in range(i + 1, len(E)):
                if abs(along(E[i][0]) - along(E[j][0])) <= 5 and seg_cross(*E[i], *E[j]):
                    c += 1
        return c
    X = count(P, (K - 1) * P) - count(P, (K - 2) * P)
    turns = sum(1 for u in band if 2 * P <= along(u) < 3 * P
                and (lambda vs: (vs[0][0] - u[0], vs[0][1] - u[1]) != (u[0] - vs[1][0], u[1] - vs[1][1]))(sorted(adj[u])))
    ok = not bad and lane_ok and not uncovered
    return dict(ok=ok, bad=bad[:5], lane_ok=lane_ok, n_paths=len(pairs), uncovered=len(uncovered),
                X_per_period=X, T_per_period=turns, max_strand_drift=max(abs(along(a) - along(b)) for a, b in pairs))

if __name__ == '__main__':
    from lib import H16a, H16b, VE
    print('H16a', check('bottom', H16a))
    print('H16b', check('bottom', H16b))
    print('VE off0', check('left', VE, off=0))
    print('VE off1', check('left', VE, off=1))
