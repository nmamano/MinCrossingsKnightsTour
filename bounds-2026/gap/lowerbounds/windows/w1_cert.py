#!/usr/bin/env python3
"""W1 certificate: CNF + DRUP proof that every crossing-free window has a fold-stack centre.

CNF over edge variables (knight edges with an end in the k x k core, other end in core or halo of width 2):
core degree exactly 2, halo degree <= 2 (direct cardinality clauses, no auxiliary variables), no two
crossing edges that both touch the core, and for every fold-stack map of the central s x s block a clause
saying the centre differs from it. No-cycle constraints are NOT used (a relaxation, so UNSAT is stronger).
Solver Glucose 4 (pysat) writes a DRUP proof; check it with w-lowerbounds/check_drup.py.
usage: w1_cert.py k b       (writes w1cert_k{k}_b{b}.cnf / .drup)
"""
import sys
from itertools import combinations
from pysat.solvers import Glucose4
sys.path.insert(0, '..')
from check_frac_obstruction import crosses
from w1_count_stacks import maps

K8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def E2(a, b): return (a, b) if a < b else (b, a)


def main():
    k, b = int(sys.argv[1]), int(sys.argv[2])
    s = k - 2 * b
    core = [(x, y) for x in range(k) for y in range(k)]; cs = set(core)
    edges = sorted({E2(a, (a[0] + dx, a[1] + dy)) for a in core for dx, dy in K8})
    vid = {e: i + 1 for i, e in enumerate(edges)}
    cl = []
    inc = {}
    for e in edges:
        for p in e: inc.setdefault(p, []).append(vid[e])
    for p, l in inc.items():
        for t in combinations(l, 3): cl.append([-x for x in t])            # at most 2
        if p in cs:
            for i in l: cl.append([j for j in l if j != i])                 # at least 2
    for e, f in combinations(edges, 2):
        if crosses(e, f): cl.append([-vid[e], -vid[f]])
    cen = [(x, y) for x in range(s) for y in range(s)]   # map order of w1_count_stacks
    nmaps = 0
    for m in maps(s):
        lits = []
        for (x, y), ds in zip(cen, m):
            p = (x + b, y + b)
            for d in ds: lits.append(-vid[E2(p, (p[0] + d[0], p[1] + d[1]))])
        cl.append(lits); nmaps += 1
    base = f'w1cert_k{k}_b{b}'
    with open(base + '.cnf', 'w') as f:
        f.write(f'p cnf {len(edges)} {len(cl)}\n')
        for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
    S = Glucose4(bootstrap_with=cl, with_proof=True)
    res = S.solve()
    print(f'k={k} b={b}: {len(edges)} vars, {len(cl)} clauses, {nmaps} fold-stack maps excluded -> '
          f'{"SAT (a non-fold-stack centre exists)" if res else "UNSAT"}')
    if not res:
        open(base + '.drup', 'w').write('\n'.join(S.get_proof()) + '\n')
    else:
        model = set(x for x in S.get_model() if x > 0)
        print('  centre edges:', [e for e in edges if vid[e] in model and any(b <= p[0] < k - b and b <= p[1] < k - b for p in e)][:20])


if __name__ == '__main__':
    main()
