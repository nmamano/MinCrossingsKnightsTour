import sys
from fold3 import build, comps
from repair import clusters, window_cells
from imbal import imbalance
n = 48
def lab(p):
    s = lambda v: 'L' if v < n // 4 else ('H' if v > 3 * n // 4 else 'M')
    return s(p[0]) + s(p[1])
for ts in [(1, 1, 1, 1), (2, 1, 1, 1), (1, 2, 1, 1)]:
    for ms in [(0, 0, 0, 0), (1, 0, 0, 0), (0, 1, 0, 0), (2, 0, 0, 0), (0, 0, 0, 1)]:
        E, deg = build(n, ts=ts, ms=ms)
        cs, cyc, bad = comps(n, E, deg)
        out = sorted((lab(cl[0]), imbalance(n, E, window_cells(n, cl, 3))) for cl in clusters(bad, link=4))
        print(ts, ms, ' '.join(f'{a}:{b}' for a, b in out))
