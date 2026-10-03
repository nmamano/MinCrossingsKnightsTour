import pickle
G = pickle.load(open('gap/lowerbounds/simple_strip/graph.pkl', 'rb'))
es, vis, tests = G['es'], G['vispairs'], G['tests']
bits = {e: 1 << i for i, e in enumerate(es)}
def g_of(m, k=0):
    coef, exc = tests[k]
    F = sum(c for e, c in coef.items() if m & bits[e]) % 3
    E = all(m & bits[e] for e in exc)
    V = any(m & v == v for v, a, b, ov in vis[k])
    return int(F != 2 or E or V)
NC = pickle.load(open('gap/lowerbounds/simple_strip/nocyc_rows.pkl', 'rb'))
bstates, rows = NC['bstates'], NC['rows']
