import sys
from fold3 import build
from imbal import imbalance
n = int(sys.argv[1]); D = int(sys.argv[2]); t = int(sys.argv[3]); C = int(sys.argv[4])
E, deg = build(n, ts=(t, t, t, t))
h = n // 2
ring = {(x, y) for x in range(n) for y in range(n) if min(x, y, n - 1 - x, n - 1 - y) < D}
box = {(x, y) for x in range(n) for y in range(n) if (abs(x - h + 0.5) <= C and abs(y - h + 0.5) <= C)}
print('ring', imbalance(n, E, ring), 'box', imbalance(n, E, box))
bad = [p for p in deg if deg[p] != 2 and p not in ring and p not in box]
print('bad outside free', bad[:10], len(bad))
