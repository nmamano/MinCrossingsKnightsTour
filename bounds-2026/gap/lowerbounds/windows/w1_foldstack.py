#!/usr/bin/env python3
"""Test each W1 central map against the fold-stack phases.

Fold stack (f, dA, dB): f integer linear with f(dA) = f(dB) = 1 for knight moves dA != dB. Each level t of f
chooses c[t] in {dA, dB}; cell P has edges {P - c[f(P)-1], P + c[f(P)]}. Families (up to reversing all
orientations): f = x: (1,2),(1,-2); f = y: (2,1),(-2,1); f = x+y: (2,-1),(-1,2); f = x-y: (2,1),(-1,-2).
A map is a FOLD STACK if one family and one choice sequence reproduce every central cell; otherwise OTHER.
Also lists every (a,b) in [-3,3]^2 with two knight moves at value 1 (completeness of the family list).
"""
import sys, json
from itertools import product
K8 = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
FAM = [((1, 0), (1, 2), (1, -2)), ((0, 1), (2, 1), (-2, 1)), ((1, 1), (2, -1), (-1, 2)), ((1, -1), (2, 1), (-1, -2))]


def fits(m, fam):
    (a, b), dA, dB = fam
    f = lambda p: a * p[0] + b * p[1]
    cells = {tuple(map(int, k.split(','))): frozenset(K8[i] for i in v) for k, v in m.items()}
    lv = sorted({f(p) for p in cells})
    levels = list(range(lv[0] - 1, lv[-1] + 1))
    # constraint propagation: try each sequence (levels <= 14)
    for seq in product((dA, dB), repeat=len(levels)):
        c = dict(zip(levels, seq))
        if all(e == frozenset({(-c[f(p) - 1][0], -c[f(p) - 1][1]), c[f(p)]}) for p, e in cells.items()):
            return True
    return False


def main():
    fams = [(a, b) for a in range(-3, 4) for b in range(-3, 4)
            if sum(1 for d in K8 if a * d[0] + b * d[1] == 1) >= 2]
    print('functionals with >= 2 knight moves at value 1:', fams)
    maps = json.load(open(sys.argv[1]))
    other = []
    for m in maps:
        ok = [i for i, fam in enumerate(FAM) for sgn in (1, -1)
              if fits(m, ((sgn * fam[0][0], sgn * fam[0][1]),
                          (sgn * fam[1][0], sgn * fam[1][1]), (sgn * fam[2][0], sgn * fam[2][1])))]
        if not ok: other.append(m)
    print(f'{len(maps)} maps: {len(maps) - len(other)} fold stacks, {len(other)} other')
    json.dump(other, open(sys.argv[1].replace('.json', '_other.json'), 'w'))
    for m in other[:6]:
        print(m)


if __name__ == '__main__':
    main()
