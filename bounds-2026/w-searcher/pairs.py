"""Pairing of a periodic gadget: list of line pairs (c, c') per period, as (c mod cper, c' - c)."""
from collections import Counter
from verify import unroll
def pairing(kind, tpl, K=10):
    adj, band, P, D = unroll(kind, tpl, K)
    along = (lambda u: u[0]) if kind == 'bottom' else (lambda u: u[1])
    depth = (lambda u: u[1]) if kind == 'bottom' else (lambda u: u[0])
    cper = P if kind == 'bottom' else 2 * P
    out = set()
    for t in sorted(u for u in band if 3 * P <= along(u) < 5 * P and any(depth(v) >= D for v in adj[u])):
        prev = next(v for v in adj[t] if depth(v) >= D); cur = t; n = 0
        while True:
            nx = [v for v in adj[cur] if v != prev]
            prev, cur = cur, nx[0]; n += 1
            if depth(cur) >= D or n > 2000: break
        a, b = t[0] + 2 * t[1], prev[0] + 2 * prev[1]
        lo, hi = min(a, b), max(a, b)
        out.add((lo % cper, hi - lo))
    return sorted(out), cper
