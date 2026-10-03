import json, sys
from paste import paste_field
from fold3 import comps
from repair import clusters, window_cells
from imbal import imbalance
n = 48; h = n // 2
fl = lambda r, y: h - n // 4 <= y < h
def lab(p):
    s = lambda v: 'L' if v < n // 4 else ('H' if v > 3 * n // 4 else 'M')
    return s(p[0]) + s(p[1])
L = json.load(open(sys.argv[1]))
for i, tp in enumerate(L):
    cells = {tuple(map(int, k.split(','))): [tuple(m) for m in v] for k, v in tp['cells'].items()}
    for tb in (1, 0, -1, 2):
        E, deg = paste_field(n, None, {0: cells}, fl, hi=h - 4, ts=(tb, 1, 1, 1))
        cs, cyc, bad = comps(n, E, deg)
        cb = [c for c in cyc if any(p[0] < h and p[1] < h for p in c)]
        imb = [imbalance(n, E, window_cells(n, c, 3)) for c in clusters(bad, link=4) if lab(c[0]) == 'LL']
        print(i, tp['XT'], 'tBL', tb, 'closed', len(cb), 'imb', imb)
