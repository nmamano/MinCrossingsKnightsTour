"""Minimum inversions per line of a periodic bijection f: Z -> Z with f(c) = -c + K (mod 6)
(single-parity gentle seam with c + c' = 0 mod 3; K = 0 for even shifts, 3 for odd shifts).
f(c + P) = f(c) + P. Exhaustive over offsets |f(c) - c| <= B. (KT Edge Searcher)"""
import itertools, sys
def inversions(f, P, R=6):
    # inversions per period: pairs (a < b) with f(a) > f(b), a in [0,P), b any (b - a <= R*P)
    cnt = 0
    for a in range(P):
        for b in range(a + 1, a + R * P):
            fb = f[b % P] + (b // P) * P
            if f[a] > fb: cnt += 1
    for a in range(P):          # also pairs b < a from earlier periods counted via symmetry: count pairs with a in [0,P), b > a only
        pass
    return cnt
for K in (0, 3):
    for P in (6, 12):
        B = 8
        best = None
        choices = []
        for c in range(P):
            opts = [v for v in range(c - B, c + B + 1) if (v + c - K) % 6 == 0]
            choices.append(opts)
        for f in itertools.product(*choices):
            if len({v % P for v in f}) != P: continue      # bijection mod P
            inv = inversions(f, P)
            if best is None or inv < best[0]: best = (inv, f)
        print(f'K={K} P={P}: min inversions per line = {best[0]}/{P}, example {best[1]}')
