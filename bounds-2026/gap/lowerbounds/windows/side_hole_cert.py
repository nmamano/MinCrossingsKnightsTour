#!/usr/bin/env python3
"""Side-anchored hole lemma (gap/lowerbounds FINDINGS W3).

Board side at x = 0 (no cells with x < 0). Core: 0 <= x < W, 0 <= y < H, degree exactly 2; halo (x in [W, W+1]
or y in [-2,-1] u [H, H+1], x >= 0) degree <= 2; edges with an end in the core. Allowed crossings: only pairs in
the class ALLOW (B: both edges touch column 0; S: both edges touch column 0 or both touch columns <= 1, i.e.
the width-two strip pairs). Any other crossing among core edges is forbidden. Ask for a hole in quarter q of the
unit square [d, d+1] x [c, c+1], c = H // 2. UNSAT = such a hole needs a crossing outside ALLOW nearby.
usage: side_hole_cert.py W H d ALLOW
"""
import sys
from itertools import combinations
from pysat.solvers import Glucose4
sys.path.insert(0, '..')
from check_frac_obstruction import crosses
from w3_quarters import tile, inside, quarters

K8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def E2(a, b): return (a, b) if a < b else (b, a)


def main():
    W, H, d, allow = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    c = H // 2
    core = [(x, y) for x in range(W) for y in range(H)]; cs = set(core)
    edges = sorted({E2(a, (a[0] + dx, a[1] + dy)) for a in core for dx, dy in K8 if a[0] + dx >= 0})
    vid = {e: i + 1 for i, e in enumerate(edges)}
    cl = []; inc = {}
    for e in edges:
        for p in e: inc.setdefault(p, []).append(vid[e])
    for p, l in inc.items():
        for t in combinations(l, 3): cl.append([-x for x in t])
        if p in cs:
            for i in l: cl.append([j for j in l if j != i])
    t0 = lambda e: min(e[0][0], e[1][0]) == 0
    t1 = lambda e: min(e[0][0], e[1][0]) <= 1
    ok = (lambda e, f: t0(e) and t0(f)) if allow == 'B' else (lambda e, f: (t0(e) and t0(f)) or (t1(e) and t1(f)))
    for e, f in combinations(edges, 2):
        if crosses(e, f) and not ok(e, f): cl.append([-vid[e], -vid[f]])
    res = {}
    near = {E2(a, (a[0] + dx, a[1] + dy)) for a in [(x, y) for x in range(0, d + 5) for y in range(c - 3, c + 5)]
            for dx, dy in K8 if a[0] + dx >= 0}
    for q, pt in quarters(d, c).items():
        cov = [e for e in near if inside(tile(e), pt)]
        assert all(e in vid for e in cov)
        S = Glucose4(bootstrap_with=cl + [[-vid[e]] for e in cov], with_proof=True)
        r = S.solve(); res[q] = 'SAT' if r else 'UNSAT'
        if not r:
            base = f'sidehole_W{W}_H{H}_d{d}_{allow}_{q}'
            with open(base + '.cnf', 'w') as f:
                f.write(f'p cnf {len(edges)} {len(cl) + len(cov)}\n')
                for cc in cl + [[-vid[e]] for e in cov]: f.write(' '.join(map(str, cc)) + ' 0\n')
            open(base + '.drup', 'w').write('\n'.join(S.get_proof()) + '\n')
    print(f'W={W} H={H} depth d={d} allow={allow}: hole in quarter of [{d},{d + 1}]x[{c},{c + 1}] ->', res)


if __name__ == '__main__':
    main()
