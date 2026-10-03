#!/usr/bin/env python3
"""Parity lemma for the 11.3 blocking field (FINDINGS L2).

In a closed tour, every cut between rows y and y+1 is crossed by an even number of tour edges (the tour is a
closed curve and no knight edge is horizontal). For the field, the edges with an end in column 0 or 1 that
cross a cut inside the run are odd in number (3 or 5); for the cheap patterns P and mirror P they are 4.
So, on every row of a field run, an odd number of crossing edges must lie entirely in columns >= 2.
"""
import check_frac_obstruction as B


def crossing(E, y, cols=(0, 1)):
    return sum(1 for e in E if any(p[0] in cols for p in e) and min(p[1] for p in e) <= y < max(p[1] for p in e))


def main():
    F = B.field()
    M = set()
    for y in range(B.LO, B.HI):
        M.add(B.E2((2, y), (0, y + 1))); M.add(B.E2((3, y), (1, y + 1))); M.add(B.E2((1, y), (0, y + 2)))
    P = {B.E2((p[0], -p[1]), (q[0], -q[1])) for p, q in map(tuple, M)}
    cf = [crossing(F, y) for y in range(10, 30)]
    cm = [crossing(M, y) for y in range(10, 30)]
    cp = [crossing(P, y) for y in range(-30, -10)]
    print('field:', cf); print('mirror P:', cm); print('P:', cp)
    assert all(c % 2 == 1 for c in cf) and set(cm) == {4} and set(cp) == {4}
    print('PASS: field gives an odd count at every cut; P and mirror P give 4.')


if __name__ == '__main__':
    main()
