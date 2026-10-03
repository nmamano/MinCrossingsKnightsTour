"""Check sum_r kappa(r) = 2X - 2(rows) up to a telescoping term: kappa(v) - (2W-2) must be a potential difference on every arc."""
import sys, pickle, numpy as np
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
S = np.array([u for u, v, W, m in rows]); D = np.array([v for u, v, W, m in rows])
C = np.array([int(2*K[v][0]) - (4*W - 4) for u, v, W, m in rows])   # in half units
# Solve phi by BFS over undirected graph and check consistency
import collections
phi = {0: 0}; q = collections.deque([0]); adj = collections.defaultdict(list)
for j, (u, v) in enumerate(zip(S, D)): adj[int(u)].append((int(v), int(C[j]))); adj[int(v)].append((int(u), -int(C[j])))
while q:
    x = q.popleft()
    for y, c in adj[x]:
        # c = phi(x) - phi(y) for arc x->y ; reversed stored with -c meaning phi(x)-phi(y) = -c... handle uniformly
        if y not in phi: phi[y] = phi[x] - c; q.append(y)
bad = sum(1 for j in range(len(S)) if phi[int(S[j])] - phi[int(D[j])] != C[j])
print('states', len(phi), 'inconsistent arcs', bad)
P = np.array([phi[i] for i in range(len(bstates))])
print('telescoping term range (half units)', P.min(), P.max())
np.save('gap/lowerbounds/simple_strip/kid_phi.npy', P)
