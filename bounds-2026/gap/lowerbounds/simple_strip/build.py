"""S1: rebuild the Claim 42 mask graph (verifier code path) and save arrays for potential analysis.
Run from research root: .venv/bin/python gap/lowerbounds/simple_strip/build.py
"""
import sys, pickle
from itertools import combinations, product
import numpy as np
sys.path.insert(0, 'gap/verifier')
from claim26_certificate import transitions, edge, cross, TERMS, EXC
from claim37_check import tile

def qs(e): return {(x, y, q) for (x, y), h in tile(e) for q in h}
states = [(0, ())]; ids = {states[0]: 0}; adj = []
for s in states:
    row = {}
    for t, w, w0 in transitions(s):
        if t not in ids: ids[t] = len(states); states.append(t)
        row[ids[t]] = w
    adj.append(list(row.items()))
universe = set()
for x, y, xx, yy in product(range(4), range(-2, 3), range(4), range(-2, 3)):
    if min(x, xx) < 2 and min(y, yy) <= 0 <= max(y, yy) and sorted((abs(x-xx), abs(y-yy))) == [1, 2]: universe.add(edge((x, y), (xx, yy)))
es = sorted(universe); bits = {e: 1 << i for i, e in enumerate(es)}
def mask(edges):
    z = 0
    for e in edges: z |= bits[e]
    return z
tests = []; vispairs = []
for sign in (1, -1):
    tr = lambda p: (p[0], sign*p[1])
    tests.append(({edge(tr(a), tr(b)): v for a, b, v in TERMS}, {edge(tr(a), tr(b)) for a, b in EXC}))
    pairs = []
    for a, b in combinations(es, 2):
        ov = qs(a) & qs(b)
        if len(ov) == 2 and any(x in (1, 2, 3) and y == (0 if sign == 1 else -1) for x, y, q in ov) and not (any(x == 0 for x, y in a) and any(x == 0 for x, y in b)):
            pairs.append((bits[a] | bits[b], a, b, sorted(ov)))
    vispairs.append(pairs)
pm = []; shifted = []
for col, pend in states:
    pm.append(mask(edge(a, b) for a, b, c in pend))
    shifted.append(mask(edge((a[0], a[1]+1), (b[0], b[1]+1)) for a, b, c in pend) if col == 0 else 0)
def flags(m):
    out = []
    for (coef, exc), vv in zip(tests, vispairs):
        F = sum(c for e, c in coef.items() if m & bits[e]) % 3
        E = all(m & bits[e] for e in exc)
        V = any(m & v == v for v, a, b, ov in vv)
        out.append((F, int(E), int(V)))
    return out
nodes = [(u, 0) for u, s in enumerate(states) if s[0] == 0]; idx = {s: i for i, s in enumerate(nodes)}
src = []; dst = []; weights = []; rowmask = []
for i, (u, seen) in enumerate(nodes):
    for v, w in adj[u]:
        final = states[v][0] == 0; whole = seen | pm[u] | (shifted[v] if final else pm[v]); key = (v, 0 if final else whole)
        if key not in idx: idx[key] = len(nodes); nodes.append(key)
        src.append(i); dst.append(idx[key]); weights.append(w); rowmask.append(whole if final else -1)
print('mask graph', len(nodes), len(src))
pickle.dump(dict(states=states, nodes=nodes, src=src, dst=dst, w=weights, rowmask=rowmask, es=es, vispairs=vispairs, tests=tests),
            open('gap/lowerbounds/simple_strip/graph.pkl', 'wb'))
