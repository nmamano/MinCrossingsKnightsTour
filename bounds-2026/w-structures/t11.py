import sys
from fold3 import build
from repair import repair
n = int(sys.argv[1]); t = int(sys.argv[2])
E, deg = build(n, ts=(t, t, t, t))
h = n // 2
for D in (3, 4, 5, 6):
    for C in (2, 3):
        free = {(x, y) for x in range(n) for y in range(n)
                if min(x, y, n - 1 - x, n - 1 - y) < D or (abs(x - h + 0.5) <= C and abs(y - h + 0.5) <= C)}
        r, st = repair(n, E, free, check_only=True, verbose=False, tlimit=60)
        print(n, t, D, C, st, flush=True)
