"""Figure: a real H16a tour (n=48). Grey = moves along the one straight direction; teal = all other moves
(the edge pieces); red = crossings. Shows that every crossing is in a thin band along the edges."""
import sys, json
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from kt.core import edges, validate, crossing_list

INK, MUTED, ACC, RED = '#22303a', '#8a97a1', '#0b7a75', '#c0392b'
d = json.load(open('/home/nil/nil/knight-formation-research/w-integrator/tours/H16a_VerticalEdge_off0_small_n48.json'))
t, n = d['tour'], d['n']
assert validate(t)
E = sorted(edges(t))
def xy(c): return (c[1], n - 1 - c[0])          # column right, row up
def straight(e):
    (i, j), (a, b) = e
    return (a - i, b - j) in ((1, 2), (-1, -2))
cl = crossing_list(E)
pts = []
for e, f in cl:
    (p1, p2), (q1, q2) = [tuple(map(xy, e)), tuple(map(xy, f))]
    x1, y1 = p1; x2, y2 = p2; x3, y3 = q1; x4, y4 = q2
    dd = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    s = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / dd
    pts.append((x1 + s * (x2 - x1), y1 + s * (y2 - y1)))
X = len(pts)
# per-side tally: assign each crossing to its nearest edge
side = {'bottom': 0, 'top': 0, 'left': 0, 'right': 0}
for x, y in pts:
    dist = {'bottom': y, 'top': n - 1 - y, 'left': x, 'right': n - 1 - x}
    side[min(dist, key=dist.get)] += 1
depth = max(min(x, y, n - 1 - x, n - 1 - y) for x, y in pts)
print('n', n, 'X', X, 'by side', side, 'max depth of a crossing from the edge', depth)

fig, axs = plt.subplots(1, 2, figsize=(15, 7.6), gridspec_kw={'width_ratios': [1, 0.9]})
ax = axs[0]
for e in E:
    (x1, y1), (x2, y2) = xy(e[0]), xy(e[1])
    if straight(e): ax.plot([x1, x2], [y1, y2], color='#c9d1d7', lw=0.7, zorder=1)
    else: ax.plot([x1, x2], [y1, y2], color=ACC, lw=0.9, zorder=2)
ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=7, color=RED, zorder=3)
ax.set_xlim(-1, n); ax.set_ylim(-1, n); ax.set_aspect('equal'); ax.axis('off')
ax.set_title(f'A real tour, n = {n}: {X} crossings, all within {depth:.0f} squares of the edge',
             color=INK, fontsize=12, loc='left')

ax = axs[1]; ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
txt = [
    ('Inside the board', 13, INK, 'bold'),
    ('every move goes the same way (grey lines).', 12, INK, None),
    ('Parallel lines never cross: 0 crossings.', 12, INK, None),
    ('', 8, INK, None),
    ('At the edges', 13, INK, 'bold'),
    ('each line hits the edge and must turn back.', 12, INK, None),
    ('Short "edge pieces" (teal) join the line ends in pairs.', 12, INK, None),
    ('All crossings (red) are in these thin edge bands.', 12, INK, None),
    ('', 8, INK, None),
    ('So the count is a sum over the four edges', 13, INK, 'bold'),
    ('crossings = n x (cost per square of edge, added over 4 sides)', 12, INK, None),
    ('', 8, INK, None),
    ('TABLE', 0, INK, None),
    ('', 8, INK, None),
    (f'This tour: bottom {side["bottom"]}, top {side["top"]}, left {side["left"]}, right {side["right"]}', 10, MUTED, None),
    (f'(about 2n, 2n, 2.5n, 2.5n with n = {n}; corners add a few)', 10, MUTED, None),
]
y = 9.6
rows = [(['', 'top + bottom', 'left + right', 'total'], MUTED, None),
        (['Paper (2019)', '3.5 + 3.5', '2.5 + 2.5', '12n'], INK, None),
        (['Shisheng Li', '3.25 + 3.25', '2.5 + 2.5', '11.5n'], INK, None),
        (['New edge piece', '2 + 2', '2.5 + 2.5', '9n'], ACC, 'bold')]
for s, fs, col, w in txt:
    if s == 'TABLE':
        for cells, c2, w2 in rows:
            for xpos, cell in zip((0.2, 3.6, 5.9, 8.2), cells):
                ax.text(xpos, y, cell, fontsize=11, color=c2, fontweight=w2, va='top')
            y -= 0.52
        continue
    ax.text(0.2, y, s, fontsize=fs, color=col, fontweight=w, va='top')
    y -= 0.52 if s else 0.25
fig.text(0.98, 0.02, '2026-10-02', ha='right', color=MUTED, fontsize=9)
plt.tight_layout()
plt.savefig('/home/nil/nil/knight-formation-research/explain/lines_edges.png', dpi=130)
