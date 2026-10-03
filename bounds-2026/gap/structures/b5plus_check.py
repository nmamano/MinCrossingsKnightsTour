# KT Structures, 2026-10-03 (b5plus_check.py: q3_check.py + per-side Nnear(2) and F' = non-g rows with no p24 port (2,y)-(4,y+-1)).
# Joint-currency strip ledger on tours (BEYOND5 section 9): per side,
# (X3 - rows) + Q3/2 against 2 #g + N_free(2), Q3 = quarter-atom units in local squares x = 0..4, rows of LB r_b.py:
# hole 1, W3 binomial(m-1, 2), X1 1 (a crossing pair whose two tiles share exactly one quarter, counted at it).
import sys, json, inspect
from pathlib import Path
from collections import Counter, defaultdict
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
    tot = Counter(); lines = []
    for sd in range(4):
        own = defaultdict(list)
        for a, b in E:
            a, b = sorted((T[sd](a), T[sd](b)))
            for x, y, k in F.templates[b[0]-a[0], b[1]-a[1]]: own[x+a[0], y+a[1], k].append((a, b))
        def tq(e):
            a, b = e; return {(x+a[0], y+a[1], k) for x, y, k in F.templates[b[0]-a[0], b[1]-a[1]]}
        Q3 = 0
        for x in range(0, 5):
            for y in rows:
                for k in range(4):
                    m = len(own[x, y, k])
                    if m == 0: Q3 += 1
                    elif m >= 3: Q3 += (m-1)*(m-2)//2
                    elif m == 2 and len(tq(own[x, y, k][0]) & tq(own[x, y, k][1])) == 1: Q3 += 1
        sides = out['sides'][sd]; g = sides['g']; Nf = sides['N_free2']; ex = sides['X3_minus_rows']
        p24 = set()
        for a, b in E:
            a, b = sorted((T[sd](a), T[sd](b)))
            if (a[0], b[0]) == (2, 4): p24.add(a[1])
        Fp = sum(1 for y in rows if y not in p24 and not G[sd][y])
        Nnear = sides['N_re'] - Nf
        rec = dict(Fp=Fp, Nnear=Nnear, ex=ex, Q3=Q3, g=g, owned=sides['owned'], Nf=Nf, joint=ex + Q3/2, need_a2c1=2*g + Nf, slack=ex + Q3/2 - 2*g - Nf)
        lines.append(rec); tot.update(rec)
    print(Path(f).name, 'n', n, 'per side (slack, Fp, Nnear):', [(round(l['slack'], 1), l['Fp'], l['Nnear']) for l in lines], 'total', {k: tot[k] for k in ('slack', 'Fp', 'Nnear', 'g', 'Nf')}, flush=True)
