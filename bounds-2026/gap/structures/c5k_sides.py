# KT Structures, 2026-10-03. BEYOND5 section 10: (C5-K) per side. Units: g row 4, far changed port 2 (d0 = 2),
# K candidate -2, side row demand 1 (LB rows 8..n-9). K = lost + deficient (side of the owned g row, r_b.py rule)
# + shallow users (retained, < 2 deep payable quarters; side of their first selected shallow quarter, deep-first
# selection as in shallow_sub.py). BQx is global (deep squares), reported separately. F = frustrated rows (9.1).
import sys, json, inspect
from pathlib import Path
from collections import Counter, defaultdict
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'lowerbounds'/'beyond5'))
import r_b, barrier_scan
src = inspect.getsource(r_b.run).replace("out = dict(tour=", "out = dict(G=G, chg=chg, rows=rows, cs=cs, payable=payable, squares=squares, tour=")
ns = dict(vars(r_b)); exec(src, ns); run = ns['run']
for f in sys.argv[1:]:
    out = run(f); n = out['n']; G, rows, cs = out['G'], out['rows'], out['cs']
    payable, squares = out['payable'], out['squares']
    dep = lambda x, y: min(x, y, n-2-x, n-2-y)
    su = Counter(); nsu = 0
    for c in cs:
        opts = sorted(((-dep(x, y), (x, y, k)) for x, y in squares(c) for k in range(4) if payable((x, y, k)) is not None))
        if len(opts) < 2 or -opts[1][0] >= 5: continue   # deficient (counted through ownership) or two deep quarters
        nsu += 1
        x, y, k = next(q for d, q in opts[:2] if -d <= 4)
        sd = min(range(4), key=lambda s: [x, n-2-x, y, n-2-y][s])
        su[sd] += 1
    _, runs = barrier_scan.scan(f)
    tot = Counter(); recs = []
    for sd in range(4):
        s = out['sides'][sd]; g = s['g']; Nf = s['N_free2']; K = s['owned'] + su[sd]
        near = sum(1 for r in rows if not G[sd][r] and any(G[sd].get(t) for t in range(r-2, r+3)))
        rec = dict(rows=len(rows), F=runs[sd].get('frustrated_here', 0), g=g, owned=s['owned'], SU=su[sd], K=K, Nf=Nf,
                   near=near, Nnear=s['N_re'] - Nf, bal=4*g + 2*Nf - 2*K - len(rows))
        recs.append(rec); tot.update(rec)
    print(Path(f).name, 'n', n, 'SU', nsu)
    for sd, r in enumerate(recs): print('  side', sd, r)
    print('  total', dict(tot), ' (bal + BQx)/n needs >= 0: bal/n =', round(tot['bal']/n, 2), flush=True)
