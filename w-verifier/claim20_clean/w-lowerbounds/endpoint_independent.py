#!/usr/bin/env python3
"""Independent check for endpoint_stab.py (no import of strip_dp.py or endpoint_stab.py).

Graph: strip2_independent.build_graph() (separate width-two strip code).
Augmented state = (base state, frozenset of the TEST edges that straddle the current row and are
selected so far). At column 0 the set starts with the pending edges of the state; each arc adds the new
edges whose lower end is the processed cell; at the row end the test is evaluated from the set
(F = sum of coefficients mod 3 == 2, and not both EXC edges), b charged, and the set reset.
Weights q*(4w-1) - 4*p*b; Bellman-Ford from a virtual source (all zeros) must converge.

usage: python3 endpoint_independent.py ORIENT p q     (ORIENT = up | down | both)
"""
import sys
import strip2_independent as S

LIST = [(((0, -1), (1, 1)), -1), (((0, 0), (1, -2)), -1), (((0, 0), (2, -1)), -1), (((0, 2), (1, 0)), -1),
        (((1, 0), (2, 2)), -1), (((1, 1), (2, -1)), -1), (((0, 1), (1, -1)), 1), (((0, 1), (2, 0)), 1)]
EXC = [((0, 0), (2, 1)), ((0, 1), (2, 0))]


def norm(a, b):
    return (a, b) if a <= b else (b, a)


def make_tests(orient):
    signs = {'up': [1], 'down': [-1], 'both': [1, -1]}[orient]
    tests = []
    for s in signs:
        refl = lambda p: (p[0], s * p[1])
        coef = {}
        for (a, b), c in LIST:
            coef[norm(refl(a), refl(b))] = c
        exc = frozenset(norm(refl(a), refl(b)) for a, b in EXC)
        tests.append((coef, exc))
    return tests


def main():
    orient, p, q = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    tests = make_tests(orient)
    watch = set()
    for coef, exc in tests:
        watch |= set(coef) | exc
    states, arcs = S.build_graph()
    print('base states', len(states), 'arcs', len(arcs), flush=True)

    def fails(seen):
        for coef, exc in tests:
            F = sum(coef.get(e, 0) for e in seen)
            if F % 3 != 2 or len(exc & seen) == 2:
                return True
        return False

    node = {}
    def nid(k):
        if k not in node:
            node[k] = len(node)
        return node[k]
    out = {}
    for u, v, w in arcs:
        out.setdefault(u, []).append((v, w))
    A = []
    todo = [(u, frozenset()) for u in range(len(states)) if states[u][0] == 0]
    done = set(todo)
    while todo:
        u, seen = todo.pop()
        col, pend = states[u]
        if col == 0:
            seen = frozenset(norm(a, b) for a, b, c in pend if norm(a, b) in watch)
        for v, w in out.get(u, []):
            vcol, vpend = states[v]
            dy = 1 if vcol == 0 else 0
            new = {norm((a[0], a[1] + dy), (b[0], b[1] + dy)) for a, b, c in vpend if a == (col, -dy)}
            seen2 = seen | frozenset(e for e in new if e in watch)
            if vcol == 0:
                b_ = 1 if fails(seen2) else 0
                key2 = (v, frozenset())
                A.append((nid((u, seen if col else frozenset())), nid(key2), q * (4 * w - 1) - 4 * p * b_))
            else:
                key2 = (v, seen2)
                A.append((nid((u, seen if col else frozenset())), nid(key2), q * (4 * w - 1)))
            if key2 not in done:
                done.add(key2); todo.append(key2)
    print('augmented nodes', len(node), 'arcs', len(A), flush=True)
    dist = [0] * len(node)
    it = 0
    while True:
        it += 1
        ch = False
        for a, b, ww in A:
            if dist[a] + ww < dist[b]:
                dist[b] = dist[a] + ww; ch = True
        if not ch:
            print(f'{orient} beta={p}/{q}: converged after {it} passes, no negative cycle; '
                  f'potential range {min(dist)}..{max(dist)} (units 1/(4q))')
            return
        if it > 100000:
            print('no convergence after', it, 'passes'); return


if __name__ == '__main__':
    main()
