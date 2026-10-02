import sys
from fold3 import build, comps
from repair import clusters, window_cells, repair
from imbal import imbalance
n = 48; t = 1
h = n // 2
for name, fl in [('both on left seg', lambda r, y: r == 0 and 16 <= y < 22),
                 ('even only', lambda r, y: r == 0 and 16 <= y < 22 and y % 2 == 0),
                 ('odd only', lambda r, y: r == 0 and 16 <= y < 22 and y % 2 == 1)]:
    E, deg = build(n, ts=(t, t, t, t), flip=fl)
    cs, cyc, bad = comps(n, E, deg)
    cls = [cl for cl in clusters(bad, link=3) if any(p[0] <= 2 and 10 <= p[1] <= 28 for p in cl)]
    for cl in cls:
        out = [cl]
        for rad in (3, 5):
            free = window_cells(n, cl, rad)
            r, st = repair(n, E, free, check_only=True, verbose=False, tlimit=30)
            out.append((rad, imbalance(n, E, free), st))
        print(name, out, flush=True)
