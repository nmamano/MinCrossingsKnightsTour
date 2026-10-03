# KT Structures, 2026-10-03. BEYOND5 8.2 (P4) data check: is every shallow bad square (local depth x = 1..4 from a
# side, side row y in LB's row range) within 2 rows of a g row, or within 2 rows of a far changed port (N_free(2))?
import sys, json, inspect
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'lowerbounds'/'beyond5'))
import r_b
src = inspect.getsource(r_b.run).replace("out = dict(tour=", "out = dict(G=G, chg=chg, rows=rows, tour=")
ns = dict(vars(r_b)); exec(src, ns); run = ns['run']
import fold_exact_scan as F
for f in sys.argv[1:]:
    out = run(f); n = out['n']; G, chg, rows = out['G'], out['chg'], out['rows']
    grid = json.loads(Path(f).read_text())['tour']
    E = {F.edge((x, n-1-y), (x+F.MOVES[int(v)][1], n-1-y-F.MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
    T = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])]
    res = []
    for sd in range(4):
        cov = Counter()
        for a, b in E:
            a, b = sorted((T[sd](a), T[sd](b)))
            for x, y, k in F.templates[b[0]-a[0], b[1]-a[1]]: cov[x+a[0], y+a[1], k] += 1
        grows = [r for r in rows if G[sd][r]]
        far = {r for r in rows if chg[sd][r] and all(abs(r - t) > 2 for t in grows)}
        bad = [(x, y) for x in range(1, 5) for y in rows if any(cov[x, y, k] != 1 for k in range(4))]
        unc = [(x, y) for x, y in bad if not any(abs(y - t) <= 2 for t in grows) and not any(abs(y - t) <= 2 for t in far)]
        res.append((len(bad), len(unc), unc[:6]))
    print(Path(f).name, 'n', n, 'per side (shallow bad squares, uncovered, examples):', res, flush=True)

# repair test (BEYOND5 8.5): for the uncovered squares, size of free deep bad quarters in their bad-square cluster
def cluster_deep(f, side, sqs):
    import c5_chamber as C5
    n, sel, badsq, dep = C5.selections(f)
    T = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])]
    m = {}
    for i in range(n-1):
        for j in range(n-1):
            cs = [T[side]((i+a, j+b)) for a in (0, 1) for b in (0, 1)]
            m[min(c[0] for c in cs), min(c[1] for c in cs)] = (i, j)
    seen, st = set(), [m[s] for s in sqs]
    while st:
        q = st.pop()
        if q in seen or not badsq.get(q): continue
        seen.add(q); st += [(q[0]+1, q[1]), (q[0]-1, q[1]), (q[0], q[1]+1), (q[0], q[1]-1)]
    deep = [q for q in seen if dep(*q) >= 5]
    return len(seen), sum(badsq[q] for q in deep) - sum(sel[q] for q in deep)
