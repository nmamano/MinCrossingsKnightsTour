"""Greedy band set D (bands at h - D) that removes all chevron loops for SEVERAL n at once."""
import sys; sys.path.insert(0, '.')
from jog_rule import closed_with
ns = [int(a) for a in sys.argv[1:]]
hmin = min(ns) // 2
Ds = []
def score(Ds):
    return sum(closed_with(n, [n // 2 - D for D in Ds])[0] for n in ns)
cur = score(Ds); print('start', cur, flush=True)
while cur > 0:
    best = None
    for D in range(2, hmin - 2):
        if D in Ds: continue
        s = score(sorted(Ds + [D]))
        if best is None or s < best[0]: best = (s, D)
    if best[0] >= cur: print('stuck', cur, Ds); break
    Ds = sorted(Ds + [best[1]]); cur = best[0]
    print('add D', best[1], 'closed', cur, flush=True)
print('final', Ds)
