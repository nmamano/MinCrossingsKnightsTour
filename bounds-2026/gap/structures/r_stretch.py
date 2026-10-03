# KT Structures, 2026-10-03. Stretch LB's R filling (gap/lowerbounds/beyond5/b5f_box_H40_R10_30.json: U-collar box,
# H = 40, R on rows 10..29) to box height 40 + D by repeating the period-1 slice of edges whose lower end is in row 20.
# Output: gadget JSON (H, remove, add) for c5w_insert.py. usage: r_stretch.py D OUT.json
import sys, json
from pathlib import Path
from collections import defaultdict
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'verifier'))
from claim38_switch import edge
D = int(sys.argv[1]); out = sys.argv[2]
def pn(v):
    x, y = v
    return {(2, y+1), (1, y-2)} if x == 0 else {(3, y+1), (0, y+2)} if x == 1 else {(x+2, y+1), (x-2, y-1)}
src = json.loads((Path(__file__).resolve().parents[1]/'lowerbounds/beyond5/b5f_box_H40_R10_30.json').read_text())
H0 = src['H']
base0 = {edge((x, y), w) for x in range(12) for y in range(-10, H0+11) for w in pn((x, y))}
rem = {edge(tuple(a), tuple(b)) for a, b in src['remove']}; add = {edge(tuple(a), tuple(b)) for a, b in src['add']}
F = (base0 - rem) | add
lo = lambda e: min(e[0][1], e[1][1])
sh = lambda e, k: edge((e[0][0], e[0][1]+k), (e[1][0], e[1][1]+k))
slice20 = [e for e in F if lo(e) == 20 and all(v[0] < 12 for v in e)]
F2 = {e for e in F if lo(e) < 20} | {sh(e, k) for e in slice20 for k in range(D+1)} | {sh(e, D) for e in F if lo(e) > 20}
H = H0 + D
base = {edge((x, y), w) for x in range(12) for y in range(-10, H+11) for w in pn((x, y))}
F2 = {e for e in F2 if all(0 <= v[0] < 12 and -10 <= v[1] <= H+10 for v in e)}
deg = defaultdict(int)
for a, b in F2: deg[a] += 1; deg[b] += 1
bad = [v for v, d in deg.items() if d != 2 and 0 < v[0] < 9 and -6 < v[1] < H+6]
print('H', H, 'edges', len(F2), 'degree errors inside', len(bad))
V = {(x, y) for x in range(6) for y in range(H)}
inside = lambda e: all(v in V for v in e)
Path(out).write_text(json.dumps(dict(H=H, remove=sorted(e for e in base - F2 if inside(e)), add=sorted(e for e in F2 - base if inside(e)), source='LB b5f R filling, stretched')))
