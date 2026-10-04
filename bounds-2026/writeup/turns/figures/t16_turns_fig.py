#!/usr/bin/env python3
"""Bottom-left part of the 16-turn tour (gen_TT16, n = 48) in the style of band_paths_fig.py, with every turn marked
(Personal Site Agent, 2026-10-04). Replaces the older t16_band figure from blog_figs.py. Dashed: the 6 x 6 corner,
and two 8 x 4 blocks of the bottom piece (16 turns each).
Output: writeup/turns/images/t16_band.png.
usage (from the project root): .venv/bin/python writeup/turns/figures/t16_turns_fig.py"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / 'demo'))
from build_data import gen_TT16
from kt.core import MI, MJ
from tt16 import is_turn

INK, TURN = '#22303a', '#c0392b'
n = 48
grid = gen_TT16(n)[0]
g = {}
for i, row in enumerate(grid):
    for j, code in enumerate(row):
        x, y = j, n - 1 - i
        g[x, y] = [(x + MJ[int(k)], y - MI[int(k)]) for k in code]
X0, X1, Y0, Y1 = 0, 26, 0, 9
BLOCKS = (6, 14)           # next to the 6 x 6 corner
per = [sum(is_turn(g, (x, y)) for x in range(a, a + 8) for y in range(4)) for a in BLOCKS]
assert per == [16, 16], per
W = {(x, y) for x in range(X0, X1) for y in range(Y0, Y1)}

fig, ax = plt.subplots(figsize=(9.6, 3.6))
ax.set_xlim(X0 - .9, X1 - .4); ax.set_ylim(Y0 - .9, Y1 - .4); ax.set_aspect('equal'); ax.axis('off')
for x in range(X0, X1):
    for y in range(Y0, Y1):
        if (x + y) % 2 == 0: ax.add_patch(mp.Rectangle((x - .5, y - .5), 1, 1, color='#eef1f4', lw=0, zorder=0))
ax.plot([X0 - .5, X1 - .5], [-.5, -.5], color=INK, lw=2, zorder=1)          # bottom side of the board
ax.plot([-.5, -.5], [Y0 - .5, Y1 - .5], color=INK, lw=2, zorder=1)          # left side of the board
drawn = set()
for u in W:
    for v in g[u]:
        e = tuple(sorted((u, v)))
        if e in drawn: continue
        drawn.add(e)
        ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], color='#7d8a96', lw=1.1, zorder=2, solid_capstyle='round')
for p in W:
    if is_turn(g, p): ax.plot(*p, 'o', color=TURN, ms=5, zorder=4)
# dashed outlines on top of the paths, each edge drawn once
# The blocks start right after the corner, so the corner and the blocks form one outline plus inner dividers.
assert BLOCKS[0] == 6
xe = BLOCKS[-1] + 8 - .5
ax.plot([-.5, 5.5, 5.5, xe, xe, -.5, -.5], [5.5, 5.5, 3.5, 3.5, -.5, -.5, 5.5], color=INK, lw=1.4, ls='--', zorder=6)
for a in BLOCKS:
    ax.plot([a - .5, a - .5], [-.5, 3.5], color=INK, lw=1.4, ls='--', zorder=6)
out = ROOT / 'writeup' / 'turns' / 'images' / 't16_band.png'
fig.savefig(out, bbox_inches='tight', dpi=160, facecolor='white')
print('wrote', out, 'turns per block:', per)
