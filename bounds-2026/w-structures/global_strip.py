"""Global repair: fold field fixed in the interior, all edge strips (depth D) + centre box free.
CP-SAT minimises crossings with lazy single-cycle cuts. KT Structures 2026-10-02."""
import sys, time, json
from fold3 import build
from repair import repair
from kt.core import validate, num_crossings, num_turns
MI = [-2, -1, 1, 2, 2, 1, -1, -2]; MJ = [1, 2, 2, 1, -1, -2, -2, -1]
def to_grid(n, E):
    """board.js grid: tour[i][j], i row down = n-1-y, j = x."""
    nb = {}
    for a, b in E:
        nb.setdefault(a, []).append(b); nb.setdefault(b, []).append(a)
    code = {}
    for m in range(8):
        code[(MJ[m], -MI[m])] = m
    g = [['' for _ in range(n)] for _ in range(n)]
    for (x, y), lst in nb.items():
        g[n - 1 - y][x] = ''.join(str(c) for c in sorted(code[(q[0] - x, q[1] - y)] for q in lst))
    return g
if __name__ == '__main__':
    n = int(sys.argv[1]); D = int(sys.argv[2]); t = int(sys.argv[3]); C = int(sys.argv[4]); tl = float(sys.argv[5])
    h = n // 2
    E, deg = build(n, ts=(t, t, t, t), flip=lambda r, y: h - n // 4 <= y < h)
    free = {(x, y) for x in range(n) for y in range(n)
            if min(x, y, n - 1 - x, n - 1 - y) < D or (abs(x - h + 0.5) <= C and abs(y - h + 0.5) <= C)}
    t0 = time.time()
    E2, st = repair(n, E, free, threads=2, tlimit=tl, max_rounds=400, hint=set(E))
    print('n', n, 'status', st, 'time', round(time.time() - t0))
    if E2:
        g = to_grid(n, E2)
        ok = validate(g)
        X = num_crossings(g); T = num_turns(g)
        print('n', n, 'valid', ok, 'X', X, 'X/n %.3f' % (X / n), 'T', T)
        json.dump([' '.join(r) for r in g], open(f'tours/fold_n{n}_D{D}.json', 'w'))
