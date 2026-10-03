"""Validate on saved closed tours: (1) 2X_sigma = 2n + 6 + sum of kappa terms (exact side identity);
(2) G_sigma <= X_sigma - n + 7 with UP on rows < n/2 and DOWN on rows >= n/2."""
import sys, json, glob
from collections import Counter
from itertools import combinations
sys.path.insert(0, 'gap/verifier'); sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from claim37_check import tile
from check_cut_certificate import cross, edge, g_value
def tq(e): return [(x, y, q) for (x, y), h in tile(e) for q in h]
for f in sorted(glob.glob('w-verifier/claim16_runner/tour*.json')):
    data = json.load(open(f)); n = max(v[0][0] for v in data) + 1
    E = {edge(tuple(v[0]), tuple(u)) for v in data for u in v[1]}
    assert len(E) == n*n
    for side in range(4):
        T = [lambda p: p, lambda p: (n-1-p[0], p[1]), lambda p: (p[1], p[0]), lambda p: (n-1-p[1], p[0])][side]
        Es = {edge(T(a), T(b)) for a, b in E}
        S = [e for e in Es if min(e[0][0], e[1][0]) <= 1]
        X = sum(cross(a, b) for a, b in combinations(S, 2))
        Q = {e: tq(e) for e in S}
        m = Counter(q for e in S for q in Q[e])
        X1 = sum(1 for a, b in combinations(S, 2) if len(set(Q[a]) & set(Q[b])) == 1)
        H0 = sum(1 for y in range(n-1) for q in 'BRTL' if m[(0, y, q)] == 0)
        col1 = sum(abs(m[(1, y, q)] - 1) for y in range(n-1) for q in 'BRTL')       # = H1 + exc1
        W3 = sum((v-1)*(v-2)//2 for (x, y, q), v in m.items() if x <= 1 and v >= 1)
        C2 = sum(v*(v-1)//2 for (x, y, q), v in m.items() if x >= 2)
        c = sum(1 for e in S if {e[0][0], e[1][0]} == {1, 2})
        kap = H0 + col1/2 + W3 + C2 + X1 + c
        # strong count
        G = 0
        for r in range(n):
            sign = 1 if r < n//2 else -1
            mask = frozenset(edge((a[0], a[1]-r), (b[0], b[1]-r)) for a, b in S if min(a[1], b[1]) <= r <= max(a[1], b[1]))
            G += g_value(mask, sign)
        print(f'{f.split("/")[-1]} n={n} side {side}: X={X} 2X-2n-6={2*X-2*n-6} kappa_sum={kap} G={G} X-n+7-G={X-n+7-G}')
