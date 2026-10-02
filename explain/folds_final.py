import sys, json
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from kt.core import edges, validate, crossing_list
d = json.load(open('/home/nil/nil/knight-formation-research/w-integrator/tours/FOLD24_n96.json'))
t = d['tour']; n = len(t); assert validate(t)
E = sorted(edges(t))
def xy(c): return (c[1], n - 1 - c[0])
def direc(e):
    (x1, y1), (x2, y2) = xy(e[0]), xy(e[1]); dx, dy = x2 - x1, y2 - y1
    return (dx, dy) if dx > 0 else (-dx, -dy)
COL = {(2, 1): '#3b6fb6', (2, -1): '#e08a1e', (1, 2): '#2a9d5b', (1, -2): '#8e44ad'}
pts = []
for e, f in crossing_list(E):
    (x1, y1), (x2, y2) = xy(e[0]), xy(e[1]); (x3, y3), (x4, y4) = xy(f[0]), xy(f[1])
    dd = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4); s = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / dd
    pts.append((x1 + s * (x2 - x1), y1 + s * (y2 - y1)))
fig = plt.figure(figsize=(9, 11.6))
ax = fig.add_axes([0.03, 0.23, 0.94, 0.70])
for e in E:
    (x1, y1), (x2, y2) = xy(e[0]), xy(e[1])
    ax.plot([x1, x2], [y1, y2], color=COL[direc(e)], lw=0.7, alpha=0.8)
ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=7, color='#c0392b', zorder=3)
ax.set_xlim(-1, n); ax.set_ylim(-1, n); ax.set_aspect('equal'); ax.axis('off')
fig.text(0.04, 0.965, f'Fold design: a real tour, n = {n}, {len(pts)} crossings (red dots)', fontsize=15, color='#22303a', weight='bold')
fig.text(0.04, 0.945, 'Colors = the 4 move directions. 8 triangles, each with its own direction.', fontsize=11.5, color='#5a6872')
lines = [
    ('Edges', '1 crossing per row: every line meets its edge steeply, so the U-turn is cheap.', ''),
    ('', '2 per row on a quarter of each edge, to break up closed loops.', '5n'),
    ('Folds', 'all 8 borders: each line bends into its mirror image (a V). No crossings.', '0'),
    ('Diagonals', 'each corner has 1 extra cell of one color; a thin corridor carries it', ''),
    ('', 'to the centre, where +1 -1 +1 -1 cancel. 2/3 crossing per unit length.', '4n/3'),
    ('Centre', 'a fixed patch, the same for every n.', 'const'),
]
y = 0.195
for a, b, c in lines:
    fig.text(0.04, y, a, fontsize=12, weight='bold', color='#22303a')
    fig.text(0.21, y, b, fontsize=11.5, color='#22303a')
    fig.text(0.95, y, c, fontsize=12, weight='bold', color='#0b7a75', ha='right')
    y -= 0.026
fig.text(0.04, y - 0.01, 'Total: 5n + 4n/3 = 19n/3 = 6.33n   (heel design: 9n; paper: 12n)', fontsize=13, weight='bold', color='#0b7a75')
fig.text(0.96, 0.003, 'counts measured 2026-10-02 on n = 96 and 120', fontsize=8.5, color='#8a97a1', ha='right')
plt.savefig('/home/nil/nil/knight-formation-research/explain/folds.png', dpi=120)
