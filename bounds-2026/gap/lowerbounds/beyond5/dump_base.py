#!/usr/bin/env python3
"""Dump the width-three base graph of joint_free.py (with Q3 attributes) for free_aug.cpp.
File base_<orient>.bin: int32 N, int32 M, then M records of 11 int32:
  src, dst, w (X3 crossings), g (row end only), c0, c1, c2 (changed ports booked on collar rows R, R-1, R-2),
  re (row end), q3 (holes x <= 2, W3 / X1 lower bounds, square row R), sat (column-3 vertex of this cell has model
  degree 2; x = 3 only), u3 (bit mask b=1 r=2 t=4 l=8 of square (3, R) quarters that no model edge covers).
usage: Q3=1 dump_base.py up|down
"""
import os, sys
import numpy as np
assert os.environ.get('Q3') == '1'
import joint_free as J

orient = sys.argv[1]
st, S, D, Wt, G, C0, C1, C2, RE, Q3L, SAT, U3 = J.build(orient)
rec = np.stack([S, D, Wt, G, C0, C1, C2, RE.astype(int), Q3L, SAT, U3], axis=1).astype(np.int32)
with open(f'base_{orient}.bin', 'wb') as f:
    np.array([len(st), len(S)], dtype=np.int32).tofile(f)
    rec.tofile(f)
print('wrote', f'base_{orient}.bin', len(st), len(S))
