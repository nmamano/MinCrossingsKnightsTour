import sys, random
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from kt.core import seg_cross

INK, MUTED, ACC, RED = '#22303a', '#8a97a1', '#0b7a75', '#c0392b'
MOVES = [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]

def tile(a, b):
    """parallelogram: long diagonal ab, short diagonal = unit grid edge with the same midpoint"""
    mx, my = (a[0]+b[0])/2, (a[1]+b[1])/2
    if abs(b[0]-a[0]) == 2:   # midpoint (int, half) -> vertical unit edge
        s1, s2 = (mx, my-0.5), (mx, my+0.5)
    else:
        s1, s2 = (mx-0.5, my), (mx+0.5, my)
    return [a, s1, b, s2]

def clip(subject, clipper):
    def inside(p, a, b): return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0]) >= -1e-12
    def inter(p, q, a, b):
        x1,y1=p; x2,y2=q; x3,y3=a; x4,y4=b
        d=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        t=((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/d
        return (x1+t*(x2-x1), y1+t*(y2-y1))
    out = subject
    cl = clipper if area(clipper) > 0 else clipper[::-1]
    for i in range(len(cl)):
        a, b = cl[i], cl[(i+1) % len(cl)]
        inp, out = out, []
        if not inp: break
        s = inp[-1]
        for e in inp:
            if inside(e, a, b):
                if not inside(s, a, b): out.append(inter(s, e, a, b))
                out.append(e)
            elif inside(s, a, b): out.append(inter(s, e, a, b))
            s = e
    return out
def area(p):
    return 0.5*sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p))) if len(p) > 2 else 0

def grid(ax, xmax, ymax):
    """cells centred at integer points 0..xmax, 0..ymax (dots = cell centres)"""
    for x in range(xmax + 2): ax.plot([x - .5, x - .5], [-.5, ymax + .5], color='#e3e8ec', lw=.8, zorder=0)
    for y in range(ymax + 2): ax.plot([-.5, xmax + .5], [y - .5, y - .5], color='#e3e8ec', lw=.8, zorder=0)
    for x in range(xmax + 1):
        for y in range(ymax + 1): ax.plot(x, y, 'o', ms=3, color='#b8c2c9', zorder=1)

def find_tour(n, seed=1):
    """closed tour by Warnsdorff with random tie-breaks (small n)"""
    rnd = random.Random(seed)
    for attempt in range(20000):
        start = (0, 0); path = [start]; seen = {start}
        cur = start
        while len(path) < n*n:
            cand = [(cur[0]+dx, cur[1]+dy) for dx, dy in MOVES]
            cand = [c for c in cand if 0 <= c[0] < n and 0 <= c[1] < n and c not in seen]
            if not cand: break
            deg = lambda c: sum(1 for dx, dy in MOVES if 0 <= c[0]+dx < n and 0 <= c[1]+dy < n and (c[0]+dx, c[1]+dy) not in seen)
            m = min(deg(c) for c in cand)
            cur = rnd.choice([c for c in cand if deg(c) == m]); path.append(cur); seen.add(cur)
        if len(path) == n*n and (abs(path[-1][0]-start[0]), abs(path[-1][1]-start[1])) in ((1,2),(2,1)):
            return path
    return None

fig = plt.figure(figsize=(12.5, 15))
gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 2.1], hspace=0.38, wspace=0.18)
fig.suptitle('Why every closed knight\'s tour has at least 4n - 2 crossings', x=0.04, ha='left', fontsize=17, fontweight='bold', color=INK)
fig.text(0.04, 0.935, 'Give every knight move a little tile of area exactly 1, then count area.', fontsize=12, color=MUTED)

# panel 1: one move and its tile
ax = fig.add_subplot(gs[0, 0]); ax.set_aspect('equal'); ax.axis('off'); grid(ax, 2, 1)
a, b = (0, 0), (2, 1)
T = tile(a, b); ax.add_patch(Polygon(T, fc=ACC, alpha=.25, ec=ACC, lw=1.5))
ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=2.5); ax.plot(*zip(a, b), 'o', color=INK, ms=7)
ax.plot([1, 1], [0, 1], color=ACC, lw=1.5, ls='--')
ax.set_title('1. The tile of a move', loc='left', fontsize=13.5, fontweight='bold', color=INK)
ax.text(-0.5, -1.0, 'The move is the long diagonal; the unit grid edge\nthrough its midpoint is the short diagonal.\nArea = 1. It stays inside the move\'s bounding box.', fontsize=11, color=INK, va='top')

# panel 2: crossing vs not crossing
ax = fig.add_subplot(gs[0, 1]); ax.set_aspect('equal'); ax.axis('off'); grid(ax, 4, 1)
e = ((0, 0), (2, 1)); f = ((0, 1), (2, 0)); g = ((2, 0), (4, 1))
for (p, q), col in [(e, ACC), (f, '#5b4b9a'), (g, '#b5651d')]:
    ax.add_patch(Polygon(tile(p, q), fc=col, alpha=.22, ec=col, lw=1.3))
    ax.plot([p[0], q[0]], [p[1], q[1]], color=col, lw=2.5)
ov = clip(tile(*e), tile(*f)); ax.add_patch(Polygon(ov, fc=RED, alpha=.55, ec=RED, lw=1))
ax.plot(1, 0.5, 'o', color=RED, ms=8, zorder=6)
ax.set_title('2. Tiles overlap only where moves cross', loc='left', fontsize=13.5, fontweight='bold', color=INK)
ax.text(-0.5, -1.0, f'Crossing moves: tiles overlap (red, area {abs(area(ov)):.2g}).\nNon-crossing moves never overlap (orange vs teal\nonly touch). A crossing overlaps at most 1/2.\n(Checked for all 1,292 relative positions.)', fontsize=11, color=INK, va='top')

# panel 3: count on an 8x8 tour
n = 8
path = find_tour(n)
E = [(path[i], path[(i+1) % len(path)]) for i in range(len(path))]
X = sum(1 for i in range(len(E)) for j in range(i+1, len(E)) if seg_cross(E[i][0], E[i][1], E[j][0], E[j][1]))
ax = fig.add_subplot(gs[1:, :]); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Polygon([(0, 0), (n-1, 0), (n-1, n-1), (0, n-1)], fc='none', ec=INK, lw=2))
for p, q in E:
    ax.add_patch(Polygon(tile(p, q), fc=ACC, alpha=.16, ec='none'))
for i in range(len(E)):
    for j in range(i+1, len(E)):
        if seg_cross(E[i][0], E[i][1], E[j][0], E[j][1]):
            o = clip(tile(*E[i]), tile(*E[j]))
            if len(o) > 2: ax.add_patch(Polygon(o, fc=RED, alpha=.6, ec='none'))
for p, q in E: ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=1.1, alpha=.8)
ax.set_xlim(-0.5, n - 0.5 + 6.3); ax.set_ylim(-0.6, n - 0.4)
ax.set_title(f'3. Count area on a real 8 x 8 tour ({X} crossings)', loc='left', fontsize=13.5, fontweight='bold', color=INK)
tx = n + 0.2
txt = (f'A tour has n^2 moves, so n^2 tiles\nof area 1: total area n^2 = {n*n}.\n\n'
       f'All tiles lie in the box spanned by\nthe cell centres: area (n-1)^2 = {(n-1)**2}.\n\n'
       f'So tiles overlap by at least\nn^2 - (n-1)^2 = 2n - 1 = {2*n-1}.\n\n'
       f'Overlap only happens at crossings,\nat most 1/2 per crossing, so\n\n'
       f'crossings >= 2(2n - 1) = 4n - 2 = {4*n-2}.\n\nThis tour: {X} crossings.\nRed = tile overlaps.')
ax.text(tx, n - 0.6, txt, fontsize=12, color=INK, va='top')
ax.text(tx, 0.2, 'This is the paper\'s 4n bound, with a\none-paragraph proof. The new work\nlocates where the extra overlap must go.', fontsize=11, color=ACC, va='bottom', fontweight='bold')
plt.savefig('/home/nil/nil/knight-formation-research/explain/tiles.png', dpi=160, facecolor='white', bbox_inches='tight')
print('crossings', X)
