import sys
from fold3 import build, comps
from repair import clusters, window_cells, repair
n = int(sys.argv[1]); t = int(sys.argv[2]); rad = int(sys.argv[3])
h = n // 2
E, deg = build(n, ts=(t, t, t, t), flip=lambda r, y: h - n // 4 <= y < h)
cs, cyc, bad = comps(n, E, deg)
cls = clusters(bad)
print('clusters', len(cls))
for cl in cls:
    free = window_cells(n, cl, rad)
    res, st = repair(n, E, free, check_only=True, verbose=False, tlimit=30)
    print(cl[0], len(cl), 'window', len(free), st, flush=True)
