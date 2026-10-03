# KT Structures, 2026-10-03. BEYOND5 9: exact shallow-user consumption per side (deep-first selection, claim40 order),
# counted at 1/2 per selected quarter in local squares x = 0..4 of LB rows 8..n-9.
import sys, json
from pathlib import Path
from collections import defaultdict, Counter
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'gap/turnstheory')); sys.path.insert(0, str(ROOT/'gap/verifier'))
from check_hall_v3 import geometry
from claim38_switch import edge, qs
from check import MOVES
for f in sys.argv[1:]:
    grid = json.loads(Path(f).read_text())['tour']; info, cs, atoms = geometry(grid); n = info['n']
    es = {edge((x, n-1-y), (x+MOVES[int(v)][1], n-1-y-MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
    own = defaultdict(list)
    for e in es:
        for q in qs(e): own[q].append(e)
    lookup = {(a[0], a[3]): j for j, a in enumerate(atoms)}
    def payable(q):
        ls = own[q]; m = len(ls)
        if m == 1: return None
        if not m: return lookup['G', q]
        if m >= 3: return lookup['W3', q]
        pair = tuple(sorted(ls)); return lookup.get(('pair', pair), lookup.get(('X1', pair)))
    dep = lambda x, y: min(x, y, n-2-x, n-2-y)
    def squares(c):
        fx, fy, r = c
        return [(n-2-x if fx else x, n-2-y if fy else y) for x, y in [(r, j) for j in range(1, r+1)] + [(i, r) for i in range(r-1, 0, -1)]]
    sub = Counter()
    for c in cs:
        opts = sorted(((-dep(x, y), (x, y, k)) for x, y in squares(c) for k in range(4) if payable((x, y, k)) is not None))
        for d, (x, y, k) in opts[:2]:
            if -d > 4: continue
            loc = [(x, y, 0), (n-2-x, y, 1), (y, x, 2), (n-2-y, x, 3)]
            for lx, ly, sd in loc:
                if lx <= 4 and 8 <= ly <= n-9: sub[sd] += 0.5
    print(Path(f).name, 'shallow consumption per side', [sub[s] for s in range(4)], flush=True)
