# KT Structures, 2026-10-03. Checks (D*) with collar holes: E >= (BQ + G2/2)/4 + N_re/2 (SHEET 9.5 (b), 13.4).
# G2 = uncovered quarters of collar column-2 squares [2,3] x [j,j+1], j = 3..n-5, all four sides (local frames).
import sys, json
from collections import Counter
from pathlib import Path
import fold_exact_scan as F, chamber_ledger as CL
for f in sys.argv[1:]:
    r = F.run(f); n, ports, changed, other, E, adj = CL.port_data(f)
    T = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])]
    G2 = 0
    for L in T:
        cov = Counter()
        for a, b in E:
            a, b = sorted((L(a), L(b)))
            for x, y, k in F.templates[b[0]-a[0], b[1]-a[1]]: cov[x+a[0], y+a[1], k] += 1
        G2 += sum(cov[2, j, k] == 0 for j in range(3, n-4) for k in range(4))
    N = len(changed)
    print(f"{Path(f).name} n={n} E={r['E']} BQ={r['BQ']} G2={G2} N_re={N}  E-(BQ+G2/2)/4-N_re/2 = {r['E'] - (r['BQ'] + G2/2)/4 - N/2}"
          f"  (T*') BQ+G2/2+2N_re-4n = {r['BQ'] + G2/2 + 2*N - 4*n}", flush=True)
