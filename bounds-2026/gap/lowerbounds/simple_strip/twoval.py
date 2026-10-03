"""Is there a two-valued potential psi in {0, A} for cost 2kappa-4g (alpha mix)? 2-SAT by propagation."""
import sys, pickle, numpy as np
from collections import defaultdict
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
k2 = np.array([int(2*K[v][0]) for v in range(len(bstates))])
k = int(sys.argv[1]); al = float(sys.argv[2])
arcs = [(u, v, al*k2[u] + (1-al)*k2[v] - 4*g_of(m, k)) for u, v, W, m in rows]
for A in (2, 3, 4, 5, 6, 8, 12):
    one = set(); zero = set(); imp = defaultdict(list); bad = False
    for u, v, c in arcs:
        if c < 0:
            if -c > A or u == v: bad = True; break
            one.add(u); zero.add(v)
        elif c < A: imp[v].append(u)   # x_v -> x_u
    if bad: print('A', A, 'impossible (deficit > A)'); continue
    # close 'one' under implications x_v -> x_u
    stack = list(one); 
    while stack:
        v = stack.pop()
        for u in imp[v]:
            if u not in one: one.add(u); stack.append(u)
    print('A', A, 'conflict states', len(one & zero), 'forced one', len(one), 'forced zero', len(zero))
