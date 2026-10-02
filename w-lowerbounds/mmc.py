"""Minimum mean cycle (Howard policy iteration) + exact certificate check."""
from fractions import Fraction
import numpy as np


def prune(adj):
    """Remove nodes with no infinite continuation. Returns kept mask."""
    n = len(adj)
    radj = [[] for _ in range(n)]
    outdeg = [len(a) for a in adj]
    for u in range(n):
        for v, w in adj[u]:
            radj[v].append(u)
    alive = [True] * n
    stack = [u for u in range(n) if outdeg[u] == 0]
    while stack:
        v = stack.pop()
        if not alive[v]:
            continue
        alive[v] = False
        for u in radj[v]:
            if alive[u]:
                outdeg[u] -= 1
                if outdeg[u] == 0:
                    stack.append(u)
    return alive


def howard(adj, alive, iters=1000):
    n = len(adj)
    nodes = [u for u in range(n) if alive[u]]
    ad = {u: [(v, w) for v, w in adj[u] if alive[v]] for u in nodes}
    pol = {u: min(ad[u], key=lambda t: t[1]) for u in nodes}
    for it in range(iters):
        # evaluate policy
        eta = {}
        d = {}
        color = {}
        for s in nodes:
            if s in eta:
                continue
            path = []
            u = s
            while u not in eta and u not in color:
                color[u] = s
                path.append(u)
                u = pol[u][0]
            if u not in eta:
                # found new cycle starting at u
                cyc = path[path.index(u):]
                tot = sum(pol[c][1] for c in cyc)
                m = Fraction(tot, len(cyc))
                eta[u] = m
                d[u] = Fraction(0)
                # assign d along the cycle backwards
                for c in reversed(cyc[1:]):
                    nxt = pol[c][0]
                    # will fill after
                cyc_rev = list(reversed(cyc))
                # d[c] = w(c) - m + d[next]; go backwards from u
                for c in cyc_rev:
                    if c == u:
                        continue
                    v, w = pol[c]
                    eta[c] = m
                    d[c] = w - m + d[v]
                path = path[:path.index(u)]
            for c in reversed(path):
                v, w = pol[c]
                eta[c] = eta[v]
                d[c] = w - eta[v] + d[v]
        changed = False
        for u in nodes:
            bu = pol[u]
            for v, w in ad[u]:
                if eta[v] < eta[u]:
                    pol[u] = (v, w)
                    eta[u] = eta[v]
                    changed = True
            if changed:
                pass
        if not changed:
            for u in nodes:
                for v, w in ad[u]:
                    if eta[v] == eta[u] and w - eta[v] + d[v] < d[u]:
                        pol[u] = (v, w)
                        d[u] = w - eta[v] + d[v]
                        changed = True
        if not changed:
            return min(eta.values()), pol, eta
    raise RuntimeError('no convergence')


def certify(adj, lam, start=0):
    """Exact Bellman-Ford with weights w - lam from start. Returns min dist if no
    negative cycle (then every walk from start of length L has weight >= lam*L + mind)."""
    lam = Fraction(lam)
    p, q = lam.numerator, lam.denominator
    n = len(adj)
    src, dst, wt = [], [], []
    for u in range(n):
        for v, w in adj[u]:
            src.append(u); dst.append(v); wt.append(q * w - p)
    src = np.array(src); dst = np.array(dst); wt = np.array(wt, dtype=np.int64)
    INF = np.iinfo(np.int64).max // 4
    dist = np.full(n, INF, dtype=np.int64)
    dist[start] = 0
    for it in range(n + 1):
        cand = np.where(dist[src] < INF, dist[src] + wt, INF)
        nd = dist.copy()
        np.minimum.at(nd, dst, cand)
        if np.array_equal(nd, dist):
            return Fraction(int(dist[dist < INF].min()), q), it
        dist = nd
    return None, n
