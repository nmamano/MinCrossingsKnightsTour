# KT Structures 2026-10-04: cycles for row-only (t_r) and column-only (t_c) copies, rectangular boards.
import sys, json
from extend import dup_rows, transpose
from kt.core import num_cycles
r = json.load(open(sys.argv[1])); g0 = r['grid']; a, k = r['per']; T = int(sys.argv[2]) if len(sys.argv) > 2 else 5
print(sys.argv[1])
for tr in range(T + 1):
    row = []
    for tc in range(T + 1):
        g = dup_rows(g0, a, k, tr) if tr else g0
        g = transpose(dup_rows(transpose(g), a, k, tc)) if tc else g
        row.append(num_cycles(g))
    print(' t_r=%d:' % tr, row)
