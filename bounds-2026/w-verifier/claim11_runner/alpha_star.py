"""Largest alpha such that every walk in the width-2 strip graph satisfies
   sum (w - 1/4) >= alpha * (#non-cycle steps) - C,
i.e. no cycle has negative weight under w' = w - 1/4 - alpha*[arc not on the two tight P/P' cycles].
Binary search with exact integer Bellman-Ford (alpha = p/q)."""
import numpy as np
from fractions import Fraction
from strip_dp import build
import networkx as nx
states, adj, W = build(2)
N = len(states)
src, dst, wt = [], [], []
for u in range(N):
    for v, w in adj[u]:
        src.append(u); dst.append(v); wt.append(w)
src = np.array(src); dst = np.array(dst); wt = np.array(wt)
# tight cycles from potential (as strip_constants.py)
INF = 10**15
d = np.full(N, INF, dtype=np.int64); d[0] = 0
for it in range(N + 1):
    cand = np.where(d[src] < INF, d[src] + 4 * wt - 1, INF)
    nd = d.copy(); np.minimum.at(nd, dst, cand)
    if np.array_equal(nd, d): break
    d = nd
red = 4 * wt - 1 + d[src] - d[dst]
G = nx.DiGraph(); G.add_edges_from((int(a), int(b)) for a, b, r in zip(src, dst, red) if r == 0)
cyc = set()
for c in nx.strongly_connected_components(G):
    if len(c) > 1:
        for a in c:
            for b in G.successors(a):
                if b in c: cyc.add((a, b))
nc = np.array([0 if (int(a), int(b)) in cyc else 1 for a, b in zip(src, dst)])
print('cycle arcs', len(cyc))
def ok(alpha):   # True if no negative cycle with weights q*(4w-1) - 4*p*nc  (alpha = p/q)
    p, q = alpha.numerator, alpha.denominator
    ww = q * (4 * wt - 1) - 4 * p * nc
    dist = np.zeros(N, dtype=np.int64)       # virtual source to all
    for it in range(N + 2):
        cand = dist[src] + ww
        nd = dist.copy(); np.minimum.at(nd, dst, cand)
        if np.array_equal(nd, dist): return True, dist
        dist = nd
    return False, None
lo, hi = Fraction(0), Fraction(2)
assert ok(lo)[0]
for _ in range(14):
    mid = (lo + hi) / 2
    if ok(mid)[0]: lo = mid
    else: hi = mid
print('alpha* in [', lo, ',', hi, '] =', float(lo), float(hi))
