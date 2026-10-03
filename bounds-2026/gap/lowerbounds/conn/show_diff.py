"""Print, row by row, the edges of a band solution that differ from the original tour (cols 0..K+1)."""
import sys, pickle
from field_close import load, tour_edges


def show(name, E, ylo, yhi, K):
    n, g, d = load(name)
    E0 = tour_edges(g)
    add = E - E0; rem = E0 - E
    for y in range(yhi, ylo - 1, -1):
        A = sorted(e for e in add if min(e[0][1], e[1][1]) == y)
        R = sorted(e for e in rem if min(e[0][1], e[1][1]) == y)
        fmt = lambda L: ' '.join(f'{a[0]},{a[1]}-{b[0]},{b[1]}' for a, b in L)
        if A or R:
            print(f'{y:4d}  +[{fmt(A)}]  -[{fmt(R)}]')
