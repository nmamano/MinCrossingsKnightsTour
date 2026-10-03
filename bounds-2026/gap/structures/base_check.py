import sys
sys.path.insert(0, '../../w-structures')
from fold3 import build, comps
for n in (16, 24, 32, 40):
    for ts in ((1,1,1,1), (-1,-1,-1,-1)):
        E, deg = build(n, ts=ts)
        cs, cyc, bad = comps(n, E, deg)
        left = [c for c in cyc if min(p[0] for p in c) == 0 and all(p[0] < n//2 and n//4 - 2 <= p[1] < 3*n//4 + 2 for p in c)]
        print(n, ts, 'comps', len(cs), 'cycles', len(cyc), 'left-mid cycles', len(left), 'defects', len(bad))
