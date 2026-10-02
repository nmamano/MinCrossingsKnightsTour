#!/usr/bin/env python3
"""Turns Theory FINDINGS 9.5: can the unit square [0,1]^2 have exactly two bad quarters
deep inside a degree-two region with no quarter-area crossing and all multiplicities <= 2?

usage: sq2_lemma.py R [outprefix]   (V = [-R,R]^2; other endpoints in [-R-2,R+2]^2)
Writes outprefix.cnf; if UNSAT, outprefix.drup (check with check_drup.py);
if SAT, outprefix.witness.txt (edge list + picture of multiplicities)."""
import sys, os
from collections import defaultdict
from itertools import combinations, product
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'w-turnstheory'))
from check_knight_tiles import microtiles
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def build(R):
    V = set(product(range(-R, R + 1), repeat=2))
    edges = set()
    for p in V:
        for dx, dy in MOVES:
            q = (p[0] + dx, p[1] + dy)
            edges.add(tuple(sorted((p, q))))
    edges = sorted(edges)
    pool = IDPool()
    var = {e: pool.id(('e', e)) for e in edges}
    cnf = CNF()
    inc = defaultdict(list)
    for e in edges:
        for p in e:
            inc[p].append(var[e])
    for p, lits in inc.items():
        enc = CardEnc.equals if p in V else CardEnc.atmost
        cnf.extend(enc(lits, bound=2, vpool=pool, encoding=EncType.seqcounter).clauses)
    tiles = {e: microtiles(e) for e in edges}
    cover = defaultdict(list)
    for e, T in tiles.items():
        for t in T:
            cover[t].append(e)
    # no pair of tiles sharing exactly one quarter
    banned = 0
    for t, es in cover.items():
        for e, f in combinations(es, 2):
            if e < f and len(tiles[e] & tiles[f]) == 1 and min(tiles[e] & tiles[f]) == t:
                cnf.append([-var[e], -var[f]]); banned += 1
    # all quarter multiplicities <= 2 (selected modelled edges)
    for t, es in cover.items():
        if len(es) > 2:
            cnf.extend(CardEnc.atmost([var[e] for e in es], bound=2, vpool=pool,
                                      encoding=EncType.seqcounter).clauses)
    # central square: exactly two quarters with multiplicity != 1
    u = []
    for k in range(4):
        S = [var[e] for e in cover[(0, 0, k)]]
        uk = pool.id(('u', k)); u.append(uk)
        cnf.append([-uk] + S)                       # u -> at least one
        for a, b in combinations(S, 2):
            cnf.append([-uk, -a, -b])               # u -> at most one
        for a in S:
            cnf.append([uk, -a] + [b for b in S if b != a])  # not u and a -> another
    cnf.extend(CardEnc.equals(u, bound=2, vpool=pool, encoding=EncType.seqcounter).clauses)
    return V, edges, var, tiles, cover, cnf, banned


def main():
    R = int(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else f'sq2_R{R}'
    V, edges, var, tiles, cover, cnf, banned = build(R)
    # sanity: every edge whose tile meets the central square is modelled
    es = set(edges)
    for p in product(range(-6, 7), repeat=2):
        for dx, dy in MOVES:
            e = tuple(sorted((p, (p[0] + dx, p[1] + dy))))
            if any(t[:2] == (0, 0) for t in microtiles(e)):
                assert e in es, e
    cnf.to_file(out + '.cnf')
    print(f'R={R}: {len(edges)} edge vars, {cnf.nv} vars, {len(cnf.clauses)} clauses, '
          f'{banned} banned quarter-area pairs', flush=True)
    with Solver(name='cadical153', bootstrap_with=cnf.clauses, with_proof=True) as s:
        sat = s.solve()
        print('SAT' if sat else 'UNSAT', s.accum_stats(), flush=True)
        if not sat:
            with open(out + '.drup', 'w') as f:
                for line in s.get_proof():
                    f.write(line + '\n')
            print('proof written', out + '.drup')
            return
        model = set(l for l in s.get_model() if l > 0)
    sel = [e for e in edges if var[e] in model]
    C = defaultdict(int)
    for e in sel:
        for t in tiles[e]:
            C[t] += 1
    with open(out + '.witness.txt', 'w') as f:
        f.write(f'# R={R} selected edges\n')
        for e in sel:
            f.write(f'{e}\n')
        f.write('# central square multiplicities (q0 bottom, q1 right, q2 top, q3 left): '
                f'{[C[0,0,k] for k in range(4)]}\n')
        f.write('# squares with a multiplicity != 1 (x, y, [m0..m3]):\n')
        for x, y in product(range(-R, R), repeat=2):
            m = [C[x, y, k] for k in range(4)]
            if m != [1, 1, 1, 1]:
                f.write(f'{x} {y} {m}\n')
    print('central', [C[0, 0, k] for k in range(4)], 'witness written', out + '.witness.txt')


if __name__ == '__main__':
    main()
