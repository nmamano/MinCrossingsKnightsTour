#!/usr/bin/env python3
"""Greedy merge of the cycles of a 2-factor by 2-swaps with exact crossing deltas (upper bound on closure cost).

A 2-swap removes edges (a,b), (c,d) of two different cycles and adds (a,c),(b,d) or (a,d),(b,c) (knight moves).
The result has one cycle fewer. Each step takes the swap with the smallest exact change in crossings.
usage: merge.py PICKLE      (prints final X, components, and writes PICKLE.merged)
"""
import sys, pickle
from field_close import E2, cross, components, count_crossings

KN = {(1, 2), (2, 1)}


def knight(a, b):
    return tuple(sorted((abs(a[0] - b[0]), abs(a[1] - b[1])))) == (1, 2)


def main():
    E = set(map(tuple, pickle.load(open(sys.argv[1], 'rb'))))
    E = {E2(tuple(a), tuple(b)) for a, b in E}
    n = int(max(max(a[0], a[1], b[0], b[1]) for a, b in E)) + 1
    X = count_crossings(E)
    print('start X', X, flush=True)
    while True:
        comps = components(n, E)
        if len(comps) == 1: break
        cid = {v: i for i, c in enumerate(comps) for v in c}
        by = {}
        for e in E:
            for p in e: by.setdefault((p[0] // 4, p[1] // 4), []).append(e)
        def near(e):
            out = set()
            for p in e:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        out.update(by.get((p[0] // 4 + dx, p[1] // 4 + dy), ()))
            return out
        def ncross(f, excl):
            return sum(1 for g in near(f) if g not in excl and cross(f, g))
        best = None
        for e in E:
            a, b = e
            for f in near(e):
                if e >= f or cid[a] == cid[f[0]]: continue
                c, d = f
                for g1, g2 in (((a, c), (b, d)), ((a, d), (b, c))):
                    if not (knight(*g1) and knight(*g2)): continue
                    g1, g2 = E2(*g1), E2(*g2)
                    if g1 in E or g2 in E: continue
                    rem = ncross(e, ()) + ncross(f, ()) - cross(e, f)
                    add = ncross(g1, (e, f)) + ncross(g2, (e, f)) + cross(g1, g2)
                    dlt = add - rem
                    if best is None or dlt < best[0]: best = (dlt, e, f, g1, g2)
        dlt, e, f, g1, g2 = best
        E -= {e, f}; E |= {g1, g2}; X += dlt
        print(f'  merge {len(comps)}->{len(comps)-1}: delta {dlt}, X {X}', flush=True)
    assert X == count_crossings(E)
    print('final X', X, 'components', len(components(n, E)))
    pickle.dump(sorted(E), open(sys.argv[1] + '.merged', 'wb'))


if __name__ == '__main__':
    main()
