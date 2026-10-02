"""Figure: close-up of the bottom edge of a real TT16 tour (n=72), turns marked.
Shows 2 turns per column in the bottom band = the minimum from the turns lemma."""
import sys, json
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from kt.core import edges, validate, num_turns, MI, MJ
INK, MUTED, ACC, RED = '#22303a', '#8a97a1', '#0b7a75', '#c0392b'
d = json.load(open('/home/nil/nil/knight-formation-research/w-integrator/tours/TT16_n72.json'))
t = d['tour']; n = len(t); assert validate(t)
T = num_turns(t)
STRAIGHT = ('04', '40', '15', '51', '26', '62', '37', '73')
def xy(i, j): return (j, n - 1 - i)
def is_turn(i, j): return t[i][j] not in STRAIGHT
# turns in the 4 rows next to the bottom edge, away from corners
x0, x1 = 16, 56
bt = sum(is_turn(i, j) for i in range(n - 4, n) for j in range(x0, x1))
print('n', n, 'turns', T, '8n-14 =', 8 * n - 14, '| bottom 4 rows, columns', x0, '..', x1 - 1, ':', bt, 'turns =', bt / (x1 - x0), 'per column')
W0, W1, H = 16, 40, 9        # window: columns W0..W1-1, rows 0..H-1 from the bottom
fig, ax = plt.subplots(figsize=(12, 6.2))
ax.axhspan(-0.5, 3.5, color='#eef3f3', zorder=0)
for (a, b) in edges(t):
    (xa, ya), (xb, yb) = xy(*a), xy(*b)
    if max(ya, yb) > H + 1 or min(xa, xb) < W0 - 2 or max(xa, xb) > W1 + 1: continue
    ax.plot([xa, xb], [ya, yb], color='#9aa7b0', lw=1.1, zorder=1)
for i in range(n - H, n):
    for j in range(W0, W1):
        x, y = xy(i, j)
        if is_turn(i, j): ax.plot(x, y, 'o', ms=7, color=RED, zorder=3)
        else: ax.plot(x, y, 'o', ms=2.5, color='#b8c2c9', zorder=2)
ax.set_xlim(W0 - 0.7, W1 - 0.3); ax.set_ylim(-0.8, H - 0.3); ax.set_aspect('equal'); ax.axis('off')
ax.text(W0 - 0.6, 3.25, 'bottom 4 rows', fontsize=10, color=MUTED, va='top')
fig.text(0.03, 0.93, 'Turns upper bound: the new bottom piece has 2 turns per column', fontsize=15, weight='bold', color=INK)
fig.text(0.03, 0.885, f'Close-up of a real tour (n = {n}, {T} turns = 8n - 14). Red = turn. Grey = straight cell.', fontsize=11, color=MUTED)
fig.text(0.03, 0.10, 'Per side, turns per unit length:   your paper  2.625 + 2.625 (top, bottom) + 2 + 2 (left, right) = 9.25n', fontsize=11.5, color=INK)
fig.text(0.03, 0.055, '                                                 new         2 + 2 + 2 + 2 = 8n.   Turns lemma: every side needs >= 2.  So 8n is tight.', fontsize=11.5, color=ACC, weight='bold')
fig.text(0.97, 0.01, '2026-10-02', ha='right', fontsize=8.5, color=MUTED)
plt.savefig('/home/nil/nil/knight-formation-research/explain/turns_upper.png', dpi=130)
