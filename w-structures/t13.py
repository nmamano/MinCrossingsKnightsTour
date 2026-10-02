import sys
from fold3 import build, comps
from repair import clusters, window_cells, repair
from imbal import imbalance
from kt.core import crossing_list
n = int(sys.argv[1]); t = 1; h = n // 2; q = n // 4
def lab(p):
    s = lambda v: 'L' if v < n // 4 else ('H' if v > 3 * n // 4 else 'M')
    return s(p[0]) + s(p[1])
for name, fl in [('both lower', lambda r, y: h - q <= y < h),
                 ('even lower', lambda r, y: h - q <= y < h and y % 2 == 0),
                 ('odd lower', lambda r, y: h - q <= y < h and y % 2 == 1),
                 ('even lower+odd upper', lambda r, y: (h - q <= y < h and y % 2 == 0) or (h <= y < h + q and y % 2 == 1)),
                 ]:
    E, deg = build(n, ts=(t, t, t, t), flip=fl)
    cs, cyc, bad = comps(n, E, deg)
    X = len(crossing_list(E))
    cl = clusters(bad, link=3)
    print(name, 'X', X, 'comps', len(cs), 'cycles', len(cyc), 'bad', len(bad), sorted((lab(c[0]), imbalance(n, E, window_cells(n, c, 3))) for c in cl))
