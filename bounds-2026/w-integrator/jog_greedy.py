import sys, time
sys.path.insert(0, '.')
import fold_jog as J
import fold3
from fold3 import comps
def closed_with(n, bands, d=1):
    old = fold3.field
    fold3.field = J.make_field(lambda m: bands, d=d)
    try:
        E, deg = fold3.build(n, ts=(1,) * 4)
    finally:
        fold3.field = old
    cs, cyc, bad = comps(n, E, deg)
    return len(cyc), len(bad)

n = int(sys.argv[1]); h = n // 2
bands = []
cur = closed_with(n, bands)[0]
print('start closed', cur, flush=True)
while cur > 0:
    best = None
    for e in range(3, h - 1):
        if e in bands: continue
        c, b = closed_with(n, sorted(bands + [e]))
        if best is None or (c, b) < best[0]: best = ((c, b), e)
    if best[0][0] >= cur: print('stuck', cur, bands); break
    bands = sorted(bands + [best[1]]); cur = best[0][0]
    print('add', best[1], '(h -', h - best[1], ') closed', cur, 'defects', best[0][1], flush=True)
print('final', bands, [h - e for e in bands])
