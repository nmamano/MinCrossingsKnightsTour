import sys
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
from kt.core import crossing_list
# left edge, family A' (lines through (x,y)->(x+2,y+1)), board x>=0, rows 0..H
H, W = 60, 10
for de in (1, -1):
    for do in (1, -1):
        E = set()
        for x in range(W):
            for y in range(-10, H + 10):
                if x + 2 < W + 2:
                    E.add(((x, y), (x + 2, y + 1)))
        for y in range(-10, H + 10):
            d = de if y % 2 == 0 else do
            E.add(tuple(sorted([(0, y), (1, y + 2 * d)])))
        # degree check of col 0/1 cells in middle
        from collections import Counter
        deg = Counter()
        for a, b in E:
            deg[a] += 1; deg[b] += 1
        okdeg = all(deg[(x, y)] == 2 for x in (0, 1) for y in range(10, 50))
        def cnt(y0, y1):
            S = [e for e in E if any(y0 <= p[1] < y1 and p[0] <= 3 for p in e)]
            return len(crossing_list(set(S)))
        per = (cnt(10, 50) - cnt(10, 30)) / 20
        print("A' left edge: even dir", de, 'odd dir', do, 'deg ok', okdeg, 'crossings/row', per)
