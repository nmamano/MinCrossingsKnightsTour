"""Figure: two copies of the T16 bottom piece side by side (real TT16 tour, n=72).
Each cell draws its own half of each of its two moves, in its copy's colour; at the joint the halves meet."""
import sys, json
sys.path.insert(0, '/home/nil/nil/knight-formation-research')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from kt.core import validate, MI, MJ
INK, MUTED = '#22303a', '#8a97a1'
A, B, G = '#2f6db5', '#e07b16', '#c3ccd2'
T16 = ['26 26 26 26 26 26 26 26', '36 26 26 46 26 46 36 26', '25 26 25 26 26 25 26 25', '16 67 06 16 06 16 16 67']
tpl = [r.split() for r in T16]
d = json.load(open('/home/nil/nil/knight-formation-research/w-integrator/tours/TT16_n72.json'))
t = d['tour']; n = len(t); assert validate(t)
# find where the template sits in the bottom 4 rows
starts = [j for j in range(8, n - 24) if all(t[n - 4 + r][j:j + 8] == tpl[r] for r in range(4))]
j0 = starts[len(starts) // 2]
assert all(t[n - 4 + r][j0 + 8:j0 + 16] == tpl[r] for r in range(4))
print('template copies start at columns', starts[:6], '... using', j0, 'and', j0 + 8)
def xy(i, j): return (j - j0, n - 1 - i)
def colour(i, j):
    if i < n - 4 or not (j0 <= j < j0 + 16): return G
    return A if j < j0 + 8 else B
H = 7
fig = plt.figure(figsize=(13, 5.0)); ax = fig.add_axes([0.02, 0.04, 0.96, 0.72])
for i in range(n - H, n):
    for j in range(j0 - 3, j0 + 19):
        x, y = xy(i, j); c = colour(i, j)
        for m in t[i][j]:
            a, b = i + MI[int(m)], j + MJ[int(m)]
            xb, yb = xy(a, b)
            ax.plot([x, (x + xb) / 2], [y, (y + yb) / 2], color=c, lw=2.6 if c != G else 1.2,
                    solid_capstyle='butt', zorder=2 if c != G else 1)
        ax.plot(x, y, 'o', ms=6 if c != G else 3, color=c, zorder=3)
for xb in (-0.5, 7.5, 15.5):
    ax.plot([xb, xb], [-0.7, 3.6], ls='--', color=MUTED, lw=1, zorder=0)
ax.text(3.5, -1.05, 'copy 1', ha='center', fontsize=12, color=A, weight='bold')
ax.text(11.5, -1.05, 'copy 2', ha='center', fontsize=12, color=B, weight='bold')
ax.set_xlim(-3.4, 18.4); ax.set_ylim(-1.4, H - 0.4); ax.set_aspect('equal'); ax.axis('off')
fig.text(0.03, 0.925, 'Two copies of the new bottom piece (4 rows x 8 columns), side by side', fontsize=15, weight='bold', color=INK)
fig.text(0.03, 0.865, 'Each cell draws its own half of each of its two moves, in its copy\'s colour. Where a move crosses the dashed joint,\n'
         'a blue half meets an orange half: the move leaving copy 1 is the same move that copy 2 sends back. Grey = rest of the tour.',
         fontsize=10.5, color=MUTED, va='top')
fig.text(0.97, 0.02, f'cut from a real tour, n = {n}, columns {j0}-{j0 + 15}; 2026-10-02', ha='right', fontsize=8.5, color=MUTED)
plt.savefig('/home/nil/nil/knight-formation-research/explain/fit.png', dpi=130)
