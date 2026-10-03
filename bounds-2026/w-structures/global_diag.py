"""Fold field (t odd, arch flips) + free diagonal bands (corner->centre) + defect windows; CP-SAT single cycle."""
import sys, time, json
from fold3 import build, comps
from repair import repair, clusters, window_cells
from global_strip import to_grid
from kt.core import validate, num_crossings, num_turns
n = int(sys.argv[1]); W = int(sys.argv[2]); t = int(sys.argv[3]); tl = float(sys.argv[4]); rad = int(sys.argv[5]) if len(sys.argv) > 5 else 3
h = n // 2
E, deg = build(n, ts=(t, t, t, t), flip=lambda r, y: h - n // 4 <= y < h)
cs, cyc, bad = comps(n, E, deg)
free = set()
for cl in clusters(bad, link=4):
    free |= window_cells(n, cl, rad)
for x in range(n):
    for y in range(n):
        if abs(y - x) <= W or abs(x + y - (n - 1)) <= W:
            free.add((x, y))
print('n', n, 'free cells', len(free), 'components before', len(cs), flush=True)
t0 = time.time()
E2, st = repair(n, E, free, threads=2, tlimit=tl, max_rounds=300, hint=set(E))
print('status', st, 'time', round(time.time() - t0), flush=True)
if E2:
    g = to_grid(n, E2)
    X = num_crossings(g)
    print('n', n, 'valid', validate(g), 'X', X, 'X/n %.3f' % (X / n), 'T', num_turns(g), flush=True)
    json.dump([' '.join(r) for r in g], open(f'tours/diag_n{n}_W{W}.json', 'w'))
