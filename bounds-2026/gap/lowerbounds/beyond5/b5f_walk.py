# B5f test input: up-edges (x y dx dy) of cells x = 0..5, rows Y0..Y1, of the U field with an optional patch
# (JSON with 'remove' / 'add' edge lists, Verifier / Structures format). usage: b5f_walk.py Y0 Y1 [patch.json]
import sys, json
Y0, Y1 = int(sys.argv[1]), int(sys.argv[2])
def pn(x, y):
    if x == 0: return {(2, y + 1), (1, y - 2)}
    if x == 1: return {(3, y + 1), (0, y + 2)}
    return {(x + 2, y + 1), (x - 2, y - 1)}
E = {tuple(sorted(((x, y), w))) for x in range(12) for y in range(Y0 - 8, Y1 + 8) for w in pn(x, y)}
if len(sys.argv) > 3:
    g = json.load(open(sys.argv[3]))
    E -= {tuple(sorted((tuple(a), tuple(b)))) for a, b in g['remove']}; E |= {tuple(sorted((tuple(a), tuple(b)))) for a, b in g['add']}
for y in range(Y0, Y1 + 1):
    for x in range(6):
        for a, b in E:
            for p, q in ((a, b), (b, a)):
                if p == (x, y) and q[1] > y and 0 <= q[0] <= 5: print(x, y, q[0] - x, q[1] - y)
