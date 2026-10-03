"""Row graph WITHOUT the forest (no-cycle) condition: state = pending edge set only. Critical rate for g (UP)."""
import sys, numpy as np
from collections import Counter
from itertools import combinations
sys.path.insert(0, 'gap/verifier'); sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from claim26_certificate import edge, cross, TERMS, EXC
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
def trans(state):
    x, pending = state
    p = (x, 0)
    incoming = [e for e in pending if e[1] == p]; keep = [e for e in pending if e[1] != p]
    if len(incoming) > 2: return
    options = [(p, (xx, dy)) for xx in range(4) for dy in (1, 2) if sorted((abs(xx-x), dy)) == [1, 2] and min(x, xx) < 2]
    needs = [2-len(incoming)] if x < 2 else range(3-len(incoming))
    for count in needs:
        for chosen in combinations(options, count):
            load = Counter(e[1] for e in keep); load.update(b for a, b in chosen)
            if any(v > 2 for v in load.values()): continue
            result = keep + list(chosen)
            pairs = [(f, e) for f in chosen for e in keep] + list(combinations(chosen, 2))
            w = sum(cross(a, b) for a, b in pairs)
            shift = int(x == 3)
            yield ((x+1) % 4, tuple(sorted(((a[0], a[1]-shift), (b[0], b[1]-shift)) for a, b in result))), w, chosen
# row-level: from boundary state, do 4 cells; track mask of edges touching row 0
start = (0, ())
bstates = [start]; bid = {start: 0}; rows = []
def bm(edges, sh):
    return sum(bits[edge((a[0], a[1]+sh), (b[0], b[1]+sh))] for a, b in edges)
for s in bstates:
    stack = [(s, 0, bm(s[1], 0))]
    while stack:
        st, W, m = stack.pop()
        for t, w, ch in trans(st):
            if t[0] == 0:
                mm = m | bm(ch, 0) | bm(t[1], 1)
                if t not in bid: bid[t] = len(bstates); bstates.append(t)
                rows.append((bid[s], bid[t], W + w, mm))
            else:
                stack.append((t, W + w, m | bm(ch, 0)))
print('no-cycle boundary states', len(bstates), 'row arcs', len(rows), flush=True)
pickle.dump(dict(bstates=bstates, rows=rows), open('gap/lowerbounds/simple_strip/nocyc_rows.pkl', 'wb'))
import rate
rate.bnd = list(range(len(bstates)))
rate.S = np.array([u for u, v, W, m in rows]); rate.D = np.array([v for u, v, W, m in rows]); rate.Wt = np.array([W for u, v, W, m in rows])
for k in (0, 1):
    print('orient', k, 'critical', rate.critical([g_of(m, k) for u, v, W, m in rows]))
