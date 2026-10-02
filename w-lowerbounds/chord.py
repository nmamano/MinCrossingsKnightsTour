# Do non-crossing matchings M_I exist with M_U u M_I a single cycle? M_U = {(2m, 2m+3 mod N)}
import sys
from functools import lru_cache
def ncm(lo, hi):
    # all non-crossing perfect matchings of points lo..hi-1 (linear)
    if lo >= hi:
        yield []
        return
    for j in range(lo + 1, hi, 2):
        for a in ncm(lo + 1, j):
            for b in ncm(j + 1, hi):
                yield [(lo, j)] + a + b
def cycles(N, M1, M2):
    p1 = {}; p2 = {}
    for a, b in M1: p1[a] = b; p1[b] = a
    for a, b in M2: p2[a] = b; p2[b] = a
    seen = set(); c = 0
    for s in range(N):
        if s in seen: continue
        c += 1; x = s; use1 = True
        while True:
            seen.add(x)
            x = p1[x] if use1 else p2[x]
            seen.add(x)
            use1 = not use1
            if x == s and use1: break
    return c
for N in range(6, 23, 2):
    MU = [(2*m % N, (2*m+3) % N) for m in range(N//2)]
    # check MU is a perfect matching
    pts = sorted(p for e in MU for p in e)
    if pts != list(range(N)):
        print(N, 'MU not perfect'); continue
    best = None; cnt1 = 0; tot = 0
    for M in ncm(0, N):
        tot += 1
        c = cycles(N, MU, M)
        if best is None or c < best: best = c
        if c == 1: cnt1 += 1
    print(N, 'non-crossing M_I:', tot, 'min cycles', best, 'single-cycle count', cnt1)
