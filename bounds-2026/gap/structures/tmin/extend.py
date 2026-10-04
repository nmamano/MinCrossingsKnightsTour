# KT Structures, 2026-10-04. Extend a solution grid by duplicating a periodic band of rows and of columns.
# A band rows a..a+k-1 with g[a+k] == g[a] and g[a+k+1] == g[a+1] can be repeated (edges reach 2 rows), and the result
# is again a 2-factor. Bands stay inside rows 4..n-5 so corner squares are unchanged and T - 8n is preserved.
# usage: extend.py src.json n_max out_prefix   (writes out_prefix_n<N>.json for every tour found)
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from kt.core import validate, num_turns, num_cycles

def bands(g):
    n = len(g); out = []
    for k in range(2, n, 2):
        for a in range(4, n - 4 - k - 1):
            if g[a + k] == g[a] and g[a + k + 1] == g[a + 1]:
                out.append((a, k))
    return out

def dup_rows(g, a, k, times=1):
    return g[:a + k] + g[a:a + k] * times + g[a + k:]

def transpose(g):
    # transpose swaps (di, dj): move codes map MI/MJ -> swapped; code m with (di,dj) -> code with (dj,di)
    MI = [-2, -1, 1, 2, 2, 1, -1, -2]; MJ = [1, 2, 2, 1, -1, -2, -2, -1]
    tr = {m: [q for q in range(8) if MI[q] == MJ[m] and MJ[q] == MI[m]][0] for m in range(8)}
    n = len(g)
    return [[''.join(str(tr[int(c)]) for c in g[i][j]) for i in range(n)] for j in range(len(g[0]))]

def main():
    src, nmax, pre = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    g0 = json.loads(Path(src).read_text())['grid']; n0 = len(g0)
    base = num_turns(g0) - 8 * n0
    rb = bands(g0); cb = bands(transpose(g0))
    print('src', src, 'n', n0, 'T-8n', base, 'row bands', rb[:6], 'col bands', cb[:6])
    found = {}
    for (a, k) in rb:
        for (b, kc) in cb:
            if kc != k: continue
            for times in range(1, (nmax - n0) // k + 1):
                g = dup_rows(g0, a, k, times)
                g = transpose(dup_rows(transpose(g), b, k, times))
                N = n0 + k * times
                if N in found: continue
                if validate(g):
                    found[N] = (a, k, b)
                    Path(f'{pre}_n{N}.json').write_text(json.dumps(dict(n=N, T=num_turns(g), T_minus_8n=num_turns(g) - 8 * N,
                        src=src, row_band=[a, k], col_band=[b, k], times=times, date='2026-10-04', grid=g)))
                    print('tour n', N, 'T-8n', num_turns(g) - 8 * N, 'bands', (a, k), (b, k), 'times', times)
                else:
                    pass
    print('sizes with a tour:', sorted(found))

if __name__ == '__main__':
    main()
