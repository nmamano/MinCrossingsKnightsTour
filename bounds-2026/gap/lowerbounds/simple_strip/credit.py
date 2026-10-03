"""Local quarter credit per square row vs 2+2g."""
import pickle, sys, numpy as np
from collections import Counter, defaultdict
from itertools import combinations
sys.path.insert(0, 'gap/verifier')
from claim37_check import tile
from claim26_certificate import edge
G = pickle.load(open('gap/lowerbounds/simple_strip/graph.pkl', 'rb')); R = pickle.load(open('gap/lowerbounds/simple_strip/rows.pkl', 'rb'))
states, nodes, es, vis, tests = G['states'], G['nodes'], G['es'], G['vispairs'], G['tests']
bits = {e: 1 << i for i, e in enumerate(es)}
def qs(e): return {(x, y, q) for (x, y), h in tile(e) for q in h}
def g_of(m, k):
    coef, exc = tests[k]
    F = sum(c for e, c in coef.items() if m & bits[e]) % 3
    E = all(m & bits[e] for e in exc)
    V = any(m & v == v for v, a, b, ov in vis[k])
    return int(F != 2 or E or V)
def credit(pend, row):
    # pending edges at end of row r=-1 in shifted coords (row r is y=-1); square row -1
    ess = [edge(a, b) for a, b, c in pend]
    mult = Counter(); 
    tq = {e: {q for q in qs(e) if q[1] == row} for e in ess}
    for e in ess: mult.update(tq[e])
    cr = sum(m*(m-1)//2 for m in mult.values())
    for e, f in combinations(ess, 2):
        ov = qs(e) & qs(f)
        if len(ov) == 1 and next(iter(ov))[1] == row: cr += 1
    return cr, mult
bnd = R['bnd']; rows = R['rows']
cr_of = {}
for b in bnd:
    u = nodes[b][0]
    cr_of[b] = credit(states[u][1], -1)[0]
print('credit distribution at boundary states', Counter(cr_of.values()))
h = np.load('gap/verifier/claim42_potential_up.npy')
bad = Counter(); tot = Counter()
for u, v, W, m in rows:
    g = g_of(m, 0)
    d = cr_of[v] - 2 - 2*g
    tot[(g, d)] += 1
print('row arcs by (g, credit-2-2g):', sorted(tot.items()))
# does h relate to credit?
