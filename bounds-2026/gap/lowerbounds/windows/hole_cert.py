#!/usr/bin/env python3
"""Hole localisation lemma (gap/lowerbounds FINDINGS W3): a hole needs a nearby crossing.

CNF as in w1_cert.py (k x k core, degree exactly 2; width-2 halo, degree <= 2; no crossing between two edges
that touch the core), plus: quarter q of the central unit square is a hole (every edge whose tile contains it
is absent). For k odd the central square is [c, c+1]^2 with c = (k-1)//2 - 1 + ... (we use the square whose
lower-left cell is the centre cell). UNSAT means: every hole has a crossing among edges touching the k x k core.
Overlaps (multiplicity >= 2) need a crossing by the audited tile lemma, so they are not tested.
usage: hole_cert.py k        (writes hole_k{k}_{q}.cnf/.drup for each quarter q)
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
    k = int(sys.argv[1]); c = k // 2
    core = [(x, y) for x in range(k) for y in range(k)]; cs = set(core)
    edges = sorted({E2(a, (a[0] + dx, a[1] + dy)) for a in core for dx, dy in K8})
    vid = {e: i + 1 for i, e in enumerate(edges)}
    cl = []; inc = {}
    for e in edges:
        for p in e: inc.setdefault(p, []).append(vid[e])
    for p, l in inc.items():
        for t in combinations(l, 3): cl.append([-x for x in t])
        if p in cs:
            for i in l: cl.append([j for j in l if j != i])
    for e, f in combinations(edges, 2):
        if crosses(e, f): cl.append([-vid[e], -vid[f]])
    allK8 = {E2(a, (a[0] + dx, a[1] + dy)) for a in [(x, y) for x in range(c - 3, c + 5) for y in range(c - 3, c + 5)]
             for dx, dy in K8}
    res = {}
    for q, pt in quarters(c, c).items():
        cov = [e for e in allK8 if inside(tile(e), pt)]
        assert all(e in vid for e in cov), 'window too small for this quarter'
        extra = [[-vid[e]] for e in cov]
        S = Glucose4(bootstrap_with=cl + extra, with_proof=True)
        r = S.solve(); res[q] = 'SAT' if r else 'UNSAT'
        if not r:
            base = f'hole_k{k}_{q}'
            with open(base + '.cnf', 'w') as f:
                f.write(f'p cnf {len(edges)} {len(cl) + len(extra)}\n')
                for cc in cl + extra: f.write(' '.join(map(str, cc)) + ' 0\n')
            open(base + '.drup', 'w').write('\n'.join(S.get_proof()) + '\n')
    print(f'k={k}: central square [{c},{c + 1}]^2, hole in quarter ->', res)


if __name__ == '__main__':
    main()
