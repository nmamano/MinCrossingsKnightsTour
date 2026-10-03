import sys
from fold3 import build, comps
from kt.core import crossing_list
t = int(sys.argv[1])
for n in (48, 96, 144):
    h = n // 2
    E, deg = build(n, ts=(t, t, t, t), flip=lambda r, y: h - n // 4 <= y < h)
    cs, cyc, bad = comps(n, E, deg)
    X = len(crossing_list(E))
    print(n, 'X', X, 'comps', len(cs), 'cycles', len(cyc), 'bad', len(bad))
    if n == 48:
        print([(p, deg[p]) for p in bad])
