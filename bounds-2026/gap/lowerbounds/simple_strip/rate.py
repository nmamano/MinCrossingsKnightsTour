"""Critical rate for an arbitrary row indicator on the row graph: max lam with 4W-4-4*lam*ind >= potential drop."""
import pickle, numpy as np
from fractions import Fraction
G = pickle.load(open('gap/lowerbounds/simple_strip/graph.pkl', 'rb')); R = pickle.load(open('gap/lowerbounds/simple_strip/rows.pkl', 'rb'))
states, nodes, es, vis, tests = G['states'], G['nodes'], G['es'], G['vispairs'], G['tests']
bits = {e: 1 << i for i, e in enumerate(es)}
bnd = R['bnd']; rows = R['rows']; bi = {b: i for i, b in enumerate(bnd)}
S = np.array([bi[u] for u, v, W, m in rows]); D = np.array([bi[v] for u, v, W, m in rows]); Wt = np.array([W for u, v, W, m in rows])
M = [m for u, v, W, m in rows]
def g_of(m, k=0):
    coef, exc = tests[k]
    F = sum(c for e, c in coef.items() if m & bits[e]) % 3
    E = all(m & bits[e] for e in exc)
    V = any(m & v == v for v, a, b, ov in vis[k])
    return int(F != 2 or E or V)
def negcycle(cost):
    """Bellman-Ford from all-zero; return (True, d) or (False, cycle arc list)."""
    n = len(bnd); d = np.zeros(n, dtype=np.int64); pred = -np.ones(n, dtype=np.int64)
    for it in range(n + 1):
        cand = d[S] + cost; nd = d.copy(); np.minimum.at(nd, D, cand)
        if np.array_equal(nd, d): return True, d
        imp = cand < nd[D]  # not used
        # record predecessor arcs
        better = cand == nd[D]
        ch = nd < d
        idx = np.nonzero(better & ch[D])[0]
        pred[D[idx]] = idx
        d = nd
        if it > 60:
            # extract a cycle via pred walk
            x = int(np.nonzero(ch)[0][0]); seen = {}
            path = []
            while x not in seen:
                seen[x] = len(path); a = int(pred[x]); path.append(a); x = int(S[a])
            return False, path[seen[x]:]
    raise RuntimeError
def critical(ind, lam=Fraction(2)):
    ind = np.asarray(ind, dtype=np.int64)
    while True:
        p, q = lam.numerator, lam.denominator
        ok, data = negcycle(q*(4*Wt - 4) - 4*p*ind)
        if ok: return lam, int(data.min())
        num = int((Wt[data] - 1).sum()); den = int(ind[data].sum())
        lam = Fraction(num, den) if den else Fraction(0)
        print('  cycle len', len(data), 'rate <=', lam, flush=True)
if __name__ == '__main__':
    gg = [g_of(m) for m in M]
    print('g:', critical(gg))
