# KT Structures 2026-10-04: cycles and T - 8n of the band copies t = 0..tmax of a PER solution (no merge).
# usage: cyc.py file.json [tmax]
import sys, json
from extend import dup_rows, transpose
from kt.core import edges, num_turns, num_cycles
r = json.load(open(sys.argv[1])); g0 = r['grid']; a, k = r['per']; tmax = int(sys.argv[2]) if len(sys.argv) > 2 else 8
out = []
for t in range(tmax + 1):
    g = transpose(dup_rows(transpose(dup_rows(g0, a, k, t)), a, k, t)) if t else g0
    assert len(edges(g)) == len(g) ** 2
    out.append(f'n={len(g)}:{num_turns(g) - 8 * len(g)}/{num_cycles(g)}c')
print(sys.argv[1], ' '.join(out))
