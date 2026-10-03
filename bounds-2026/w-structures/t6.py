import sys
from fold3 import build, comps
from repair import clusters, window_cells
from imbal import imbalance
n = int(sys.argv[1]); t = int(sys.argv[2]); rad = int(sys.argv[3])
h = n // 2
for name, fl in [('noflip', None), ('flip', lambda r, y: h - n // 4 <= y < h)]:
    E, deg = build(n, ts=(t, t, t, t), flip=fl)
    cs, cyc, bad = comps(n, E, deg)
    print(name, [(cl[0], imbalance(n, E, window_cells(n, cl, rad))) for cl in clusters(bad)])
