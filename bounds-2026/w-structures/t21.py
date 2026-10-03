import sys
from paste import paste_field
from fold3 import comps
from repair import clusters, window_cells
from imbal import imbalance
n = int(sys.argv[1]); t = 1; h = n // 2
fl = lambda r, y: h - n // 4 <= y < h
def lab(p):
    s = lambda v: 'L' if v < n // 4 else ('H' if v > 3 * n // 4 else 'M')
    return s(p[0]) + s(p[1])
for r in (1, 2, 3):
    for tg in (1, -1, 2, -2):
        E, deg = paste_field(n, t, {r: tg}, fl, hi=h - 4)
        cs, cyc, bad = comps(n, E, deg)
        print('r', r, tg, len(cs), len(cyc), len(bad), sorted((lab(c[0]), imbalance(n, E, window_cells(n, c, 3))) for c in clusters(bad, link=4) if lab(c[0]) in ('HH','HL','LH','LL','MM')))
