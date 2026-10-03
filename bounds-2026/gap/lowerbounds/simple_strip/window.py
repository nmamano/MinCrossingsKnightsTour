"""Window LP: weights alpha_j on cuts c_0..c_{2w+1} around the g-row (row between c_w and c_{w+1}).
maximize t s.t. for all windows: sum_j alpha_j*2kappa(c_j) - 4 g(row) >= t, sum alpha = 1, alpha >= 0. Cutting planes."""
import sys, pickle, numpy as np
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
from ortools.linear_solver import pywraplp
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
k2 = np.array([int(2*K[v][0]) for v in range(len(bstates))], dtype=float)
k = int(sys.argv[1]); w = int(sys.argv[2])
S = np.array([u for u, v, W, m in rows]); D = np.array([v for u, v, W, m in rows])
Gm = np.array([g_of(m, k) for u, v, W, m in rows], dtype=float)
N = len(bstates); L = 2*w + 2
def separate(al):
    f = al[0]*k2.copy(); back = []
    for j in range(1, L):
        cand = f[S] + (-4*Gm if j == w+1 else 0)
        nf = np.full(N, np.inf); np.minimum.at(nf, D, cand)
        # backpointer: an arc achieving the min
        arg = np.full(N, -1); ok = np.isclose(cand, nf[D]); idx = np.nonzero(ok)[0]; arg[D[idx]] = idx
        back.append(arg); f = nf + al[j]*k2
    end = int(np.argmin(f)); val = f[end]
    path = [end]; arcs = []
    for j in range(L-1, 0, -1):
        a = back[j-1][path[-1]]; arcs.append(a); path.append(int(S[a]))
    path = path[::-1]; arcs = arcs[::-1]
    return val, [k2[c] for c in path], Gm[arcs[w]]
solver = pywraplp.Solver.CreateSolver('GLOP')
al = [solver.NumVar(0, 1, f'a{j}') for j in range(L)]; t = solver.NumVar(-100, 100, 't')
solver.Add(sum(al) == 1); solver.Maximize(t)
for it in range(500):
    solver.Solve(); a = np.array([x.solution_value() for x in al]); tv = t.solution_value()
    val, ks, g = separate(a)
    if val >= tv - 1e-7: break
    solver.Add(sum(al[j]*ks[j] for j in range(L)) - 4*g >= t)
print('orient', k, 'w', w, 'iters', it, 'optimal t =', round(tv, 4), 'alpha', np.round(a, 4))
val, ks, g = separate(a)
print('worst window 2kappa at cuts', ks, 'g', g)
# long-range: debt states. potential d from kpot (end-kappa)
d = np.load(f'gap/lowerbounds/simple_strip/kpot_{k}_0.npy')
neg = [s for s in range(N) if d[s] < 0]
# zero-cost cycles among negative-potential states?
import networkx as nx
C = np.array([k2[v] - 4*Gm[j] for j, (u, v) in enumerate(zip(S, D))])
sl = C + d[S] - d[D]
Z = nx.DiGraph(); Z.add_edges_from((int(S[j]), int(D[j])) for j in np.nonzero(sl == 0)[0] if d[S[j]] < 0 and d[D[j]] < 0)
cyc = [c for c in nx.strongly_connected_components(Z) if len(c) > 1 or Z.has_edge(next(iter(c)), next(iter(c)))]
print('tight SCCs inside debt states', [len(c) for c in cyc])
for c in cyc:
    for s in c: print('  debt', d[s], '2kappa', k2[s], bstates[s][1])
