import sys, ast
from fold3 import build, comps
from kt.core import crossing_list
n = int(sys.argv[1]); t = int(sys.argv[2])
h = n // 2
for name, fl in [('none', None),
                 ('flip upper-mid quarter', lambda r, y: h <= y < h + n // 4),
                 ('flip lower-mid quarter', lambda r, y: h - n // 4 <= y < h)]:
    E, deg = build(n, ts=(t, t, t, t), flip=fl)
    cs, cyc, bad = comps(n, E, deg)
    X = len(crossing_list(E))
    print(name, 't', t, 'X', X, 'X/n %.3f' % (X / n), 'comps', len(cs), 'cycles', len(cyc), 'bad', len(bad), sorted(len(c) for c in cs)[-8:])
