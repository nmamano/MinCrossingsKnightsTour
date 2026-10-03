"""Is there a potential LINEAR in pending-edge indicators (no-cycle row graph)? LP via OR-Tools GLOP."""
import pickle, sys, numpy as np
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
from ortools.linear_solver import pywraplp
k = int(sys.argv[1]) if len(sys.argv) > 1 else 0
feats = sorted({e for s in bstates for e in s[1]})
print('pending edge universe', len(feats), feats)
fi = {e: i for i, e in enumerate(feats)}
def vec(s):
    v = np.zeros(len(feats)); 
    for e in s[1]: v[fi[e]] = 1
    return v
V = np.array([vec(s) for s in bstates])
cons = {}
for u, v, W, m in rows:
    c = 4*W - 4 - 4*g_of(m, k)
    key = (u, v)
    cons[key] = min(cons.get(key, 99), c)
print('distinct state pairs', len(cons))
solver = pywraplp.Solver.CreateSolver('GLOP')
x = [solver.NumVar(-100, 100, f'c{i}') for i in range(len(feats))]
for (u, v), c in cons.items():
    d = V[u] - V[v]
    solver.Add(c + sum(float(d[i]) * x[i] for i in range(len(feats)) if d[i]) >= 0)
st = solver.Solve()
print('status', st, 'OPTIMAL=0 INFEASIBLE=2')
if st == 0:
    for e, xi in zip(feats, x): print(e, xi.solution_value())
