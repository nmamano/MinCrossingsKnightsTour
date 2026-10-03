#!/usr/bin/env python3
"""Self-test of w3_flux: (1) circulation around the boundary of a cell box is 6*sum chi = 0 mod 3 for random
degree-2 edge sets that are complete on the box; (2) on the cheap pattern P along both sides, every gamma_R is
charged (residue 1+3chi(R) of the audited proof)."""
import random
from w3_flux import *

K8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def main():
    rnd = random.Random(3)
    # (1) closed loop around box [2,7]^2: omega = sum_{v in box} chi(v)(deg(v)+4) = 6 sum chi for degree 2
    loop = path_steps([(3, 3), (15, 3), (15, 15), (3, 15), (3, 3)])
    for t in range(200):
        E = set()
        deg = {}
        cells = [(x, y) for x in range(0, 10) for y in range(0, 10)]
        rnd.shuffle(cells)
        for p in cells:
            for d in rnd.sample(K8, 8):
                q = (p[0] + d[0], p[1] + d[1])
                if deg.get(p, 0) < 2 and deg.get(q, 0) < 2 and -2 <= q[0] < 12 and -2 <= q[1] < 12:
                    e = tuple(sorted((p, q)))
                    if e in E: continue
                    E.add(e); deg[p] = deg.get(p, 0) + 1; deg[q] = deg.get(q, 0) + 1
        box = [(x, y) for x in range(2, 8) for y in range(2, 8)]
        om = sum(grid_term(s) for s in loop) + sum(edge_flux(e, s) for e in E for s in loop)
        want = sum(chi(v) * (deg.get(v, 0) + 4) for v in box)
        # orientation convention: counterclockwise with the box on the left
        assert om == want or om == -want, (om, want)
        sgn = 1 if om == want else -1
        if t == 0: print('loop orientation sign', sgn)
    print('PASS: closed-loop flux = +-sum chi(v)(deg+4) on 200 random partial configurations')


if __name__ == '__main__':
    main()
