from fold3 import build, comps
from repair import clusters, window_cells, repair
from imbal import imbalance
n = 48; t = 1
for name, fl in [('both', lambda r, y: r == 0 and 6 <= y < 14),
                 ('even', lambda r, y: r == 0 and 6 <= y < 14 and y % 2 == 0),
                 ('odd', lambda r, y: r == 0 and 6 <= y < 14 and y % 2 == 1)]:
    E, deg = build(n, ts=(t, t, t, t), flip=fl)
    cs, cyc, bad = comps(n, E, deg)
    for cl in clusters(bad, link=3):
        if cl[0][0] <= 2 and 2 <= cl[0][1] <= 18:
            free = window_cells(n, cl, 3)
            r, st = repair(n, E, free, check_only=True, verbose=False, tlimit=20)
            print(name, cl, imbalance(n, E, free), st)
