"""Adversary search: periodic width-two strip fields vs the refined endpoint penalty (KT Structures, 2026-10-03).

Field = periodic edge set S (period p rows) of edges with an endpoint in columns 0,1 (other endpoint in columns
0..3). Rules as in the strip model: columns 0,1 degree exactly 2, columns 2,3 degree <= 2, no finite cycle.
Per period: D0 = strip crossings - p, R = column-0 crossings - p, A = sum of endpoint penalties a (up or down test,
best parity phase), A' = sum of a' = max(0, a - q/2), q = bad quarters of the endpoint square [1,2]x[r,r+1]
(uncovered, or in the overlap of a crossing pair that is not a column-0 pair).
Prints the fields with the smallest D0/(A-R) and D0/(A'-R).
usage: python stripenum.py p"""
import sys
from collections import Counter
from itertools import combinations
sys.path[:0] = ['../../w-turnstheory']
from check_knight_tiles import microtiles, cross

COEF = {((0,-1),(1,1)): -1, ((0,0),(1,-2)): -1, ((0,0),(2,-1)): -1, ((0,1),(1,-1)): 1,
        ((0,1),(2,0)): 1, ((0,2),(1,0)): -1, ((1,0),(2,2)): -1, ((1,1),(2,-1)): -1}
norm = lambda e: tuple(sorted(e))
COEF = {norm(k): v for k, v in COEF.items()}
EXC = (norm(((0,0),(2,1))), norm(((0,1),(2,0))))

def base_edges(y):
    return [norm(((0,y),(1,y+2))), norm(((0,y),(1,y-2))), norm(((0,y),(2,y+1))), norm(((0,y),(2,y-1))),
            norm(((1,y),(2,y+2))), norm(((1,y),(2,y-2))), norm(((1,y),(3,y+1))), norm(((1,y),(3,y-1)))]

def enumerate_fields(p):
    cand = sorted({e for y in range(p) for e in base_edges(y)})
    # canonical: edge e stands for its translates by multiples of p
    canon = lambda e: norm(((e[0][0], e[0][1] % p), (e[1][0], e[1][1] - (e[0][1] - e[0][1] % p))))
    cand = sorted({canon(e) for e in cand})
    cells = [(x, y) for x in range(4) for y in range(p)]
    inc = {c: [] for c in cells}
    for i, e in enumerate(cand):
        for v in e:
            inc[(v[0], v[1] % p)].append(i)
    order = sorted(range(len(cand)))
    res = []
    choice = [0] * len(cand)
    deg = Counter()
    def ok_partial(i):
        for v in cand[i]:
            c = (v[0], v[1] % p)
            if deg[c] > 2: return False
        return True
    def complete():
        return all(deg[(x, y)] == 2 for x in (0, 1) for y in range(p))
    def rec(i):
        if i == len(cand):
            if complete(): res.append([cand[j] for j in range(len(cand)) if choice[j]])
            return
        # prune: a col-0/1 cell whose remaining edges cannot reach degree 2
        for take in (0, 1):
            choice[i] = take
            if take:
                for v in cand[i]: deg[(v[0], v[1] % p)] += 1
            good = (not take) or ok_partial(i)
            if good:
                # check cells whose last candidate edge is i
                for x in (0, 1):
                    for y in range(p):
                        c = (x, y)
                        if max(inc[c]) == i and deg[c] != 2: good = False
                if good: rec(i + 1)
            if take:
                for v in cand[i]: deg[(v[0], v[1] % p)] -= 1
        choice[i] = 0
    rec(0)
    return res

def unroll(S, p, k0, k1):
    return {norm(((a[0], a[1] + t*p), (b[0], b[1] + t*p))) for a, b in S for t in range(k0, k1)}

def has_cycle(E):
    par = {}
    def f(u):
        while par.setdefault(u, u) != u:
            par[u] = par[par[u]]; u = par[u]
        return u
    for a, b in E:
        ra, rb = f(a), f(b)
        if ra == rb: return True
        par[ra] = rb
    return False

def evaluate(S, p, orient):
    U = unroll(S, p, -6, 7)
    if orient == 'down':
        U = {norm(((a[0], -a[1]), (b[0], -b[1]))) for a, b in U}
    lo, hi = 0, (p if p % 2 == 0 else 2 * p)   # whole periods covering both row parities
    # crossings assigned to row max(min_y e, min_y f) in [lo,hi)
    El = sorted(U)
    X = b0 = 0
    for e, f in combinations(El, 2):
        r = max(min(e[0][1], e[1][1]), min(f[0][1], f[1][1]))
        if not (lo <= r < hi): continue
        if abs(e[0][1] - f[0][1]) > 6: continue
        if cross(e, f):
            X += 1
            if min(e[0][0], e[1][0]) == 0 and min(f[0][0], f[1][0]) == 0: b0 += 1
    tiles = {e: microtiles(e) for e in El if -10 <= e[0][1] <= p + 10}
    mult = Counter(q for ts in tiles.values() for q in ts)
    nonB = set()
    keys = list(tiles)
    for e, f in combinations(keys, 2):
        if abs(e[0][1] - f[0][1]) > 6 or not cross(e, f): continue
        if min(e[0][0], e[1][0]) == 0 and min(f[0][0], f[1][0]) == 0: continue
        nonB |= tiles[e] & tiles[f]
    best = None
    for phase in (0, 1):
        A = A2 = 0.0
        for r in range(lo, hi):
            sh = {norm(((a[0], a[1] - r), (b[0], b[1] - r))) for a, b in U if abs(a[1] - r) <= 4}
            F = sum(COEF.get(e, 0) for e in sh)
            exc = EXC[0] in sh and EXC[1] in sh
            c = 1 if (r + phase) % 2 == 0 else -1
            h = ((1 + c) // 2 + c * (F + 2)) % 3
            a = 1.0 if exc else {0: 0.5, 1: 1.0, 2: 0.0}[h]
            q = sum(1 for k in range(4) if mult[(1, r, k)] == 0 or (1, r, k) in nonB)
            A += a; A2 += max(0.0, a - q / 2)
        cand = (A, A2, phase)
        if best is None or cand[:2] > best[:2]: best = cand
    return X - hi, b0 - hi, best

if __name__ == '__main__':
    p = int(sys.argv[1])
    F = enumerate_fields(p)
    print(p, 'raw fields', len(F))
    rows = []
    for S in F:
        if has_cycle(unroll(S, p, -6, 7)): continue
        for orient in ('up', 'down'):
            D0, R, (A, A2, ph) = evaluate(S, p, orient)
            rows.append((D0, R, A, A2, orient, ph, S))
    print('acyclic field-orientations', len(rows))
    def ratio(D0, R, A):
        return D0 / (A - R) if A - R > 1e-9 else float('inf')
    rows.sort(key=lambda z: ratio(z[0], z[1], z[2]))
    print('old penalty a: smallest D0/(A-R):')
    for z in rows[:4]: print('  ', round(ratio(z[0], z[1], z[2]), 4), 'D0', z[0], 'R', z[1], 'A', z[2], "A'", z[3], z[4], 'phase', z[5], z[6])
    rows.sort(key=lambda z: ratio(z[0], z[1], z[3]))
    print("refined penalty a': smallest D0/(A'-R):")
    for z in rows[:6]: print('  ', round(ratio(z[0], z[1], z[3]), 4), 'D0', z[0], 'R', z[1], 'A', z[2], "A'", z[3], z[4], 'phase', z[5], z[6])
