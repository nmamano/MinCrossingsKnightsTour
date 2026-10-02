#!/usr/bin/env python
"""Fold field with JOG BANDS (KT Lower Bounds F14b) instead of the arch flips.

In every quadrant frame (BL frame coordinates, as in fold_board.field) the cells of the (2,1) region
with -e <= x - y < -e + d get direction (-1,-2), for band start points e = h - 2^j on the left edge
(j = 1..J, 2^J >= h/2).  A band runs from the edge point (0, e) up to the horizontal midline.
Then fold3.build adds the U-turns (no flips).  Returns E like fold3.build.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'w-structures')); sys.path.insert(0, os.path.join(ROOT, 'w-lowerbounds'))
import fold3
from fold_board import field as field0

def band_starts(n, jmin=1):
    h = n // 2
    out, j = [], jmin
    while True:
        out.append(h - 2 ** j)
        if 2 ** j >= h // 2: break
        j += 1
    return out

def make_field(bands, d=1, ts=(1, 1, 1, 1)):
    def field_jog(n, ts=ts, ms=(0, 0, 0, 0)):
        v = field0(n, ts=ts, ms=ms)
        h = n // 2
        for (x, y), dv in list(v.items()):
            # frame of this cell (same rule as fold_board.field)
            lower = y < h; left = x < h
            r = {(True, True): 0, (False, True): 1, (False, False): 2, (True, False): 3}[(left, lower)]
            p = (x, y)
            for _ in range(r):
                p = (p[1], n - 1 - p[0])
            df = dv
            for _ in range(r):           # rotate direction back to the frame
                df = (df[1], -df[0])
            if df != (2, 1): continue
            for e in bands(n):
                if -e <= p[0] - p[1] < -e + d:
                    nd = (-1, -2)
                    for _ in range(r):
                        nd = (-nd[1], nd[0])
                    v[(x, y)] = nd
                    break
        return v
    return field_jog

def build_jog(n, t=1, d=1, jmin=1, flip=None):
    old = fold3.field
    fold3.field = make_field(lambda m: band_starts(m, jmin), d=d, ts=(t, t, t, t))
    try:
        E, deg = fold3.build(n, ts=(t, t, t, t), flip=flip)
    finally:
        fold3.field = old
    return E, deg

if __name__ == '__main__':
    from fold3 import comps
    from kt.core import crossing_list
    for n in [int(a) for a in sys.argv[1:]] or [48, 96]:
        h = n // 2
        for label, (E, deg) in (('no flips', fold3.build(n, ts=(1,) * 4)),
                                ('arch flips', fold3.build(n, ts=(1,) * 4, flip=lambda r, y: h - n // 4 <= y < h)),
                                ('jog bands', build_jog(n))):
            cs, cyc, bad = comps(n, E, deg)
            print(f'n={n} {label:10}: comps {len(cs)} closed {len(cyc)} defects {len(bad)} X {len(crossing_list(E))}'
                  + (f' bands {band_starts(n)}' if label == 'jog bands' else ''))
