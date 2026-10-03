"""Figure: a real fold-design tour. Each move is colored by its direction (4 undirected directions);
red dots are crossings. Shows the regions, the folds between them, and where the crossings are."""
import sys, json
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from kt.core import edges, validate, crossing_list

name = sys.argv[1] if len(sys.argv) > 1 else 'FOLD24_n96'
d = json.load(open(f'/home/nil/nil/knight-formation-research/w-integrator/tours/{name}.json'))
t = d['tour']; n = len(t)
assert validate(t)
E = sorted(edges(t))
def xy(c): return (c[1], n - 1 - c[0])
def direc(e):
    (x1, y1), (x2, y2) = xy(e[0]), xy(e[1])
    dx, dy = x2 - x1, y2 - y1
    if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
    return (dx, dy)
COL = {(2, 1): '#3b6fb6', (2, -1): '#e08a1e', (1, 2): '#2a9d5b', (1, -2): '#8e44ad'}
pts = []
for e, f in crossing_list(E):
    (x1, y1), (x2, y2) = xy(e[0]), xy(e[1]); (x3, y3), (x4, y4) = xy(f[0]), xy(f[1])
    dd = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    s = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / dd
    pts.append((x1 + s * (x2 - x1), y1 + s * (y2 - y1)))
cnt = {k: sum(direc(e) == k for e in E) for k in COL}
print(name, 'n', n, 'X', len(pts), 'moves by direction', cnt)
fig, ax = plt.subplots(figsize=(10, 10))
for e in E:
    (x1, y1), (x2, y2) = xy(e[0]), xy(e[1])
    ax.plot([x1, x2], [y1, y2], color=COL[direc(e)], lw=0.8, alpha=0.85)
ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=6, color='#c0392b', zorder=3)
ax.set_xlim(-1, n); ax.set_ylim(-1, n); ax.set_aspect('equal'); ax.axis('off')
ax.set_title(f'{name}: n = {n}, {len(pts)} crossings', loc='left')
plt.tight_layout(); plt.savefig(f'/home/nil/nil/knight-formation-research/explain/folds_raw.png', dpi=110)
# tally crossings by location
reg = {'edge band (<= 3 from edge)': 0, 'diagonal folds': 0, 'centre (<= 6)': 0, 'other': 0}
c0 = (n - 1) / 2
for x, y in pts:
    if min(x, y, n - 1 - x, n - 1 - y) <= 3: reg['edge band (<= 3 from edge)'] += 1
    elif max(abs(x - c0), abs(y - c0)) <= 6: reg['centre (<= 6)'] += 1
    elif min(abs(x - y), abs(x + y - (n - 1))) <= 4: reg['diagonal folds'] += 1
    else: reg['other'] += 1
print(reg)
