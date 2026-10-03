import sys
from fold3 import build, comps
from repair import clusters, window_cells
from imbal import imbalance
from kt.core import crossing_list
n = 48; t = 1; rad = 3
h = n // 2
for name, fl in [('even only on left seg', lambda r, y: r == 0 and 8 <= y < 16 and y % 2 == 0),
                 ('odd only on left seg', lambda r, y: r == 0 and 8 <= y < 16 and y % 2 == 1),
                 ('both on left seg', lambda r, y: r == 0 and 8 <= y < 16)]:
    E, deg = build(n, ts=(t, t, t, t), flip=fl)
    cs, cyc, bad = comps(n, E, deg)
    print(name, 'X', len(crossing_list(E)), [(cl[0], imbalance(n, E, window_cells(n, cl, rad))) for cl in clusters(bad)])
