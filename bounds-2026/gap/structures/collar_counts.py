# KT Structures, 2026-10-03. Per-side collar edge counts for (R2) (SHEET 9.4): local left frame, rows 3..n-4.
# m0: col0-col1, n0: col0-col2, m12: col1-col2, p13: ports 1->3, p23: ports 2->3 (non-steep), p24: ports 2->4.
import sys, json
from collections import Counter
from pathlib import Path
import fold_exact_scan as F, barrier_scan, nre_scan
f = sys.argv[1]
grid = json.loads(Path(f).read_text())['tour']; n = len(grid)
E = {F.edge((x, n-1-y), (x+F.MOVES[int(v)][1], n-1-y-F.MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
T = [lambda v: v, lambda v: (n-1-v[0], v[1]), lambda v: (v[1], v[0]), lambda v: (n-1-v[1], v[0])]
_, runs = barrier_scan.scan(f); nr = nre_scan.scan(f)
for si, L in enumerate(T):
    c = Counter(); cov = Counter()
    for a, b in E:
        a, b = sorted((L(a), L(b)))
        for x, y, k in F.templates[b[0]-a[0], b[1]-a[1]]: cov[x+a[0], y+a[1], k] += 1
        if not (3 <= min(a[1], b[1]) and max(a[1], b[1]) <= n-4): continue
        xs = (a[0], b[0])
        key = {(0, 1): 'm0', (0, 2): 'n0', (1, 2): 'm12', (1, 3): 'p13', (2, 3): 'p23', (2, 4): 'p24'}.get(xs)
        if key: c[key] += 1
    r = runs[si]
    c['G2'] = sum(cov[2, j, k] == 0 for j in range(3, n-4) for k in range(4))
    c['G2multi'] = sum(cov[2, j, k] > 1 for j in range(3, n-4) for k in range(4))
    Fv = r.get('frustrated_here', 0); bound = (n-7) - c['p24'] + r.get('bdry_bad', 0)
    lowch = c['p23'] + abs(c['p13'] - c['p24'])
    print(si, dict(c), 'N=', n-6, 'F=', r.get('frustrated_here', 0), 'bad=', r.get('bdry_bad', 0), 'changed=', nr['changed_by_side'].get(si, 0), '| F<=N-p24+bad:', Fv, '<=', bound, '| changed>=p23+|p13-p24|:', lowch)
